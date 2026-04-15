---
title: "Linux笔记 - 数据库 - 基础 - 数据操作语言-DML - 增删改"
category: "Linux笔记"
date: 2026-04-15
published: 2026-04-15
author: "Rin"
---

## 添加数据
```mysql
#给指定字段添加数据
insert into 表名(字段名1，字段名2,...) values(值1,值2,...);
#给全部字段添加数据
insert into 表名 values(值1,值2,...);
#批量添加数据
insert into 表名(字段名1,字段名2,...) values(值1,值2,...),values(值1,值2,...),values(值1,值2,...);
insert into 表名 values(值1,值2,...),values(值1,值2,...),values(值1,值2,...);
```

ps:
- 插入数据时，指定的字段顺序需要与值的顺序是一一对应的。
- 字符串和日期型数据应该包含在引号中。
- 插入的数据大小，应该在字段的规定范围内。

## 修改数据
```mysql
#修改字段的值
update 表名 set 字段名1=值1,字段名2=值2,,...[where 条件];
```

ps：
修改语句的条件可以写 也可以不写 如果不写 修改的就是整个表的对应字段的数据

## 删除数据
```mysql
#删除
delete from 表名 [where 条件]
```

ps：
- delete语句的条件可以写 也可以不写 如果不写 删除的就是整张表的所有数据
- delete语句不能删除某一个字段的值 如果要删除某一个字段的值 可以使用update