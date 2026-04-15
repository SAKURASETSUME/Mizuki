---
title: "Linux笔记 - 数据库 - 基础 - 数据定义语言-DDL - 数据库操作"
category: "Linux笔记"
date: 2026-04-15
published: 2026-04-15
author: "Rin"
---

```mysql
#查询所有数据库
show databases;
#查询当前数据库
select database();
#创建
create database [if not exists] 数据库名 [default charset 字符集] [coliate 排序规则];
#删除
drop database [if exists] 数据库名;
#使用
use 数据库名;
```