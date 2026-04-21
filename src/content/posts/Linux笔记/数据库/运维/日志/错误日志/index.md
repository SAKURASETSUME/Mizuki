---
title: "Linux笔记 - 数据库 - 运维 - 日志 - 错误日志"
category: "Linux笔记"
date: 2026-04-21
published: 2026-04-21
author: "Rin"
---

错误日志是MySQL中最重要的日志之一 它记录了当mysqld启动和停止时，以及服务器在运行过程中发生任何严重错误时的相关信息。当数据库出现任何故障导致无法正常使用时，建议首先查看此日志。
该日志是默认开启的，默认存放目录/var/log/，默认的日志文件名为mysqld.log。查看日志位置：
```mysql
show variables like "%log_error%";
```

```bash
#查看日志
tail /var/log/mysql.log

#实时查看
tail -f /var/log/mysql.log
```