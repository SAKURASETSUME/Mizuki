---
title: "内存日志"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/高级/日志管理/内存日志/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 常用指令

```bash
#查看全部
journalctl

#查看最新三条
journalctl -n 3

#查看起始时间到结束时间的日志 可加日期
journalctl --since 19:00 --until 19:10:10

#报错日志
journalctl -p err

#日志详细内容
journalctl -o verbose

#查看包含这些参数的日志
journalctl_PID=1345 _COMM=sshd
#或者
journalctl | grep sshd
```