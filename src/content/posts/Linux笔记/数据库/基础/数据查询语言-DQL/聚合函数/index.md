---
title: "Linux笔记 - 数据库 - 基础 - 数据查询语言-DQL - 聚合函数"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

聚合函数 指的是将一列数据作为一个整体 进行纵向计算

## 常见聚合函数

| 函数    | 功能   |
| ----- | ---- |
| count | 统计数量 |
| max   | 最大值  |
| min   | 最小值  |
| avg   | 平均值  |
| sum   | 求和   |
## 语法
```mysql
#注意 所有的null值不参与聚合函数的运算
select 聚合函数(字段列表) from 表名;
```