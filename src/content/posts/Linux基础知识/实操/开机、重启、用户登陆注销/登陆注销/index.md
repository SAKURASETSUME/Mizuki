---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/登陆注销/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

**登录时建议尽可能少使用root登陆 因为它是系统管理员 最大的权限 避免操作失误 可以利用普通用户登录 登陆后再用 "su - 用户名" 命令来切换成系统管理员身份**

**在提示符下输入logout即可注销用户**

```shell
#切换用户
su - 用户名

#退出用户（在图形化界面使用无效）
logout
```