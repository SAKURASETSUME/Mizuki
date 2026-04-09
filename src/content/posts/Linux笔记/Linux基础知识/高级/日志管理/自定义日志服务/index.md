---
title: "Linux笔记 - Linux基础知识 - 高级 - 日志管理 - 自定义日志服务"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 添加一个日志文件

```txt
在/etc/rsyslog.conf 中添加一个日志文件/var/log/adad.log 当有事件发送时 该文件会接受信息并保存 用重启 登陆来测试
```

```bash
vim /etc/rsyslog.conf

#写入
*.*       /var/log/adad.log

#重启过后查看
cat /var/log/adad.log | grep "sshd"
```