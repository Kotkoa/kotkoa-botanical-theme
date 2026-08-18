#!/usr/bin/env python3
"""Fail-closed validator for a Shopify image SEO dry-run plan."""

import argparse
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"INVALID: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: str):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def product_from_backup(data):
    if data.get("errors"):
        fail(f"backup contains GraphQL errors: {data['errors']}")
    if isinstance(data.get("data"), dict):
        product = data["data"].get("productByIdentifier") or data["data"].get("product")
        if product:
            return product
    if data.get("id") and data.get("media") and data.get("variants"):
        return data
    fail("backup does not contain a product")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    parser.add_argument("backup")
    parser.add_argument("--expected-handle", required=True)
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    plan = load(args.plan)
    product = product_from_backup(load(args.backup))

    if plan.get("handle") != args.expected_handle:
        fail("plan handle differs from --expected-handle")
    if product.get("handle") != args.expected_handle:
        fail("backup handle differs from --expected-handle")
    if plan.get("productId") != product.get("id"):
        fail("plan Product ID differs from backup")

    status = plan.get("status")
    if args.require_approved and status != "approved-not-applied":
        fail("live apply requires status approved-not-applied")
    if status not in {"draft-not-applied", "approved-not-applied", "applied-success"}:
        fail(f"unsupported status {status!r}")

    keep = plan.get("keepMediaIds")
    detach = plan.get("detachFromProductMediaIds")
    if not isinstance(keep, list) or not keep:
        fail("keepMediaIds must be a non-empty list")
    if not isinstance(detach, list):
        fail("detachFromProductMediaIds must be a list")
    if len(keep) != len(set(keep)) or len(detach) != len(set(detach)):
        fail("duplicate media ID inside keep or detach list")
    if set(keep) & set(detach):
        fail("keep and detach media lists overlap")

    backup_media = product.get("media", {}).get("nodes", [])
    backup_ids = [item.get("id") for item in backup_media]
    if None in backup_ids or len(backup_ids) != len(set(backup_ids)):
        fail("backup media IDs are missing or duplicated")
    if set(keep) | set(detach) != set(backup_ids):
        missing = set(backup_ids) - (set(keep) | set(detach))
        unknown = (set(keep) | set(detach)) - set(backup_ids)
        fail(f"plan does not partition backup media; missing={sorted(missing)}, unknown={sorted(unknown)}")
    if plan.get("plannedMediaCount") != len(keep):
        fail("plannedMediaCount differs from keepMediaIds count")
    if plan.get("sharedVariantMediaId") not in set(keep):
        fail("sharedVariantMediaId is not retained")

    variants = product.get("variants", {}).get("nodes", [])
    variant_ids = {item.get("id") for item in variants}
    current_variant_media = {
        item.get("id"): {media.get("id") for media in item.get("media", {}).get("nodes", [])}
        for item in variants
    }
    changes = plan.get("variantMediaChanges")
    if not isinstance(changes, list):
        fail("variantMediaChanges must be a list")
    changed_variants = set()
    for index, change in enumerate(changes):
        variant_id = change.get("variantId")
        old = change.get("detachMediaId")
        new = change.get("appendMediaId")
        if variant_id not in variant_ids:
            fail(f"variantMediaChanges[{index}] has unknown variant")
        if variant_id in changed_variants:
            fail(f"variant {variant_id} appears more than once")
        changed_variants.add(variant_id)
        if old not in current_variant_media.get(variant_id, set()):
            fail(f"detach media {old} is not attached to variant {variant_id} in backup")
        if old not in set(detach) and old not in set(keep):
            fail(f"detach media {old} is outside the approved partition")
        if new not in set(keep):
            fail(f"append media {new} is not retained")

    metadata = plan.get("metadataUpdates")
    if not isinstance(metadata, list) or len(metadata) != len(keep):
        fail("metadataUpdates must contain exactly one entry per retained media")
    metadata_ids = [item.get("id") for item in metadata]
    if set(metadata_ids) != set(keep) or len(metadata_ids) != len(set(metadata_ids)):
        fail("metadataUpdates IDs must equal keepMediaIds exactly")
    for index, item in enumerate(metadata):
        filename = item.get("filename")
        alt = item.get("alt")
        if not isinstance(filename, str) or not filename or "/" in filename or filename != filename.lower() or " " in filename:
            fail(f"metadataUpdates[{index}] has unsafe filename")
        if not isinstance(alt, str) or not alt.strip():
            fail(f"metadataUpdates[{index}] has empty alt")
        original = next(x for x in backup_media if x.get("id") == item.get("id"))
        url = (original.get("image") or {}).get("url", "").split("?", 1)[0]
        original_ext = Path(url).suffix.lower()
        if original_ext and Path(filename).suffix.lower() != original_ext:
            fail(f"metadataUpdates[{index}] changes file extension")

    if plan.get("filesDeleted") is not False or plan.get("pixelsChanged") is not False:
        fail("filesDeleted and pixelsChanged must both be false")

    print(
        f"VALID: {args.expected_handle}: {len(keep)} keep + {len(detach)} detach = "
        f"{len(backup_ids)} media; {len(changes)} variant changes; status={status}"
    )


if __name__ == "__main__":
    main()
