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

python3 - "$FINDINGS" "$TARGET" "$HX_RUN_ID" > $RUN/report/vulnerability-report.html <<'PY'
import html, sys, datetime
findings, target, run = sys.argv[1], sys.argv[2], sys.argv[3]
color = {"critical":"#d11","high":"#e3401f","medium":"#e07b1a","low":"#c9a227","info":"#2b8fd1"}
rows = []
try:
    for line in open(findings):
        f = line.rstrip("\n").split("\t")
        if len(f) < 6: continue
        sev, kind, title, tgt, tool, ev = f[:6]
        c = color.get(sev, "#888")
        rows.append(f'<div class="card" style="border-left:6px solid {c}">'
                    f'<span class="badge" style="background:{c}">{html.escape(sev.upper())}</span>'
                    f'<h3>{html.escape(title)}</h3>'
                    f'<p class="meta">{html.escape(tgt)} | {html.escape(tool)} | {html.escape(kind)}</p>'
                    f'<pre>{html.escape(ev)}</pre></div>')
except FileNotFoundError:
    pass
print(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Report {html.escape(target)}</title>
<style>body{{background:#0d0f12;color:#e6e6e6;font-family:monospace;padding:32px}}
h1{{color:#ff3b30}}.card{{background:#14181d;border-radius:8px;padding:16px;margin:12px 0}}
.badge{{color:#fff;padding:2px 8px;border-radius:4px;font-size:12px}}
.meta{{color:#9aa4b2;font-size:12px}}pre{{background:#0a0c0f;padding:10px;border-radius:6px;overflow:auto}}</style>
</head><body><h1>Vulnerability Report</h1>
<p class="meta">{html.escape(target)} | run {html.escape(run)} | {datetime.datetime.utcnow().isoformat()}Z</p>
{''.join(rows) or '<p>No findings.</p>'}</body></html>""")
PY
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
