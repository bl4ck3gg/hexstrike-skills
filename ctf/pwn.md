---
name: ctf-pwn
when_to_use: CTF Pwn
---
# CTF Pwn 策略
1. buffer_overflow
2. format_string
3. rop_chains
4. heap_exploitation
5. race_conditions
6. integer_overflow

## 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 二进制侦察 | checksec, file, strings, objdump | ✓ | 600s |
| 2 | 静态分析 | ghidra, radare2, ida | ✓ | 1800s |
| 3 | 动态分析 | gdb-peda, ltrace, strace | ✗ | 1200s |
| 4 | 漏洞识别 | manual | ✗ | 900s |
| 5 | 利用开发 | pwntools, ropper, one-gadget | ✗ | 2400s |
| 6 | 本地测试 | gdb-peda | ✗ | 600s |
| 7 | 远程利用 | pwntools | ✗ | 600s |
| 8 | 后利用 | manual | ✗ | 300s |

## 回退
alternative_exploitation / information_leaks / heap_feng_shui / ret2libc_variants / sigreturn_oriented

## 验证
exploit_reliability / payload_verification / shell_validation / flag_retrieval

二进制载荷文件（buffer/cyclic/random）与 offset 定位见 `payloads/file-generation.md`。
