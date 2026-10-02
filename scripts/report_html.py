#!/usr/bin/env python3
"""findings.tsv -> HTML 漏洞报告

用法:
    report_html.py <findings.tsv> <target> [run_id] > report.html

findings.tsv 为制表符分隔，6 列:
    sev  kind  title  target  tool  evidence
"""
import datetime
import html
import sys

COLOR = {
    "critical": "#d11",
    "high": "#e3401f",
    "medium": "#e07b1a",
    "low": "#c9a227",
    "info": "#2b8fd1",
}

STYLE = """body{background:#0d0f12;color:#e6e6e6;font-family:monospace;padding:32px}
h1{color:#ff3b30}.card{background:#14181d;border-radius:8px;padding:16px;margin:12px 0}
.badge{color:#fff;padding:2px 8px;border-radius:4px;font-size:12px}
.meta{color:#9aa4b2;font-size:12px}pre{background:#0a0c0f;padding:10px;border-radius:6px;overflow:auto}"""


def render(findings_path: str, target: str, run: str) -> str:
    rows = []
    try:
        with open(findings_path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) < 6:
                    continue
                sev, kind, title, tgt, tool, ev = f[:6]
                c = COLOR.get(sev, "#888")
                rows.append(
                    f'<div class="card" style="border-left:6px solid {c}">'
                    f'<span class="badge" style="background:{c}">{html.escape(sev.upper())}</span>'
                    f"<h3>{html.escape(title)}</h3>"
                    f'<p class="meta">{html.escape(tgt)} | {html.escape(tool)} | {html.escape(kind)}</p>'
                    f"<pre>{html.escape(ev)}</pre></div>"
                )
    except FileNotFoundError:
        pass

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = "".join(rows) or "<p>No findings.</p>"
    return (
        f'<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<title>Report {html.escape(target)}</title>"
        f"<style>{STYLE}</style></head><body>"
        f"<h1>Vulnerability Report</h1>"
        f'<p class="meta">{html.escape(target)} | run {html.escape(run)} | {ts}</p>'
        f"{body}</body></html>"
    )


def main(argv: list) -> int:
    if len(argv) < 3 or argv[1] in ("-h", "--help"):
        print(__doc__.strip(), file=sys.stderr if len(argv) > 1 else sys.stdout)
        return 0 if len(argv) > 1 else 2
    findings, target = argv[1], argv[2]
    run = argv[3] if len(argv) > 3 else "-"
    print(render(findings, target, run))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
