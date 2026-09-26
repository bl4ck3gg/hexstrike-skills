---
name: rustscan
category: 网络侦察
description: 超高速端口发现
when_to_use: 需要执行 rustscan 时
---
# rustscan
**类别**: 网络侦察
**用途**: 超高速端口发现

**底层命令行**:
```bash
rustscan -a <target> --ulimit 5000 -b 4500 -t 1500 [-p <ports>] [-- -sC -sV]
```

失败时参考 ../recovery/tool-alternatives.md
