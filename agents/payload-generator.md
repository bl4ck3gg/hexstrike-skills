---
name: agent-payload-generator
description: 载荷生成规则（模板见 payloads/*）
when_to_use: 针对具体上下文生成载荷
---
# 载荷生成器

按攻击类型与复杂度生成载荷，并给出测试用例。

## 生成规则
```
输入: attack_type ∈ {xss,sqli,lfi,cmd_injection,ssti,xxe}
      complexity  ∈ {basic,advanced,bypass}   (sqli 另有 time_based)
      technology  (来自 parsed/tech.json)
1. payloads = payload_templates[attack_type][complexity]
   缺失 complexity -> 回退 basic；attack_type 未知 -> 单条占位注释
2. 上下文增强，每条载荷产出两个变体:
   {"payload": 原样,   "encoding":"none"}
   {"payload": URL编码, "encoding":"url"}
   URL 编码仅替换三种字符: " "->%20  "<"->%3C  ">"->%3E
3. test_cases = 前 5 条: method = GET if len(payload)<100 else POST
4. risk_level: 含 system|exec|eval|cmd|shell|passwd|etc -> HIGH
               含 script|alert|union|select          -> MEDIUM
               否则                                  -> LOW
5. recommendations: 按 attack_type 的固定建议
```
载荷本体见 `payloads/xss.md|sqli.md|lfi.md|cmd-injection.md|ssti.md|xxe.md`。
URL 编码变体一行生成：
```bash
printf '%s' "$PAYLOAD" | sed 's/ /%20/g; s/</%3C/g; s/>/%3E/g'
```

## 攻击套件（多类型一次生成）
对 `attack_types`（如 `xss,sqli,lfi`）里每个类型按上面的规则各生成一套，
汇总 `total_payloads / high_risk_payloads / test_cases`（对应 `ai_generate_attack_suite`）：
```bash
SKILLS='<skill 包根目录>'   # 本文件所在包的根，如 b/skills
TARGET_URL='<url>'
: > $RUN/parsed/attack_suite.tsv
for t in xss sqli lfi cmd-injection ssti xxe; do
  # 取 payloads/<类型>.md 的全部载荷行（跳过 frontmatter 与标题）
  awk 'BEGIN{fm=0} /^---$/{fm++;next} fm<2{next} /^#/{next} NF{print}' "$SKILLS/payloads/$t.md" |
  while IFS= read -r p; do
    case "$p" in *system*|*exec*|*eval*|*cmd*|*shell*|*passwd*|*etc*) risk=HIGH;;
                   *script*|*alert*|*union*|*select*)              risk=MEDIUM;;
                   *)                                               risk=LOW;; esac
    printf '%s\t%s\t%s\n' "$t" "$risk" "$p" >> $RUN/parsed/attack_suite.tsv
  done
done
awk -F'\t' '{n++; if($2=="HIGH")h++} END{printf "total_payloads=%d high_risk_payloads=%d\n",n,h}' \
  $RUN/parsed/attack_suite.tsv
```
产物：`parsed/attack_suite.tsv`（type/risk/payload）+ 顶部 totals；
`test_cases` 取每类型前 5 条，用 `http/framework.md` 实测（未实测不记 finding）。

## 二进制载荷文件（buffer / cyclic / random）
见 `payloads/file-generation.md`（含 pwntools cyclic 与 offset 反查）。

## 按 CVE 生成 exploit
见 `vuln-intel/exploit-generate.md`（分类 → 模板 → 规避 → 说明）。

## 验证载荷
生成后必须实测：用 `http/framework.md` 的 repeater/intruder 发送，
按响应判定（反射/报错/时间差）。未实测的载荷不得写成 finding。
