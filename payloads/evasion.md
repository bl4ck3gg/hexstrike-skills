---
name: payload-evasion
when_to_use: 绕过 WAF/AV
---
# 规避技巧
## 编码
url / base64 / hex / unicode
## 混淆
variable_renaming / string_splitting / comment_injection
## AV 规避
encryption / packing / metamorphism
## WAF 绕过
case_variation / parameter_pollution / header_manipulation

## 高级示例
Double URL: payload.replace("%","%25").replace(" ","%2520")
Unicode: "script" → "scr\u0131pt"
Case: "".join(c.upper() if i%2 else c.lower() for i,c in enumerate(payload))
Nation-State:
  Polyglot: /*{payload}*/ OR {payload}
  Time-delayed: setTimeout(function(){payload}, 1000)
  Env Keying: if(navigator.userAgent.includes('specific')){payload}
