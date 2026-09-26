---
name: intel-dashboard
description: 情报仪表盘（markdown 快照）
when_to_use: 向人类汇报情报汇总
---
# 情报仪表盘

```bash
{
  echo "# Vulnerability Intelligence Dashboard"; echo
  echo "run: $HX_RUN_ID  |  $(date -u +%FT%TZ)"; echo
  echo "## Findings"; echo "| severity | count |"; echo "|---|---|"
  for s in critical high medium low info; do
    printf '| %s | %s |\n' "$s" "$(awk -F'\t' -v s=$s '$1==s' $FINDINGS 2>/dev/null | wc -l)"
  done
  echo; echo "## Recent CVEs"; echo "| CVE | CVSS | Sev | Description |"; echo "|---|---|---|---|"
  [ -f $RUN/parsed/cve_monitor.tsv ] && awk -F'\t' '{printf "| %s | %s | %s | %s |\n",$1,$2,$3,$4}' $RUN/parsed/cve_monitor.tsv | head -20
  echo; echo "## Threat feeds"
  [ -f $RUN/parsed/kev_recent.tsv ] && echo "KEV(30d): $(wc -l < $RUN/parsed/kev_recent.tsv) 条"
  [ -f $RUN/parsed/epss_top.tsv ] && { echo; echo "| CVE | EPSS | pct |"; echo "|---|---|---|"; awk -F'\t' '{printf "| %s | %s | %s |\n",$1,$2,$3}' $RUN/parsed/epss_top.tsv; }
} > $RUN/report/intel-dashboard.md
wc -l $RUN/report/intel-dashboard.md
```
仪表盘是按需重生成的 markdown 快照，重跑即刷新。
