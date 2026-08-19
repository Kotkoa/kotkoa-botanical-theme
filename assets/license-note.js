function updateLicenseNote(container, licenseValue) {
  if (!licenseValue) return;

  const value = licenseValue.toLowerCase();
  const standard = container.querySelector('[data-license-text-standard]');
  const extended = container.querySelector('[data-license-text-extended]');

  standard?.toggleAttribute('hidden', value !== 'standard');
  extended?.toggleAttribute('hidden', value !== 'extended');
  container.removeAttribute('hidden');
}

document.querySelectorAll('[data-license-note]').forEach((container) => {
  const variantSelects = container.closest('variant-selects');
  const optionIndex = Number(container.dataset.licenseOptionIndex);

  const selectedVariantScript = variantSelects?.querySelector('[data-selected-variant]');
  if (selectedVariantScript) {
    try {
      const variant = JSON.parse(selectedVariantScript.textContent);
      updateLicenseNote(container, variant?.options?.[optionIndex]);
    } catch (error) {
      // ignore malformed initial JSON, event-driven updates will still work
    }
  }
});

if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined') {
  subscribe(PUB_SUB_EVENTS.variantChange, (event) => {
    const container = document.querySelector(
      `#variant-selects-${event.data.sectionId} [data-license-note]`
    );
    if (!container) return;

    const optionIndex = Number(container.dataset.licenseOptionIndex);
    updateLicenseNote(container, event.data.variant?.options?.[optionIndex]);
  });
}
