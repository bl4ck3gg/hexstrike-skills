---
name: ctf-rev
when_to_use: CTF Rev
---
# CTF Rev 策略
1. static_analysis 2. dynamic_analysis 3. anti_debugging 4. unpacking 5. algorithm_recovery 6. key_recovery

## 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 初步分类 | file, strings, checksec | ✓ | 300s |
| 2 | 壳检测 | upx, peid, detect-it-easy | ✗ | 600s |
| 3 | 静态反汇编 | ghidra, ida, radare2 | ✓ | 2400s |
| 4 | 动态分析 | gdb-peda, ltrace, strace | ✗ | 1800s |
| 5 | 算法识别 | manual | ✗ | 1200s |
| 6 | 密钥提取 | manual | ✗ | 900s |
| 7 | 解实现 | python, custom | ✗ | 1200s |
| 8 | flag | manual | ✗ | 300s |

## 回退
dynamic_analysis_focus / anti_analysis_bypass / library_analysis / algorithm_identification / patch_analysis

## 验证
algorithm_accuracy / key_extraction / solution_testing / flag_generation
