---
name: gdb-peda
category: 二进制调试
description: GDB+PEDA
when_to_use: 需要执行 gdb-peda 时
---
# gdb-peda
**类别**: 二进制调试
**用途**: GDB+PEDA

**底层命令行**:
```bash
gdb -q <binary> -ex 'source ~/peda/peda.py' -ex '<cmd>' -ex 'quit'
```

失败时参考 ../recovery/tool-alternatives.md
