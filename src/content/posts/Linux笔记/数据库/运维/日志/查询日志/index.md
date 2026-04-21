---
title: "Linux笔记 - 数据库 - 运维 - 日志 - 查询日志"
category: "Linux笔记"
date: 2026-04-21
published: 2026-04-21
author: "Rin"
---

查询日志中记录了客户端的所有操作语句，而二进制日志不包含查询数据的SQL语句。默认情况下，查询日志是未开启的。如果需要开启查询日志，可以设置以下配置：
```mysql
show variables like "%general%";
```

开启查询日志
```bash
#进入配置文件
vim /etc/my.cnf 

#添加
#开启查询日志 0或1
general_log=1
#设置日志的文件名 不指定则默认为host_name.log
general_log_file=/var/lib/mysql/mysql_query.log
#重启服务
systemctl restart mysqld
```