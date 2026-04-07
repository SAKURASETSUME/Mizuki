---
title: "用户组"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/实操/用户管理/用户组/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 概念

类似于角色 系统可以对有共性/权限的多个用户进行统一的管理


## 语法

```bash
#新增组
groupadd 组名

#删除组
groupdel 组名

#添加用户时直接加上组
useradd -g 组名 用户名

#修改用户的组
usermod -g 组名 用户名
```