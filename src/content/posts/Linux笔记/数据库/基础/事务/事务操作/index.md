---
title: "Linux笔记 - 数据库 - 基础 - 事务 - 事务操作"
category: "Linux笔记"
date: 2026-04-17
published: 2026-04-17
author: "Rin"
---

## 语法
```mysql
#查看/设置事务提交方式
select @@autocommit;
set @@autocommit=0;

#提交事务
commit;

#回滚事务
rollback;

#方式二
#开启事务
start transaction 或 begin

#提交事务
commit;

#回滚事务
rollback;
```

## 演示
```mysql
select @@autocommit;
set @@autocommit = 0; #设置为手动提交

select * from account where name = '张三';
update account set money = money - 1000 where name = '张三';
#这是一个异常 如果要测试回滚 就把这句的注释去掉
update account set money = money + 1000 where name = '李四';

commit; #如果不写这条语句 数据就不会变
rollback; #如果执行出错了 就选中这条语句回滚事务

#方式二
start transaction;
select * from account where name = '张三';
update account set money = money - 1000 where name = '张三';
#这是一个异常
update account set money = money + 1000 where name = '李四';

commit;
rollback;
```