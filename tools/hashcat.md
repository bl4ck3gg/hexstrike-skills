---
name: hashcat
category: 密码攻击
description: GPU 破解
when_to_use: 需要执行 hashcat 时
---
# hashcat
**类别**: 密码攻击
**用途**: GPU 破解

**底层命令行**:
```bash
hashcat -m <ht> -a <am:0> <hash_file> [<wl>|<mask>]
```

失败时参考 ../recovery/tool-alternatives.md
