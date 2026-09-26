---
name: graphql-scanning
description: GraphQL 安全扫描配方（introspection / depth / batch）
when_to_use: 目标暴露 /graphql、/api/graphql
---
# GraphQL 安全扫描（三连测）

```bash
EP='https://target/graphql'
H=(-H 'Content-Type: application/json')

# Test 1 introspection -> 响应含 "data" 则 MEDIUM
curl -sSk "${H[@]}" -X POST -d '{"query":"{__schema{types{name}}}"}' "$EP" | grep -q '"data"' \
  && { echo "introspection ENABLED (MEDIUM)"; add_finding medium graphql_introspection_enabled \
       "GraphQL introspection enabled" "$EP" curl ""; }

# Test 2 query depth -> 不含 error 则 HIGH
D=$(printf '{ %.0s' $(seq 1 10)); D="$D""field"; for i in $(seq 1 10); do D="$D }"; done
curl -sSk "${H[@]}" -X POST -d "{\"query\":\"$D\"}" "$EP" | grep -qi error \
  || { echo "no depth limit (HIGH)"; add_finding high graphql_no_depth_limit \
       "No query depth limiting (tested 10)" "$EP" curl ""; }

# Test 3 batch -> 含 "data" 则 MEDIUM
B=$(printf '{"query":"{field}"},%.0s' $(seq 1 10)); B="[${B%,}]"
curl -sSk "${H[@]}" -X POST -d "$B" "$EP" | grep -q '"data"' \
  && { echo "batch allowed (MEDIUM)"; add_finding medium graphql_batch_allowed \
       "GraphQL batch queries allowed" "$EP" curl ""; }
```

命中后的固定建议：关闭 introspection、限制查询深度、
批量限流、查询复杂度分析、敏感操作鉴权。

## 深挖
```bash
# 完整 introspection 落盘
curl -sSk "${H[@]}" -X POST \
  -d '{"query":"{__schema{queryType{name}mutationType{name}types{name kind fields{name args{name type{name kind ofType{name}}}}}}}"}' \
  "$EP" > $RUN/parsed/graphql_schema.json
jq -r '.data.__schema.types[] | select(.kind=="OBJECT") | .name' $RUN/parsed/graphql_schema.json | sort -u
```
拿到 schema 后用 `http/framework.md` 的 repeater 重放 mutation / 越权字段。
