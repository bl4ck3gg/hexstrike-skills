---
name: api-fuzzer
category: API 测试
description: API 端点模糊测试配方（端点发现 + 多方法测试）
when_to_use: 目标含 /api/ 或已知 API base
---
**配方**: `api-security/fuzzing.md`

```bash
BASE='https://api.target.com'
for ep in v1/users v1/login v1/admin graphql; do
  for m in GET POST PUT DELETE; do
    printf '%-6s %-20s %s\n' "$m" "$ep" \
      "$(curl -sSk -o /dev/null -w '%{http_code}|%{size_download}' -X $m "$BASE/${ep#/}")"
  done
done
```
端点发现（ffuf，判定码 200,201,202,204,301,302,307,401,403,405）：
```bash
ffuf -u "$BASE/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
     -mc 200,201,202,204,301,302,307,401,403,405 -t 50
```
