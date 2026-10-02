#!/usr/bin/env bash
# HexStrike skill 包 — 引导函数库
#
# 用法（每个任务开始时执行一次）：
#   source /path/to/hexstrike-skills/scripts/hx.sh
#
# 依赖 $RUN / $FINDINGS / $HX_ROOT（由 basics/environment.md 的引导块设置）。
# 本文件只定义函数，不产生副作用。

# ── findings.tsv 记录 ───────────────────────────────────────────────────────
# 字段: sev  kind  title  target  tool  evidence
# evidence 里的制表符/换行会被替换，避免破坏列结构（截断到 500 字符）
add_finding() {
  if [ $# -ne 6 ]; then
    echo "usage: add_finding <sev> <kind> <title> <target> <tool> <evidence>" >&2
    return 2
  fi
  local ev
  ev=$(printf '%s' "$6" | tr '\t\n' '  ' | cut -c1-500)
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" "$ev" >> "$FINDINGS"
}

# 按 sev/kind/title/target 四列去重（就地覆盖）
dedupe_findings() {
  [ -f "$FINDINGS" ] || return 0
  sort -u -t$'\t' -k1,4 "$FINDINGS" -o "$FINDINGS"
}

# ── 错误分类 ────────────────────────────────────────────────────────────────
# $1 = stderr + exit code 文本；输出 ErrorType（见 recovery/recovery-engine.md）
#
# 顺序重要：TARGET_UNREACHABLE 必须排在 TOOL_NOT_FOUND 之前，
# 否则 "host not found" 会被 *"not found"* 抢先匹配成 TOOL_NOT_FOUND。
classify() {
  case "$1" in
    *timeout*|*"timed out"*|*"exit=124"*)                 echo TIMEOUT;;
    *"permission denied"*|*"access denied"*|*forbidden*)  echo PERMISSION_DENIED;;
    *"no route to host"*|*"connection refused"*|*"connection reset"*) echo NETWORK_UNREACHABLE;;
    *"rate limit"*|*"too many requests"*|*429*)            echo RATE_LIMITED;;
    *"host not found"*|*"target unreachable"*|*"name or service not known"*|*"could not resolve"*|*"temporary failure in name resolution"*) echo TARGET_UNREACHABLE;;
    *"command not found"*|*"not found"*)                   echo TOOL_NOT_FOUND;;
    *"invalid option"*|*"invalid argument"*)               echo INVALID_PARAMETERS;;
    *"no space left"*|*"out of memory"*)                   echo RESOURCE_EXHAUSTED;;
    *"authentication failed"*|*unauthorized*)              echo AUTHENTICATION_FAILED;;
    *"parse error"*|*"invalid json"*|*malformed*)          echo PARSING_ERROR;;
    *)                                                     echo UNKNOWN;;
  esac
}

# ── HTTP 测试辅助 ───────────────────────────────────────────────────────────
# Match/Replace 规则：rule <input> <sed-expr>
rule() { printf '%s' "$1" | sed -E "$2"; }

# Scope 校验：in_scope <url>（需先 export SCOPE=target.com）
in_scope() {
  [ -n "${SCOPE:-}" ] || { echo "SCOPE 未设置" >&2; return 2; }
  case "$1" in
    *"://$SCOPE"*|*".$SCOPE"*) return 0;;
    *)                         return 1;;
  esac
}

# ── 自检 ────────────────────────────────────────────────────────────────────
hx_selftest() {
  local ok=0
  [ -n "${RUN:-}" ] && echo "RUN=$RUN" || { echo "RUN 未设置" >&2; ok=1; }
  [ -n "${FINDINGS:-}" ] && echo "FINDINGS=$FINDINGS" || { echo "FINDINGS 未设置" >&2; ok=1; }
  for f in add_finding dedupe_findings classify rule in_scope; do
    command -v "$f" >/dev/null 2>&1 && echo "  ok  $f" || { echo "  MISSING $f" >&2; ok=1; }
  done
  return $ok
}

# 若被直接执行（而非 source），跑自检
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  hx_selftest
fi
