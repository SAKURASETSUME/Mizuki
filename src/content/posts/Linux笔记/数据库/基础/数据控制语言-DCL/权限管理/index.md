---
title: "Linux笔记 - 数据库 - 基础 - 数据控制语言-DCL - 权限管理"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

## 用户管理
```mysql
#查询用户
use mysql;
select * from user;

#创建用户
create user '用户名'@'主机名' identified by '密码'; #这里的主机名代表的是能够在哪台主机访问数据库 如果想要设置任意主机访问 用%就行了

#修改用户密码
alter user '用户名'@'主机名' identified by mysql_native_password by '新密码';

#删除用户
drop user '用户名'@'主机名';
```

## 权限控制
```mysql
#查询权限
show grants for '用户名'@'主机名';

#授予权限
grant 权限列表 on 数据库名.表名 to '用户名'@'主机名';

#撤销权限
revoke 权限列表 on 数据库名.表名 from '用户名'@'主机名'
```

| 权限                 | 说明         |
| ------------------ | ---------- |
| all,all,privileges | 所有权限       |
| select             | 查询数据       |
| insert             | 插入数据       |
| update             | 修改数据       |
| delete             | 删除数据       |
| alter              | 修改表        |
| drop               | 删除数据库/表/视图 |
| create             | 创建数据库/表    |
ps:
- 多个权限之间 使用逗号分隔
- 授权时 数据库名和表名可以使用\*进行通配 代表所有