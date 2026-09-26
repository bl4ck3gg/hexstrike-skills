---
name: burpsuite
category: 综合 Web
description: Burp Suite 真实扫描（headless CLI / 内置 REST API）
when_to_use: 环境有 Burp Professional 且需要其扫描器与报告
---
# burpsuite

**注意**：MCP 工具 `burpsuite_scan` 提交到 `/api/tools/burpsuite`，而当前
`hexstrike_server.py` **没有这条路由**（只有 `/api/tools/burpsuite-alternative`），
所以该 MCP 工具不可用。要跑真 Burp 走本文件；没有 Burp 就用
`tools/burpsuite-alternative.md`（http/framework.md + browser/inspection.md）。

## 前置
```bash
command -v java || echo "缺 java"
ls /opt/burpsuite/burpsuite_pro.jar 2>/dev/null || echo "自备 Burp Professional jar（Community 无扫描器/REST API）"
```

## 1) REST API 模式（推荐，可脚本化）
```bash
cat > $RUN/artifacts/burp-rest.json <<'JSON'
{
  "rest_api_config": {
    "enabled": true,
    "port": 1337,
    "address": "127.0.0.1",
    "api_keys": ["hexstrike-local-key"]
  }
}
JSON

java -jar /opt/burpsuite/burpsuite_pro.jar --headless \
  --config-file=$RUN/artifacts/burp-rest.json \
  --project-file=$RUN/artifacts/burp.burp \
  > $RUN/raw/burp_server.log 2>&1 &
echo $! > $RUN/raw/burp.pid
sleep 10; curl -sS http://127.0.0.1:1337/v0.1/scan -H 'Authorization: hexstrike-local-key' || true

BURP=http://127.0.0.1:1337/v0.1; KEY=hexstrike-local-key

# 建扫描
curl -sS -X POST "$BURP/scan" -H "Authorization: $KEY" -H 'Content-Type: application/json' \
  -d '{"urls":["<https://target>"],"scan_configurations":[{"name":"Crawl strategy - fastest"}]}' \
  | tee $RUN/raw/burp_scan.json
TASK=$(jq -r '.task_id // .id' $RUN/raw/burp_scan.json)

# 轮询状态（succeeded/failed/paused）
while :; do
  curl -sS "$BURP/scan/$TASK" -H "Authorization: $KEY" | tee $RUN/raw/burp_status.json | jq -r '.scan_status'
  grep -q succeeded $RUN/raw/burp_status.json && break
  sleep 30
done

# 取报告（HTML/XML）
curl -sS -X POST "$BURP/scan/$TASK/report" -H "Authorization: $KEY" -H 'Content-Type: application/json' \
  -d '{"report_type":"HTML"}' -o $RUN/report/burp.html
# 取消扫描
# curl -sS -X DELETE "$BURP/scan/$TASK" -H "Authorization: $KEY"
```
API 细节以本机 Burp 版本的 `/v0.1` 文档为准（版本间字段略有差异）。

## 2) headless 纯 CLI（无 REST）
Burp 没有"直接指定目标扫描"的官方命令行开关；无 REST 时用
`--config-file` 载入预置的 target scope + scan launcher 配置后启动：
```bash
java -jar /opt/burpsuite/burpsuite_pro.jar --headless \
  --config-file=$RUN/artifacts/burp-scan-config.json \
  --project-file=$RUN/artifacts/burp.burp > $RUN/raw/burp_cli.log 2>&1
```
扫描结果从 project 文件导出（GUI 或 REST report）。

## 3) 结果解析入 findings
```bash
jq -r '.issue_events[]? | [.issue.severity, .issue.name, .issue.path, (.issue.origin // "")] | @tsv' \
  $RUN/raw/burp_status.json > $RUN/parsed/burp_issues.tsv
while IFS=$'\t' read -r sev name path origin; do
  case "$sev" in
    high) s=high;; medium) s=medium;; low) s=low;; *) s=info;;
  esac
  add_finding "$s" burp "$name" "$path" burpsuite "$origin"
done < $RUN/parsed/burp_issues.tsv
```
severity 映射：`high→high / medium→medium / low→low / information→info`。

## 失败回退
无 Burp / 无许可 / REST 起不来 → `tools/burpsuite-alternative.md`：
`http/framework.md`（repeater/intruder/spider）+ `browser/inspection.md`，
覆盖手工测试面；替代映射见 `recovery/tool-alternatives.md`。
