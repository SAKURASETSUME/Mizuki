---
title: "Linux笔记 - Linux基础知识 - 实操 - 用户管理 - 查询用户 切换用户"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```bash
#查询语法
id 用户名

#切换用户 （高权限的用户切换到低权限的用户时不需要输入密码）
su - 用户名

#登出
logout

#查看当前用户信息(查询的是第一次登陆的用户 用su切换用户 查询的还是第一次登陆的用户)
whoami / who am I
```