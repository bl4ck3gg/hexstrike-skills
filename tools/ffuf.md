---
name: ffuf
category: Web模糊
description: 目录/参数模糊
when_to_use: 需要执行 ffuf 时
---
# ffuf
**类别**: Web模糊
**用途**: 目录/参数模糊

**底层命令行**:
```bash
ffuf -u <url>/FUZZ -w <wl> -mc <codes:200,204,301,302,307,401,403>
```

失败时参考 ../recovery/tool-alternatives.md
