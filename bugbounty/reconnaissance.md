---
name: bb-reconnaissance
when_to_use: 赏金侦察
---
# Bug Bounty 侦察工作流
## Phase 1 子域发现 (~300s)
amass {domain, mode=enum} / subfinder {silent} / assetfinder {domain}
## Phase 2 HTTP 服务 (~180s)
httpx {probe, tech_detect, status_code} / nuclei {tags=tech, severity=info}
## Phase 3 内容发现 (~600s)
katana {depth=3, js_crawl} / gau {include_subs} / waybackurls / dirsearch
## Phase 4 参数发现 (~240s)
paramspider {level=2} / arjun {method="GET,POST", stable} / x8 {method=GET}
总计 ~1320s,12 工具
