---
name: api-schema-analysis
description: API Schema 审计配方（OpenAPI/Swagger）
when_to_use: 发现 openapi.json / swagger.json / api-docs
---
# API Schema 分析

```bash
S='https://target/openapi.json'
curl -sSk "$S" -o $RUN/parsed/schema.json
jq -e . $RUN/parsed/schema.json >/dev/null 2>&1 || {
  echo "invalid_json (HIGH)"; add_finding high api_invalid_schema "Schema is not valid JSON" "$S" curl ""; exit 0; }

# 1) 逐端点列出鉴权要求
jq -r '.paths | to_entries[] | .key as $p | .value | to_entries[]
  | select(.value|type=="object")
  | "\(.key|ascii_upcase)\t\($p)\t\((.value.security // [])|tostring)"' $RUN/parsed/schema.json \
  | tee $RUN/parsed/schema_endpoints.tsv

# 2) 无 security -> MEDIUM
awk -F'\t' '$3=="[]"' $RUN/parsed/schema_endpoints.tsv | while IFS=$'\t' read -r m p s; do
  add_finding medium api_no_auth "$m $p has no auth requirement" "$S" jq ""; echo "no-auth: $m $p"; done

# 3) 敏感参数 -> HIGH
jq -r '.paths[][]?.parameters[]? | select(.name|test("password|token|key|secret";"i")) | .name' \
  $RUN/parsed/schema.json | sort -u | while read -r n; do
  add_finding high api_sensitive_param "sensitive param: $n" "$S" jq ""; echo "sensitive: $n"; done
```

## 常见 schema 路径（逐个试）
```bash
for p in /openapi.json /swagger.json /api-docs /v3/api-docs /swagger/v1/swagger.json /.well-known/openapi.json; do
  code=$(curl -sSk -o /dev/null -w '%{http_code}' "https://target$p")
  echo "$code $p"
done
```
深挖：无鉴权端点用 `http/framework.md` repeater 实测；敏感参数结合 `payloads/*`。
