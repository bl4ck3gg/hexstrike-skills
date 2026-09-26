---
name: trivy
category: 容器安全
description: 容器/FS 扫描
when_to_use: 需要执行 trivy 时
---
# trivy
**类别**: 容器安全
**用途**: 容器/FS 扫描

**底层命令行**:
```bash
trivy <scan_type:image> <target> --format json [--severity HIGH,CRITICAL]
```

失败时参考 ../recovery/tool-alternatives.md
