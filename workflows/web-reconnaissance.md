---
name: web-reconnaissance
when_to_use: 目标为 Web 应用
---
# Web 侦察剧本
| # | 工具 | 参数 |
|---|------|------|
| 1 | nmap | scan_type="-sV -sC", ports="80,443,8080,8443" |
| 2 | httpx | probe=true, tech_detect=true |
| 3 | katana | depth=3, js_crawl=true |
| 4 | gau | include_subs=true |
| 5 | waybackurls | get_versions=false |
| 6 | nuclei | severity="critical,high", tags="tech" |
| 7 | dirsearch | extensions="php,html,js,txt", threads=30 |
| 8 | gobuster | mode="dir", extensions="php,html,js,txt" |
