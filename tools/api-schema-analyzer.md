---
name: api-schema-analyzer
category: API 安全
description: OpenAPI/Swagger schema 审计
when_to_use: 发现 openapi.json / swagger.json
---
**配方**: `api-security/schema-analysis.md`

```bash
curl -sSk 'https://target/openapi.json' -o /tmp/schema.json
jq -r '.paths | to_entries[] | .key as $p | .value | to_entries[]
  | "\(.key|ascii_upcase)\t\($p)\t\((.value.security // [])|tostring)"' /tmp/schema.json
```
无 security → medium；参数名含 password/token/key/secret → high。
