---
name: api-testing
when_to_use: 目标为 API
---
# API 测试剧本
| # | 工具 | 参数 |
|---|------|------|
| 1 | httpx | probe=true, tech_detect=true |
| 2 | arjun | method="GET,POST", stable=true |
| 3 | x8 | method="GET" |
| 4 | paramspider | level=2 |
| 5 | nuclei | tags="api,graphql,jwt", severity="high,critical" |
| 6 | ffuf | mode="parameter", method="POST" |
