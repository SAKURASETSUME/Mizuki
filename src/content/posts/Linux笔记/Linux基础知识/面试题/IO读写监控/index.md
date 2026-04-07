---
title: "IO读写监控"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/面试题/IO读写监控/
categories:
  - Linux笔记
  - Linux基础知识
  - 面试题
  - IO读写监控
tags:
  - Study
---

```txt
列举Linux高级命令 至少6个
```

```bash
netstat #网络状态监控
top #系统运行状态
lsblk #查看硬盘分区
find 
ps -aux #查看运行进程
chkconfig #查看服务启动状态
systemctl #管理系统服务
```

```txt
Linux查看内存 IO读写 磁盘存储 端口占用 进程查看命令是什么
```

```bash
top #查看内存
iotop #IO读写 要用yum安装一下
df -lh #磁盘存储
netstat -tunlp #端口占用情况
ps -aux #进程查看
```

```txt
用Linux命令计算t2.txt第二列的和并输出
张三 40
李四 50
王五 60
```

```bash
#查看 截取 相加 打印
cat /opt/interview/t2.txt | awk -F " " '{sum+=$2} END {print sum}'
```