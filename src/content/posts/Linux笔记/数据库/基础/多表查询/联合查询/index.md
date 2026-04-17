---
title: "Linux笔记 - 数据库 - 基础 - 多表查询 - 联合查询"
category: "Linux笔记"
date: 2026-04-17
published: 2026-04-17
author: "Rin"
---

对于union查询，就是把多次查询的结果合并起来，形成一个新的查询结果集。
```mysql
#语法
select 字段列表 from 表A ... union [all] select 字段列表 from 表B ...;
```

ps:
联合查询的多张表列数必须保持一致 字段类型也需要保持一致