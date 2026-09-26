---
name: fallback-chains
when_to_use: 关键操作主工具失败
---
# 降级链
## network_discovery
1 [nmap, rustscan, masscan]
2 [rustscan, nmap]
3 [ping, telnet]
## web_discovery
1 [gobuster, feroxbuster, dirsearch]
2 [feroxbuster, ffuf]
3 [curl, wget]
## vulnerability_scanning
1 [nuclei, jaeles, nikto]
2 [nikto, w3af]
3 [curl]
## subdomain_enumeration
1 [subfinder, amass, assetfinder]
2 [amass, findomain]
3 [dig, nslookup]
## parameter_discovery
1 [arjun, paramspider, x8]
2 [ffuf, wfuzz]
3 [manual_testing]

## 关键操作
network_discovery / web_discovery / vulnerability_scanning / subdomain_enumeration

## 部分失败补位
缺 open_ports → 基础端口检查
缺 directories → 基础目录探测
缺 vulns → 基础安全头检查
