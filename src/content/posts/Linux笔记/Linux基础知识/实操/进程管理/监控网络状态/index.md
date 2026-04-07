---
title: "监控网络状态"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/实操/进程管理/监控网络状态/
categories:
  - Linux笔记
  - Linux基础知识
  - 实操
  - 进程管理
  - 监控网络状态
tags:
  - Study
---

```bash
#基本语法
netstat [选项]
#选项说明
-an 按一定的顺序排列输出
-p 显示哪个进程在调用

#常用组合
netstat -ntlp
```

## 顶部信息

- Proto 协议
- Local Address 本地地址（Linux地址）
- Foreign Address 外部地址

```bash
#查看哪个进程在使用tcp协议建立连接
netstat -anp | grep tcp
```