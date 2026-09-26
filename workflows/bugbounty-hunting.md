---
name: bug-bounty-vulnerability-hunting
when_to_use: 漏洞挖掘阶段
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | nuclei | severity="critical,high", tags="rce,sqli,xss,ssrf" |
| 2 | dalfox | mining_dom=true, mining_dict=true |
| 3 | sqlmap | batch=true, level=2, risk=2 |
| 4 | jaeles | threads=20, timeout=20 |
| 5 | ffuf | match_codes="200,204,301,302,307,401,403", threads=40 |
