---
title: "Linux笔记 - 数据库 - 基础 - 数据查询语言-DQL - 查询"
category: "Linux笔记"
date: 2026-04-15
published: 2026-04-15
author: "Rin"
---

## 查询语句语法
```mysql
select 字段列表 from 表名列表 where 条件列表 group by 分组字段列表 having 分组后条件列表 order by 排序字段列表 limit 分页参数;
```

## 基本查询
```mysql
#查询多个字段
select 字段1,字段2,字段3... from 表名;
select * from 表名;

#设置别名
selcet 字段1 [as 别名1], 字段2[as 别名2], ... from 表名;

#去除重复记录
select distinct 字段列表 from 表名;
```

## 条件查询
```mysql
#语法
select 字段列表 from 表名 where 条件列表;
```

where条件列表可以用的功能

| 运算符           | 功能                      |
| ------------- | ----------------------- |
| >             |                         |
| >=            |                         |
| <             |                         |
| <=            |                         |
| =             |                         |
| <>或!=         |                         |
| between...and | 在某个范围之内                 |
| in(...)       | 在in之后的列表中的值 多选一         |
| like 占位符      | 模糊匹配(\_匹配单个字符 %匹配任意个字符) |
| is null       | 为空                      |
| and 或 &&      | 同时成立                    |
| or 或 \|\|     | 成立一个                    |
| not 或 !       | 非                       |