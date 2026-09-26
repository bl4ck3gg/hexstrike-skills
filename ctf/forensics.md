---
name: ctf-forensics
when_to_use: CTF Forensics
---
# CTF Forensics 策略
1. file_carving 2. metadata_analysis 3. steganography 4. memory_analysis 5. network_analysis 6. timeline_analysis

## 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 证据采集 | file, exiftool | ✗ | 300s |
| 2 | 文件分析 | binwalk, foremost, strings | ✓ | 900s |
| 3 | 元数据 | exiftool, steghide | ✓ | 600s |
| 4 | 隐写检测 | stegsolve, zsteg, outguess | ✓ | 1200s |
| 5 | 内存分析 | volatility, volatility3 | ✗ | 1800s |
| 6 | 网络分析 | wireshark, tcpdump | ✗ | 1200s |
| 7 | 时间线 | manual | ✗ | 900s |
| 8 | 关联 | manual | ✗ | 600s |

## 回退
alternative_tools / manual_hex_analysis / correlation_analysis / timeline_reconstruction / deleted_data_recovery

## 验证
data_integrity / timeline_accuracy / evidence_correlation / flag_location
