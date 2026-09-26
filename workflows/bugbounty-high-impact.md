---
name: bug-bounty-high-impact
when_to_use: 只关注 RCE/SQLi/SSRF/LFI/XXE
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | nuclei | severity=critical, tags="rce,sqli,ssrf,lfi,xxe" |
| 2 | sqlmap | batch=true, level=3, risk=3, tamper=space2comment |
| 3 | jaeles | signatures="rce,sqli,ssrf", threads=30 |
| 4 | dalfox | blind=true, mining_dom=true |
