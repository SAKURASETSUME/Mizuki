---
title: "Linux笔记 - 数据库 - 运维 - 日志 - 慢查询日志"
category: "Linux笔记"
date: 2026-04-21
published: 2026-04-21
author: "Rin"
---

慢查询日志记录了所有执行时间超过参数long_query_time设置值并且扫描记录数不小于min_examined_row_limit的所有的SQL语句的日志，默认未开启。long_query_time 默认为10秒，最小为0，精度可以到微秒。

开启慢查询日志
```bash
vim /etc/my.cnf
#慢查询日志
slow_query_log=1
#执行时间参数
long_query_time=2
#重启
systemctl restart mysqld
```

默认情况下 不会记录管理语句 也不会记录不使用索引进行查找的查询 可以使用log_slow_admin_statements和更改此行为log_queries_not_using_indexes
```bash
#记录执行较慢的管理语句
log_slow_admin_statements=1
#记录执行较慢的未使用索引的语句
log_queries_not_using_indexes=1
```