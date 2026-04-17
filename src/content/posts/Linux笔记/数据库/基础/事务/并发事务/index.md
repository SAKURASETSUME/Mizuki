---
title: "Linux笔记 - 数据库 - 基础 - 事务 - 并发事务"
category: "Linux笔记"
date: 2026-04-17
published: 2026-04-17
author: "Rin"
---

## 并发事务问题

| 问题    | 描述                                                    |
| ----- | ----------------------------------------------------- |
| 脏读    | 一个事务读到另一个事务还没提交的数据                                    |
| 不可重复读 | 一个事务先后读取同一条记录 但两次读取的数据不同 称之为不可重复读                     |
| 幻读    | 一个事务按照条件查询数据时 没有对应的数据行 但是在插入数据时 又发现这行数据已经存在 好像出现了"幻影" |

## 事务的隔离级别

| 隔离级别                | 脏读  | 不可重复读 | 幻读  |
| ------------------- | --- | ----- | --- |
| Read uncommitted    | √   | √     | √   |
| Read committed      | ×   | √     | √   |
| Repeatable Read(默认) | ×   | ×     | √   |
| Serializable        | ×   | ×     | ×   |
```mysql
#查看事务隔离级别
select @@transaction_isolation;

#设置事务隔离级别
set [session | global] transaction isolation level [read uncommitted | read committed | repeatable read | serializable];
```