---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/监控网络状态/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
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