---
name: ctf-parallel-tasks
when_to_use: 并发跑多工具
---
# 并行任务分组
| 类别 | 组 | 工具 | 并发 |
|------|----|------|------|
| web | reconnaissance | httpx, whatweb, katana | 3 |
| web | directory_enumeration | gobuster, dirsearch, feroxbuster | 2 |
| web | parameter_discovery | arjun, paramspider | 2 |
| web | vulnerability_scanning | sqlmap, dalfox, nikto | 2 |
| crypto | hash_cracking | hashcat, john | 2 |
| crypto | cipher_analysis | frequency-analysis, substitution-solver | 2 |
| crypto | factorization | factordb, yafu | 2 |
| pwn | binary_analysis | checksec, file, strings, objdump | 4 |
| pwn | static_analysis | ghidra, radare2 | 2 |
| pwn | gadget_finding | ropper, ropgadget | 2 |
| forensics | file_analysis | binwalk, foremost, strings | 3 |
| forensics | steganography | stegsolve, zsteg, outguess | 3 |
| rev | initial_analysis | file, strings, checksec | 3 |
| rev | disassembly | ghidra, radare2 | 2 |
| osint | username_search | sherlock, social-analyzer | 2 |
| osint | domain_recon | sublist3r, amass, dig | 3 |
