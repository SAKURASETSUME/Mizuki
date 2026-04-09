---
title: "Linux笔记 - Linux基础知识 - 实操 - 开机、重启、用户登陆注销 - 关机、重启命令"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```shell
#立刻关机
shutdown -h now

#1分钟后关机
shutdown -h 1

#立刻重启
shutdown -r now

#关机
halt

#现在重启
reboot

#把内存的数据同步到磁盘
sync
```

**ps:不管是重启系统还是关闭系统 首先要运行sync命令 把内存中的数据写入到磁盘中**

**目前reboot shutdown halt等命令都在关机前自动进行了sync 但是建议手动再保存一次**