---
name: optimization-profiles
when_to_use: stealth/normal/aggressive 参数
---
# 参数优化档案
## nmap
| 档位 | scan_type | timing | additional |
|------|-----------|--------|-----------|
| stealth | -sS | -T2 | --max-retries 1 --host-timeout 300s |
| normal | -sS -sV | -T4 | --max-retries 2 |
| aggressive | -sS -sV -sC -O | -T5 | --max-retries 3 --min-rate 1000 |
## gobuster
| 档位 | threads | delay | timeout |
|------|---------|-------|---------|
| stealth | 5 | 1s | 30s |
| normal | 20 | 0s | 10s |
| aggressive | 50 | 0s | 5s |
## sqlmap
| 档位 | level | risk | threads | delay |
|------|-------|------|---------|-------|
| stealth | 1 | 1 | 1 | 1 |
| normal | 2 | 2 | 5 | 0 |
| aggressive | 3 | 3 | 10 | 0 |

强制 stealth: 检测到 WAF(cloudflare/incapsula/sucuri) 时
