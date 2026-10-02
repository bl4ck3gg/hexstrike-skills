#!/usr/bin/env python3
"""浏览器深度检查：storage / console / network / forms / scripts

用法:
    playwright_probe.py <url> [screenshot.png] [--json-out out.json]

依赖（仅本脚本需要，其余文档仍可零依赖运行）:
    pip3 install --break-system-packages playwright && python3 -m playwright install chromium

判定（见 browser/inspection.md）:
    storage key 含 password/token/secret/key -> high
    POST 表单无 csrf/token                   -> medium
    security_score = max(0, 100 - issues*5)
"""
import json
import sys

EVAL_JS = """() => {
  const s = x => { const o = {}; for (let i = 0; i < x.length; i++) {
    const k = x.key(i); o[k] = x.getItem(k); } return o; };
  return {
    title: document.title,
    url: location.href,
    cookie: document.cookie,
    local_storage: s(localStorage),
    session_storage: s(sessionStorage),
    forms: [...document.querySelectorAll('form')].map(f => ({
      action: f.action, method: f.method,
      inputs: [...f.querySelectorAll('input,textarea,select')].map(
        i => ({ name: i.name, type: i.type })) })),
    scripts: [...document.querySelectorAll('script')].map(s => s.src || 'inline')
  };
}"""

SENSITIVE = ("password", "token", "secret", "key")


def probe(url: str, shot: str) -> dict:
    from playwright.sync_api import sync_playwright  # 延迟导入，便于 --help

    with sync_playwright() as p:
        b = p.chromium.launch(
            headless=True, args=["--no-sandbox", "--ignore-certificate-errors"]
        )
        ctx = b.new_context(ignore_https_errors=True)
        pg = ctx.new_page()
        net, errs = [], []
        pg.on("request", lambda r: net.append(r.url))
        pg.on(
            "console",
            lambda m: errs.append({"type": m.type, "text": m.text})
            if m.type in ("error", "warning")
            else None,
        )
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(3000)
        out = pg.evaluate(EVAL_JS)
        out["network"] = net
        out["console"] = errs
        pg.screenshot(path=shot, full_page=True)
        b.close()
    return out


def assess(out: dict) -> dict:
    issues = []
    for store in ("local_storage", "session_storage"):
        for k in (out.get(store) or {}):
            if any(s in k.lower() for s in SENSITIVE):
                issues.append(f"high: {store} 含敏感 key '{k}'")
    for f in out.get("forms") or []:
        if (f.get("method") or "").lower() == "post":
            names = " ".join((i.get("name") or "").lower() for i in f.get("inputs") or [])
            if "csrf" not in names and "token" not in names:
                issues.append(f"medium: POST 表单无 csrf/token ({f.get('action')})")
    n_inline = sum(1 for s in out.get("scripts") or [] if s == "inline")
    if n_inline:
        issues.append(f"low: {n_inline} 个内联 script")
    for e in out.get("console") or []:
        if e.get("type") == "error":
            issues.append(f"low: console error: {e.get('text','')[:80]}")
    return {"issues": issues, "security_score": max(0, 100 - len(issues) * 5)}


def main(argv: list) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) > 1 else 2
    url = argv[1]
    shot = argv[2] if len(argv) > 2 and not argv[2].startswith("-") else "/tmp/hx_page.png"
    try:
        out = probe(url, shot)
    except ImportError:
        print("缺少 playwright：pip3 install --break-system-packages playwright "
              "&& python3 -m playwright install chromium", file=sys.stderr)
        return 3
    result = dict(out)
    result["assessment"] = assess(out)

    if "--json-out" in argv:
        dest = argv[argv.index("--json-out") + 1]
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, ensure_ascii=False)
        print(f"written: {dest}", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
