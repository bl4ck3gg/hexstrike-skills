---
name: bug-bounty-reconnaissance
when_to_use: 赏金侦察
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | amass | mode=enum, passive=false |
| 2 | subfinder | silent=true, all_sources=true |
| 3 | httpx | probe/tech_detect/status_code=true |
| 4 | katana | depth=3, js_crawl=true, form_extraction=true |
| 5 | gau | include_subs=true |
| 6 | waybackurls | get_versions=false |
| 7 | paramspider | level=2 |
| 8 | arjun | method="GET,POST", stable=true |
