# Доступ к картинкам продуктов через "Kotkoa Image SEO"

Это не приложение с UI/дашбордом — это Dev Dashboard app (client-credentials grant),
подключённое через этот репозиторий. Готового "экспорта" нет — доступ идёт через
Admin GraphQL API, авторизацию делает локальный скилл или прямой curl-запрос.

## Где что лежит

- Креды (client ID/secret, домен магазина, версия API):
  `/Users/kotkoa/dev/kotkoa-botanical-theme/.env`
  (не коммитится, не печатать в чат/логи; шаблон полей — `.env.example` рядом)
- Скилл с полным протоколом работы с картинками товара:
  `.pi/skills/shopify-image-seo-cycle/SKILL.md`
  `.pi/skills/shopify-image-seo-cycle/references/workflow.md`
  `.pi/skills/shopify-image-seo-cycle/scripts/validate_plan.py`
  (дублируется в `.claude/skills/shopify-image-seo-cycle/` — то же самое)
- Артефакты аудита/применения (создаются скиллом по ходу работы):
  `audits/image-seo/<slug>.md`
  `audits/image-seo/<slug>-dry-run.json`
  `audits/image-seo/backups/...`
- Общий контекст проекта и правила: `CLAUDE.md` в корне репозитория,
  раздел "Tooling: image SEO skill and Admin API access".

## Что за приложение

- Название в Shopify Partner/Dev Dashboard: **Kotkoa Image SEO**
- Grant type: client credentials (машинный токен, без OAuth-редиректа)
- Scopes: `read_products`, `write_products`, `read_files`, `write_files`
- Этих scope достаточно для любых Admin GraphQL операций с медиа товаров,
  коллекций и файлов — отдельное приложение/scope не нужны.

## Как получить токен вручную (если не через скилл)

```bash
set -a; source .env; set +a

curl -s -X POST "https://${SHOPIFY_STORE}/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SHOPIFY_CLIENT_ID}" \
  -d "client_secret=${SHOPIFY_CLIENT_SECRET}" \
  | jq -r '.access_token'
```

Токен короткоживущий — получать заново на каждую сессию, не сохранять в файлы,
не печатать в чат.

## Как забрать картинки конкретного товара (read-only)

```bash
TOKEN="<токен из шага выше>"

curl -s -X POST "https://${SHOPIFY_STORE}/admin/api/${SHOPIFY_API_VERSION}/graphql.json" \
  -H "X-Shopify-Access-Token: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query($handle: String!) { productByHandle(handle: $handle) { id title media(first: 50) { nodes { id alt ... on MediaImage { image { url width height } } } } variants(first: 50) { nodes { id title media(first: 10) { nodes { id } } } } } }",
    "variables": { "handle": "<product-handle>" }
  }'
```

Это возвращает media ID, alt, URL, размеры — то есть все нужные "картинки" и метаданные.

## Важно

- **Не** использовать этот доступ для прямых правок в обход скилла — правила
  дедупликации/переименования/alt зафиksированы в `workflow.md` (три
  gated-команды `/image-1-audit`, `/image-2-approve`, `/image-3-apply`).
  Для чтения (просто "показать картинки") прямой curl-запрос выше — ок.
- Никогда не использовать `fileDelete` — только `referencesToRemove` в `fileUpdate`.
- Один product handle за цикл, никаких батчей.
