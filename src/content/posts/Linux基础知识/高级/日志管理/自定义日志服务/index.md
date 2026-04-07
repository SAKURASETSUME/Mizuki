---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/自定义日志服务/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
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