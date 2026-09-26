---
name: target-types
description: 目标类型枚举
when_to_use: 任务开始判断目标类别
---
# 目标类型
| 类型 | 识别规则 | 典型工具 |
|------|---------|---------|
| WEB_APPLICATION | http(s):// 且非 /api/ | nmap, gobuster, nuclei, nikto, sqlmap, ffuf, katana, httpx, wpscan |
| API_ENDPOINT | URL 含 /api/ | nuclei, ffuf, arjun, paramspider, httpx, x8, katana |
| NETWORK_HOST | IPv4 正则 | nmap, nmap-advanced, masscan, rustscan, autorecon, enum4linux-ng, smbmap, responder |
| CLOUD_SERVICE | 含 amazonaws/azure/googleapis | prowler, scout-suite, cloudmapper, pacu, trivy, kube-hunter, kube-bench, checkov, terrascan |
| BINARY_FILE | .exe/.bin/.elf/.so/.dll | ghidra, radare2, gdb, angr, pwntools, ropper, one-gadget, libc-database, checksec, binwalk, pwninit |
| UNKNOWN | 其他 | 先侦察 |

派生:
- attack_surface_score = 类型基数 + 技术×0.5 + 端口×0.3 + 子域×0.2 + CMS 1.5,上限 10
- risk_level: ≥8 critical / ≥6 high / ≥4 medium / ≥2 low / else minimal
- confidence: 0.5 + IP +0.1 + 技术 +0.2 + CMS +0.1 + 类型非 UNKNOWN +0.1
