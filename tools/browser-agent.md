---
name: browser-agent
category: 浏览器代理
description: JS 渲染后的页面检查（chromium 单命令优先）
when_to_use: 需要渲染后 DOM、storage、console、network
---
**配方**: `browser/inspection.md`

```bash
chromium --headless --no-sandbox --disable-gpu --virtual-time-budget=5000 \
  --dump-dom '<url>' > dom.html                       # 渲染后 DOM（零代码）
chromium --headless --no-sandbox --disable-gpu \
  --screenshot=page.png --window-size=1920,1080 '<url>'
command -v katana >/dev/null && katana -u '<url>' -headless -d 2 -jc -o urls.txt
```
需要 localStorage/console/network 时，用 `browser/inspection.md` 里的 ~15 行片段。
