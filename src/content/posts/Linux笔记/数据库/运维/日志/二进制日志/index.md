---
title: "Linux笔记 - 数据库 - 运维 - 日志 - 二进制日志"
category: "Linux笔记"
date: 2026-04-21
published: 2026-04-21
author: "Rin"
---

## 介绍
二进制日志（BINLOG）记录了所有的DDL（数据定义语言）语句和DML（数据操纵语言）语句，但不包括数据查询（SELECT、SHOW）语句。

## 作用

- 灾难时的数据恢复
- MySQL的主从复制 在MySQL8.0版本中 默认二进制是开启着的 涉及到的参数如下：
```mysql
show variables like "%log_bin%";
```

## 二进制日志的格式
MySQL服务器中提供了多种格式来记录二进制日志 具体格式及特点如下：

| 日志格式      | 含义                                                     |
| --------- | ------------------------------------------------------ |
| STATEMENT | 基于SQL语句的日志记录 记录的是SQL语句 对数据进行修改的SQL都会记录在日志文件中           |
| ROW       | 基于行的日志记录 记录的是每一行的数据变更(默认)                              |
| MIXED     | 混合了STATEMENT和ROW两种模式 默认采用STATEMENT 在某些情况下会自动切换为ROW进行记录 |
```mysql
show variables like "%binlog_format%";
```

## 修改二进制日志的格式
```bash
vim /etc/my.cnf

#写入
binlog_format=STATEMENT
#重启服务
systemctl restart mysqld
```

## 查看二进制日志
通过二进制日志查询工具mysqlbinlog来查看
```bash
mysqlbinlog [参数选项] logfilename

-d 指定数据库名称 只列出指定的数据库相关操作
-o 忽略日志中前n行命令
-v 将行事件(数据变更)重构为SQL语句
-vv 将行事件(数据变更)重构为SQL语句 并输出注释信息

#查看
mysqlbinlog -d studty -vv /var/log/lib/mysql/binlog.000006
```

## 日志删除
对于比较繁忙的业务系统 每天生成的binlog数据巨大 如果长时间不清除 将会占用大量磁盘空间 可以通过以下几种方法清理日志
```mysql
#删除全部binlog日志 删除之后 日志编号 将从bin.000001重新开始
reset master
#删除******编号之前的所有日志
purge master logs to "binlog.******"
#删除日志为"yyyy-mm-dd hh24:mi:ss"之前产生的所有日志
purge master logs before 'yyyy-mm-dd hh24:mi:ss'
```

或者你可以在mysql的配置文件中配置二进制日志的过期时间 设置了之后 二进制日志过期将会自动删除
```mysql
show variables like '%binlog_expire%';
```