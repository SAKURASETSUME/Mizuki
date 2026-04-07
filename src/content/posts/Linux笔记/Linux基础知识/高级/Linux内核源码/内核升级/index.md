---
title: "内核升级"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/高级/Linux内核源码/内核升级/
categories:
  - Linux笔记
  - Linux基础知识
  - 高级
  - Linux内核源码
  - 内核升级
tags:
  - Study
---

## 步骤

```bash
uname -a #查看当前内核版本

yum info kernel -q #检测内核版本 显示可升级的内核

yum update kernel #升级内核

yum list kernel -q #查看已经安装的内核

reboot #重启之后 可以选择进入哪个内核
```
