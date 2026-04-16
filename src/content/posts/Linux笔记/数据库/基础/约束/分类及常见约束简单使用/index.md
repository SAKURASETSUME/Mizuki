---
title: "Linux笔记 - 数据库 - 基础 - 约束 - 分类及常见约束简单使用"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

## 分类

| 约束   | 描述                           | 关键字         |
| ---- | ---------------------------- | ----------- |
| 非空约束 | 限制该字段的数据不能为null              | not null    |
| 唯一约束 | 保证该字段的所有数据都是唯一、不重复的          | unique      |
| 主键约束 | 主键是一行数据的唯一标识 要求非空且唯一         | primary key |
| 默认约束 | 保存数据时 如果未指定该字段的值 则采用默认值      | default     |
| 检查约束 | 保证字段值满足某一个条件                 | check       |
| 外键约束 | 用来让两张表的数据之间建立连接 保证数据的一致性和完整性 | foreign key |

ps：
约束是作用于表中字段上的 可以在创建表/修改表的时候添加约束

## 使用演示
```mysql
create table user(
id int primary key auto_increment comment '主键',
name varchar(10) not null unique comment '姓名',
age int check ( age > 0 && age <= 120 ) comment '年龄',
status char(1) default '1' comment '状态',
gender char(1) comment '性别'
) comment'用户表'
```