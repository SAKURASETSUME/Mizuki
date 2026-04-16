---
title: "Linux笔记 - 数据库 - 基础 - 多表查询 - 连接查询"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

## 内连接查询
```mysql
#隐式内连接
select 字段列表 from 表1,表2 where 条件...;
#显式内连接
select 字段列表 from 表1 [inner] join 表2 on 连接条件...;

#举例
select e.name , d.name from emp e , dept d where e.dept_id = d.id;
select e.name , d.name from emp e join dept d on e.dept_id = d.id;
```

## 外连接查询
```mysql
#左外连接
select 字段列表 from 表1 left [outer] join 表2 on 条件;
#右外连接
select 字段列表 from 表1 right [outer] join 表2 on 条件;

#举例
select e.* , d.name from emp e left join dept d on e.dept_id = d.id;
select e.* , d.* from emp e right join dept d on e.dept_id = d.id;
```

## 自连接查询
```mysql
#语法
select 字段列表 from 表A 别名A join 表A 别名B on 条件;

#用法
#查询员工及其所属领导的名字
select e.name, m.name from emp e join emp m on e.managerid = m.id;
#查询所有员工及其领导的名字 如果员工没有领导也需要查询出来
select e.name '员工' , m.name '领导' from emp e left join emp m on e.managerid = m.id;
```

自连接查询 可以是内连接查询 也可以是外连接查询