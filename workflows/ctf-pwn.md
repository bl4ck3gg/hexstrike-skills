---
name: ctf-pwn-challenge
when_to_use: CTF Pwn
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | pwninit | template_type=python |
| 2 | checksec | - |
| 3 | ghidra | analysis_timeout=180 |
| 4 | ropper | gadget_type=all, quality=3 |
| 5 | angr | analysis_type=symbolic |
| 6 | one-gadget | level=2 |
