---
name: threat-feeds
description: 威胁情报关联配方（KEV + EPSS + NVD）
when_to_use: 判断"哪些漏洞正在被利用"
---
# 威胁情报关联

```bash
# 1) CISA KEV：近 30 天新增的在野利用
curl -sS 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json' \
  -o $RUN/raw/kev.json
jq -r --arg d "$(date -u -d '-30 days' +%Y-%m-%d)" \
  '.vulnerabilities[] | select(.dateAdded >= $d) | [.cveID, .vulnerabilityName, .dateAdded] | @tsv' \
  $RUN/raw/kev.json | sort -k3 -r | tee $RUN/parsed/kev_recent.tsv

# 2) EPSS：30 天内被利用概率（可批量，逗号分隔 CVE）
IDS=$(cut -f1 $RUN/parsed/cve_monitor.tsv 2>/dev/null | head -50 | paste -sd,)
[ -n "$IDS" ] && curl -sS "https://api.first.org/data/v1/epss?cve=$IDS" \
  | jq -r '.data | sort_by(.epss|tonumber) | reverse | .[:10][] | [.cve, .epss, .percentile] | @tsv' \
  | tee $RUN/parsed/epss_top.tsv
```

## 关联与记账
```bash
# epss > 0.5 -> high, 否则 medium
awk -F'\t' '{sev=($2+0>0.5)?"high":"medium"; print sev"\t"$1"\t"$2}' $RUN/parsed/epss_top.tsv \
| while IFS=$'\t' read -r sev cve epss; do add_finding "$sev" epss_high "$cve EPSS=$epss" "$TARGET" feeds ""; done

# 目标软件命中 KEV -> 置顶
jq -r '(.web_servers+.cms+.frameworks)[]?' $RUN/parsed/tech.json 2>/dev/null | while read -r t; do
  grep -i "$t" $RUN/parsed/kev_recent.tsv && echo "!! KEV match: $t"
done
```
命中 KEV 的优先级高于任何扫描器的泛泛输出。
