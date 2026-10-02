---
name: ctf-strategy-matrix
description: CTF 分类 × 子能力 × 工具矩阵，以及 7 分类的解题策略清单
when_to_use: 拿到题目先定分类，再选策略与工具
---
# CTF 策略矩阵

先按 `ctf/<category>.md` 定分类，用本文件选**策略**（§2）再选**工具**（§1）。
具体命令模板见 `ctf/tool-commands.md`；并行分组见 `ctf/parallel-tasks.md`。

## 1. 分类 × 子能力 × 工具 `category_tools`

### web
| 子能力 | 工具 |
|---|---|
| reconnaissance | httpx, katana, gau, waybackurls |
| vulnerability_scanning | nuclei, dalfox, sqlmap, nikto |
| content_discovery | gobuster, dirsearch, feroxbuster |
| parameter_testing | arjun, paramspider, x8 |
| specialized | wpscan, joomscan, droopescan |

### crypto
| 子能力 | 工具 |
|---|---|
| hash_analysis | hashcat, john, hash-identifier |
| cipher_analysis | cipher-identifier, cryptool, cyberchef |
| rsa_attacks | rsatool, factordb, yafu |
| frequency_analysis | frequency-analysis, substitution-solver |
| modern_crypto | sage, pycrypto, cryptography |

### pwn
| 子能力 | 工具 |
|---|---|
| binary_analysis | checksec, ghidra, radare2, gdb-peda |
| exploit_development | pwntools, ropper, one-gadget |
| heap_exploitation | glibc-heap-analysis, heap-viewer |
| format_string | format-string-exploiter |
| rop_chains | ropgadget, ropper, angr |

### forensics
| 子能力 | 工具 |
|---|---|
| file_analysis | file, binwalk, foremost, photorec |
| image_forensics | exiftool, steghide, stegsolve, zsteg |
| memory_forensics | volatility, rekall |
| network_forensics | wireshark, tcpdump, networkminer |
| disk_forensics | autopsy, sleuthkit, testdisk |

### rev
| 子能力 | 工具 |
|---|---|
| disassemblers | ghidra, ida, radare2, binary-ninja |
| debuggers | gdb, x64dbg, ollydbg |
| decompilers | ghidra, hex-rays, retdec |
| packers | upx, peid, detect-it-easy |
| analysis | strings, ltrace, strace, objdump |

### misc
| 子能力 | 工具 |
|---|---|
| encoding | base64, hex, url-decode, rot13 |
| compression | zip, tar, gzip, 7zip |
| qr_codes | qr-decoder, zbar |
| audio_analysis | audacity, sonic-visualizer |
| esoteric | brainfuck, whitespace, piet |

### osint
| 子能力 | 工具 |
|---|---|
| search_engines | google-dorking, shodan, censys |
| social_media | sherlock, social-analyzer |
| image_analysis | reverse-image-search, exif-analysis |
| domain_analysis | whois, dns-analysis, certificate-transparency |
| geolocation | geoint, osm-analysis, satellite-imagery |

## 2. 解题策略清单 `solving_strategies`

按顺序试，命中即停；每条策略的具体命令见 `ctf/tool-commands.md`。

### web
1. `source_code_analysis` — Analyze HTML/JS source for hidden information
2. `directory_traversal` — Test for path traversal vulnerabilities
3. `sql_injection` — Test for SQL injection in all parameters
4. `xss_exploitation` — Test for XSS and exploit for admin access
5. `authentication_bypass` — Test for auth bypass techniques
6. `session_manipulation` — Analyze and manipulate session tokens
7. `file_upload_bypass` — Test file upload restrictions and bypasses

### crypto
1. `frequency_analysis` — Perform frequency analysis for substitution ciphers
2. `known_plaintext` — Use known plaintext attacks
3. `weak_keys` — Test for weak cryptographic keys
4. `implementation_flaws` — Look for implementation vulnerabilities
5. `side_channel` — Exploit timing or other side channels
6. `mathematical_attacks` — Use mathematical properties to break crypto

### pwn
1. `buffer_overflow` — Exploit buffer overflow vulnerabilities
2. `format_string` — Exploit format string vulnerabilities
3. `rop_chains` — Build ROP chains for exploitation
4. `heap_exploitation` — Exploit heap-based vulnerabilities
5. `race_conditions` — Exploit race condition vulnerabilities
6. `integer_overflow` — Exploit integer overflow conditions

### forensics
1. `file_carving` — Recover deleted or hidden files
2. `metadata_analysis` — Analyze file metadata for hidden information
3. `steganography` — Extract hidden data from images/audio
4. `memory_analysis` — Analyze memory dumps for artifacts
5. `network_analysis` — Analyze network traffic for suspicious activity
6. `timeline_analysis` — Reconstruct timeline of events

### rev
1. `static_analysis` — Analyze binary without execution
2. `dynamic_analysis` — Analyze binary during execution
3. `anti_debugging` — Bypass anti-debugging techniques
4. `unpacking` — Unpack packed/obfuscated binaries
5. `algorithm_recovery` — Reverse engineer algorithms
6. `key_recovery` — Extract encryption keys from binaries

## 3. 使用顺序

```
1. 分类   -> ctf/<category>.md（web|crypto|pwn|forensics|rev|osint|misc）
2. 选策略 -> 本文件 §2，按序试
3. 选工具 -> 本文件 §1 的子能力分组
4. 并行   -> ctf/parallel-tasks.md
5. 验证   -> ctf/validation.md
6. 卡住   -> recovery/*，或 ctf/<category>.md 的"回退"小节
```
