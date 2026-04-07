---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/无人值守备份目录/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```txt
列出你了解的web服务器负载架构
```

```txt
Nginx
Haproxy
Keepalived
LVS
```

```txt
每天晚上10点30分 打包站点目录/var/spool/mail备份到/home 目录下（每次备份按时间生成不同的备份包）
```

```bash
#!/bin/bash
cd /var/spool/ && /bin/tar zcf /home/mail-`date +%Y-%m-%d_%H%M%S`.tar.gz mail/

crond -e
30 22 * * * /bin/sh /root/shcode/bak.sh
```