---
name: ctf-misc
when_to_use: CTF Misc
---
# CTF Misc 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 挑战分析 | manual | ✗ | 300s |
| 2 | 编码检测 | base64, hex, rot13 | ✓ | 600s |
| 3 | 格式识别 | file, binwalk | ✗ | 300s |
| 4 | 专项分析 | qr-decoder, audio-analysis | ✓ | 900s |
| 5 | 模式识别 | manual | ✗ | 600s |
| 6 | 解实现 | python, custom | ✗ | 900s |
| 7 | 验证 | manual | ✗ | 300s |

## 回退
alternative_interpretations / encoding_combinations / esoteric_approaches / metadata_focus / collaborative_solving
