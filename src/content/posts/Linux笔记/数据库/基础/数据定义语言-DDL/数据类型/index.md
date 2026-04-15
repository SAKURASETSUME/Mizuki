---
title: "Linux笔记 - 数据库 - 基础 - 数据定义语言-DDL - 数据类型"
category: "Linux笔记"
date: 2026-04-15
published: 2026-04-15
author: "Rin"
---

数据类型大体分为三大类
- 数值类型
- 字符串类型
- 日期类型

## 案例
```txt
设计一张员工信息表，要求如下：
1.编号(纯数字）
2.员工工号(字符串类型，长度不超过10位）
3．员工姓名（字符串类型，长度不超过10位）
4. 性别（男/，存储个汉字)
5.年龄（正常人年龄，不可能存储负数）
6.身份证号（二代身份证号均为18位，身份证中有X这样的字符）
7.入职时间（取值年月日即可）
```

```mysql
create table emp (
	number int,
	worknu varchar(10),
	name varchar(10),
	gender char(1),
	age tinyint unsigned,
	id char(18),
	entrydate date comment '入职时间'
)comment '员工表';
```