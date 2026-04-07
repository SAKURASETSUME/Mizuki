---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/日志轮替机制/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 原理

**日志文件之所以可以在指定时间备份日志 是依赖系统定时任务 在/etc/cron.daily/目录 就会发现这个目录中是有logrotate文件（可执行） logrotate通过这个文件依赖定时任务执行 **