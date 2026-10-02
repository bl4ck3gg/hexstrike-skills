---
name: reporting
description: 报告与可视化交付
when_to_use: 阶段结束或需要交付人类
---
# 报告交付

## 扫描摘要
```bash
dedupe_findings
{
  echo "# Scan Summary — $TARGET"; echo
  echo "- run: \`$HX_RUN_ID\`"
  echo "- duration: $(( $(date +%s) - $(stat -c %Y $RUN/meta.txt) ))s"
  echo "- commands: $(ls $RUN/raw | wc -l)"
  echo "- findings: $(wc -l < $FINDINGS 2>/dev/null || echo 0)"
  echo; echo "| severity | count |"; echo "|---|---|"
  for s in critical high medium low info; do
    printf '| %s | %s |\n' "$s" "$(awk -F'\t' -v s=$s '$1==s' $FINDINGS 2>/dev/null | wc -l)"
  done
  echo; echo "## Findings"; echo "| sev | kind | title | target |"; echo "|---|---|---|---|"
  sort -t$'\t' -k1,1r $FINDINGS | awk -F'\t' '{printf "| %s | %s | %s | %s |\n",$1,$2,$3,$4}'
} > $RUN/report/scan-summary.md
```

## 漏洞报告（md + html）
```bash
{
  echo "# Vulnerability Report — $TARGET"; echo
  echo "Generated $(date -u +%FT%TZ) | run \`$HX_RUN_ID\`"; echo
  for s in critical high medium low info; do
    n=$(awk -F'\t' -v s=$s '$1==s' $FINDINGS | wc -l); [ "$n" -gt 0 ] || continue
    echo "## $s ($n)"; echo
    awk -F'\t' -v s=$s '$1==s{printf "### %s\n- target: %s\n- tool: %s\n- kind: %s\n\n```\n%s\n```\n\n",$3,$4,$5,$2,$6}' $FINDINGS
  done
} > $RUN/report/vulnerability-report.md

python3 "$SKILLS/scripts/report_html.py" "$FINDINGS" "$TARGET" "$HX_RUN_ID" > $RUN/report/vulnerability-report.html
```

## 工具输出美化（20 行窗口 + 分类标记）
```bash
sed -n '1,20p' $RUN/raw/<x>.log | awk '
  /error|failed|denied/        {printf "│ [!] %s\n", substr($0,1,75); next}
  /found|discovered|vulnerable/{printf "│ [+] %s\n", substr($0,1,75); next}
  /warning|timeout/            {printf "│ [~] %s\n", substr($0,1,75); next}
  {printf "│ [ ] %s\n", substr($0,1,75)}' > $RUN/report/tool-output-<x>.md
```

## 交付
报告都是 `$RUN/report/` 下的普通文件：文本直接读取，HTML/截图走文件下载。
不要让大文件经过终端输出（会被截断/转义）。

## 产物对应
| 能力 | 产物 |
|---|---|
| 扫描摘要 | scan-summary.md |
| 漏洞报告 | vulnerability-report.md/.html（同卡片语义） |
| 工具输出美化 | tool-output-*.md |
| 系统指标 / 仪表盘 | `basics/state.md` 的 dashboard 快照 |
原则：每条 finding 必须可复现（URL/参数/证据）；未验证的猜测记 info；
降级运行（无浏览器/工具缺失）必须在报告开头注明。
