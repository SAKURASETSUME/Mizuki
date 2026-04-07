---
title: "Linux笔记 - Linux基础知识 - 高级 - 日志管理 - 日志管理服务"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## rsyslogd

**CentOS7的日志服务是rsyslogd CentOS6.x的日志服务是syslogd rsyslogd的功能更强大 rsyslogd的使用、日志文件的格式和syslogd相同**

- 查询Linux中的rsyslogd服务是否启动

```bash
ps aux | grep "rsyslogd" | grep -v "grep"
```

- 查询rsyslogd服务的自启动状态

```bash
systemctl list-unit-files | grep rsyslog
```

## 日志服务配置文件

**位置：/etc/rsyslog.conf**

**编辑格式： \*.\* 存放日志文件 其中第一个\*代表日志类型 第二个\*代表日志级别**

**日志类型分为**

- auth pam产生的日志
- authpriv ssh、ftp等登录信息的验证信息
- corn 时间任务相关
- kern 内核
- lpr 打印
- mail 邮件
- mark(syslog)-rsyslog 服务内部信息 时间标识
- news 新闻组
- users 用户程序产生的相关信息
- uucp unix to nuix copy主机之间线管的通信
- local 1-7 自定义的日志设备

**日志级别分为**

- debug 有调试信息的 日志通信最多
- info 一般信息日志 最常用
- notice 最具有重要性的普通条件的信息
- warning 警告级别
- err 错误级别 阻止某个功能或者模块不能正常工作的信息
- crit 严重级别 阻止某个系统或者整个软件不能正常工作的信息
- alert 需要立刻修改的信息
- emerg 内核崩溃等重要信息
- none 什么都不记录
ps：从上到下 级别从低到高 记录信息越来越少

## 日志文件的格式包含以下4列

- 事件产生的时间
- 产生事件的服务器的主机名
- 产生事件的服务名或程序名
- 事件的具体信息