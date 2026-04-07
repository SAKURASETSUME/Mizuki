---
title: "Linux笔记 - Linux基础知识 - 实操 - 实用指令 - 找回root密码"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 步骤（CentOS7.6）

- 启动系统 进入开机界面 按e进入编辑界面
- 进入编辑界面 找到Linux16开头的行 在行的最后输入 init=/bin/sh
- 按下Ctrl + x 进入单用户模式
- 接着 输入mount -o remount,rw /
- 按下回车 再输入passwd 输入两次密码
- 输入touch /.autorelabel
- 接着输入 exec /sbin/init 按下回车 (等待时间较长 完成后会自动重启 不用管)