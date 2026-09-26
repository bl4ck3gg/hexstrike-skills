---
name: zero-day-research
description: 零日研究流程配方（研究领域 + 检查清单）
when_to_use: 无公开 CVE，需自主审计目标软件
---
# 零日研究流程

## 研究领域
```
通用: Input validation / Memory corruption / Authentication bypasses / Authorization flaws
      / Cryptographic weaknesses / Race conditions / Logic flaws
Web 追加: XSS / SQLi / SSRF / Insecure deserialization / Template injection
系统追加: Buffer overflows / Privilege escalation / Kernel / Service exploitation / Configuration
判定: 名称含 apache|nginx|tomcat|php|node|django -> Web 组
      含 windows|linux|kernel|driver -> 系统组
depth: quick(2 项) | standard(5 项) | comprehensive(全部)
```

## 可执行清单
```
recon     版本确认(headers/文件哈希/banner) -> 暴露面 -> 公开补丁 diff
code      定位 parser/deserializer 入口 -> 追踪不可信输入到 sink -> 检查鉴权分支
dynamic   ffuf/dalfox/radamsa 模糊输入 -> 对比补丁前后行为 -> 监控崩溃/ASAN
validate  第二实例复现 -> 最小化触发器 -> CVSS 向量评估
```
```bash
# 版本确认
curl -sSk -D - -o /dev/null '<url>' | grep -iE '^(server|x-powered-by)'
# 补丁 diff（以 nginx 为例）
git clone --depth 200 https://github.com/nginx/nginx /tmp/nginx-src 2>/dev/null && \
  git -C /tmp/nginx-src log --oneline -30 --grep='fix\|security' -i
# 模糊
ffuf -u '<url>/FUZZ' -w /usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt -mc all -fs 0 -t 20
```

## 优先级建议
1. **先做 1-day**：diff 上游已修但目标未修的补丁（成本最低、命中率最高）
2. 再查同类组件历史 CVE 模式（如 nginx resolver / HTTP2 解析）
3. 最后才无引导 fuzz；崩溃必须能 gdb/ASAN 复现才计入发现
