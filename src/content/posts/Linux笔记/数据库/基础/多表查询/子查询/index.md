---
title: "Linux笔记 - 数据库 - 基础 - 多表查询 - 子查询"
category: "Linux笔记"
date: 2026-04-17
published: 2026-04-17
author: "Rin"
---

```mysql
#基本语法
select * from t1 where column1 = (select column1 from t2);
```

子查询外部的语句可以是inset / update / delete / select的任何一个

## 子查询的分类
- 标量子查询 -> 子查询结果为单个值
- 列子查询 -> 子查询结果为一列
- 行子查询 -> 子查询结果为一行
- 表子查询 -> 子查询结果为多行多列

根据子查询的位置分为：where之后、from之后、select之后

## 标量子查询
```mysql
#举例
#根据销售部门ID查询员工信息
select * from emp where dept_id = (select id from dept where name = '销售部');
```

常用操作符：>、<、!=、>=、<=、=
## 列子查询
```mysql
#举例
#查询销售部和市场部的所有员工信息
select * from emp where dept_id in (select id from dept where name = '销售部' || name = '市场部');
#查询比财务部所有人工资都高的人的信息
selec * from emp where salary > all (select salary from emp where dept_id = (select id from dept where name = '财务部'))
```

常用操作符：in、not in、any、some、all

| 操作符    | 描述               |
| ------ | ---------------- |
| in     | 在指定的范围内 多选一      |
| not in | 不在指定的范围内         |
| any    | 子查询返回列表中 有一个满足即可 |
| some   | 与any相同           |
| all    | 子查询返回列表的值必须全部满足  |

## 行子查询
```mysql
#举例
#查询与test的薪资和直属领导相同的员工信息
select * from emp where (salary , managerid) = (select salary , managerid from emp where name = 'test');
```

常用操作符：=、!=、in、not in

## 表子查询
```mysql
#举例
#查询与test1 test2的职位和薪资相同的员工信息
select * from emp where (job , salary) in (select job , salary from emp where name = 'test1' || name = 'test2');

#查询入职日期是'2006-01-01'之后的员工信息和部门信息
select e.*, d.* from (select * from emp where entrydate > '2006-01-01') e left join dept d on e.dept_id = d.id;
```
常用操作符：in