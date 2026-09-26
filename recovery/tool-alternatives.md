---
name: tool-alternatives
when_to_use: 换工具
---
# 工具替代表
nmap→rustscan,masscan,zmap | rustscan→nmap,masscan | masscan→nmap,rustscan,zmap
gobuster→feroxbuster,dirsearch,ffuf,dirb | feroxbuster→gobuster,dirsearch,ffuf | dirsearch→gobuster,feroxbuster,ffuf | ffuf→gobuster,feroxbuster,dirsearch
nuclei→jaeles,nikto,w3af | jaeles→nuclei,nikto | nikto→nuclei,jaeles,w3af
katana→gau,waybackurls,hakrawler | gau→katana,waybackurls,hakrawler | waybackurls→gau,katana,hakrawler
burpsuite→http-framework,browser-agent,zap
arjun→paramspider,x8,ffuf | paramspider→arjun,x8 | x8→arjun,paramspider
sqlmap→sqlninja,jsql-injection
dalfox→xsser,xsstrike
subfinder→amass,assetfinder,findomain | amass→subfinder,assetfinder,findomain | assetfinder→subfinder,amass,findomain
prowler→scout-suite,cloudmapper | scout-suite→prowler,cloudmapper
trivy→clair,docker-bench-security | clair→trivy,docker-bench-security
ghidra→radare2,ida,binary-ninja | radare2→ghidra,objdump,gdb | gdb→radare2,lldb
pwntools→ropper,ropgadget | ropper→ropgadget,pwntools | ropgadget→ropper,pwntools

上下文:
- require_no_privileges → 跳过 nmap/masscan
- prefer_faster_tools → 跳过 amass/w3af
