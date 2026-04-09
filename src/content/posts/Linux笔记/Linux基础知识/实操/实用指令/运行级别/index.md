---
title: "Linux笔记 - Linux基础知识 - 实操 - 实用指令 - 运行级别"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

- 0：关机
- 1：单用户(找回丢失密码)
- 2：多用户状态没有网络服务
- 3：多用户状态有网络服务
- 4：系统未使用保留给用户
- 5：图形界面
- 6：系统重启

常用运行级别是3和5 也可以指定默认运行级别

```bash
#指定运行级别
init 运行级别
```

## 指定运行级别

**在CentOS7以前 运行级别在/etc/inittab中**

**CentOS7开始 进行了简化:
multi-user.target : analogous to runlevel 3
graphical.target : analogous to runlevel 5**

```bash
#查看当前运行级别
systemctl get-default

#设置默认运行级别 比如设置3级别
systemctl set-default multi-user.target
```