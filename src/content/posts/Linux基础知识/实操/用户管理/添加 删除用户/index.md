---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/添加-删除用户/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#基本语法 默认该用户的家目录在/home/xxx 当使用新用户登陆的时候 会默认切换到/home/xxx目录下
useradd 用户名

#指定创建的用户家目录的路径
useradd -d 指定目录 用户名

#指定密码
passwd 用户名

#显示当前目录
pwd

#删除用户 但保留家目录
userdel 用户名

#用户和家目录全部删除
userdel -r 用户名
```