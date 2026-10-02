# HexStrike AI — Skill 版

这是 [HexStrike AI](https://github.com/0x4m4/hexstrike-ai) 的 skill 版本：一套自成体系的攻防技能包。
从目标判断、工具选择、参数决策，到漏洞验证、情报利用与报告交付，
全部以可直接执行的命令块与判定规则给出。

## 目录

| 目录 | 内容 |
|---|---|
| `basics/` | 环境检查、记录约定（findings.tsv）、长任务/并发、运行状态 |
| `intelligence/` | 目标类型、工具有效性、攻击剧本、打分算法、技术指纹 |
| `workflows/` | 15 个基础剧本 + `smart-scan`、`http-testing` |
| `tools/` | 91 个 CLI 工具 + 无 CLI 等价物的配方（api/graphql/jwt/schema/browser/http/burp） |
| `api-security/` `http/` `browser/` | API 端点发现、GraphQL、JWT、Schema 审计、HTTP 手工测试、浏览器检查的判定规则与配方 |
| `vuln-intel/` | CVE 监控、exploit 检索/生成、攻击链、零日、威胁情报、威胁狩猎 |
| `reporting/` | 扫描摘要、漏洞报告（md+html）、工具输出美化、dashboard |
| `recovery/` `optimization/` `agents/` | 错误恢复策略、参数优化、编排流程 |
| `ctf/` `bugbounty/` `payloads/` | 知识域（`ctf/strategy-matrix.md` 是策略/工具选择入口） |
| `scripts/` | 跨 shell 函数与 >20 行的程序（`hx.sh`、报告、解析、探测） |

## 使用约定

1. **先定记录位置**：原始输出存 `raw/`，发现记 `parsed/findings.tsv`（制表符分隔：
   `sev kind title target tool evidence`），报告只读它 —— 输出丢了也能恢复。
2. **引导块先 source**：`source "$SKILLS/scripts/hx.sh"` 拿到 `add_finding` 等跨 shell 函数；
   其余命令块可直接粘贴运行，无需先落成脚本文件。
3. **每条发现必须可复现**：URL/参数/payload/证据齐全；未验证的猜测记 `info`。

最小引导块见 `basics/environment.md`。
