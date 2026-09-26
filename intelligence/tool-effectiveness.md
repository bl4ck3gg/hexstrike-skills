---
name: tool-effectiveness
description: 各目标类型下工具有效性评分
when_to_use: 工具优先级排序
---
# 工具有效性评分

## Web Application
nuclei 0.95 / wpscan 0.95 / dalfox 0.93 / jaeles 0.92 / sqlmap 0.90 / ffuf 0.90 / arjun 0.90 / burpsuite 0.90 / gobuster 0.90 / katana 0.88 / x8 0.88 / dirsearch 0.87 / nikto 0.85 / feroxbuster 0.85 / httpx 0.85 / paramspider 0.85 / gau 0.82 / waybackurls 0.80 / nmap 0.80 / qsreplace 0.75 / anew 0.70 / uro 0.70

## Network Host
nmap-advanced 0.97 / nmap 0.95 / autorecon 0.95 / masscan 0.92 / rustscan 0.90 / enum4linux-ng 0.88 / responder 0.88 / smbmap 0.85 / arp-scan 0.85 / netexec 0.85 / rpcclient 0.82 / hydra 0.80 / enum4linux 0.80 / nbtscan 0.75 / amass 0.70

## API Endpoint
arjun 0.95 / x8 0.92 / nuclei 0.90 / httpx 0.90 / paramspider 0.88 / jaeles 0.88 / ffuf 0.85 / katana 0.85 / postman 0.80

## Cloud Service
prowler 0.95 / scout-suite 0.92 / trivy 0.90 / kube-hunter 0.90 / checkov 0.90 / kube-bench 0.88 / terrascan 0.88 / cloudmapper 0.88 / falco 0.87 / pacu 0.85 / clair 0.85 / docker-bench-security 0.85

## Binary File
ghidra 0.95 / gdb-peda 0.92 / radare2 0.90 / pwntools 0.90 / angr 0.88 / ropper 0.88 / ropgadget 0.85 / pwninit 0.85 / gdb 0.85 / one-gadget 0.82 / libc-database 0.80 / binwalk 0.80 / checksec 0.75 / objdump 0.75 / strings 0.70

## 选择规则
- objective=quick → 取评分前 3
- objective=comprehensive → 取 >0.7
- objective=stealth → 只用 amass/subfinder/httpx/nuclei
