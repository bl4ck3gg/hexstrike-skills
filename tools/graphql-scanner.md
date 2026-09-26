---
name: graphql-scanner
category: API 安全
description: GraphQL introspection / 深度 / 批量测试
when_to_use: 目标存在 /graphql
---
**配方**: `api-security/graphql.md`

```bash
EP='https://target/graphql'; H=(-H 'Content-Type: application/json')
curl -sSk "${H[@]}" -X POST -d '{"query":"{__schema{types{name}}}"}' "$EP"   # introspection
D=$(printf '{ %.0s' $(seq 1 10)); D="$D""field"; for i in $(seq 1 10); do D="$D }"; done
curl -sSk "${H[@]}" -X POST -d "{\"query\":\"$D\"}" "$EP"                    # depth
```
