---
title: "Linux笔记 - Linux基础知识 - 面试题 - Linux系统优化策略"
category: "Linux笔记"
date: 2026-03-17
published: 2026-03-17
author: "Rin"
---

```txt
1.对Linux的架构的优化，和原则分析 -> 负载均衡 网络 磁盘IO 文件连接数 安全性 防火墙 内存
2.对linux系统本身的优化-规则
（1）不用root，使用sudo提示权限
（2）定时的自动更新服务时间，使用ntpdate ntp1.aliyun.com，让croud定时更新
（3）配置yum源，指向国内镜像（清华，163）
（4）配置合理的防火墙策略，打开必要的端口，关闭不必要的端口
（5）打开最大文件数（调整文件的描述的数量）vim/etc/profile ulimit-SHn 65535
（6）配置合理的监控策略
（7）配置合理的系统重要文件的备份策略
（8）对安装的软件进行优化，比如nginx，apache
（9）内核参数进行优化/etc/sysctl.conf
（10）锁定一些重要的系统文件chattr /etc/passwd /etc/shadow /etc/inittab
（11）禁用不必要的服务setup，ntsysv
```