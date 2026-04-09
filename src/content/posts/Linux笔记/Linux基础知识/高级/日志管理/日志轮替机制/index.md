---
title: "Linux笔记 - Linux基础知识 - 高级 - 日志管理 - 日志轮替机制"
category: "Linux笔记"
date: 2026-03-13
published: 2026-03-13
author: "Rin"
---

## 原理

**日志文件之所以可以在指定时间备份日志 是依赖系统定时任务 在/etc/cron.daily/目录 就会发现这个目录中是有logrotate文件（可执行） logrotate通过这个文件依赖定时任务执行 **