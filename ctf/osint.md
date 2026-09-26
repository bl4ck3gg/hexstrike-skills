---
name: ctf-osint
when_to_use: CTF OSINT
---
# CTF OSINT 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 目标识别 | manual | ✗ | 300s |
| 2 | 自动侦察 | sherlock, theHarvester, sublist3r | ✓ | 1200s |
| 3 | 社媒 | sherlock, social-analyzer | ✓ | 900s |
| 4 | 域名 | whois, dig, amass | ✓ | 600s |
| 5 | 搜索引擎 | shodan, censys | ✓ | 900s |
| 6 | 关联 | manual | ✗ | 1200s |
| 7 | 验证 | manual | ✗ | 600s |

## 回退
alternative_sources / historical_data / social_engineering / cross_reference / deep_web_search
