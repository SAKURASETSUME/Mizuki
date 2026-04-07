---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/read获取输入/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 基本语法

```bash
read (选项) (参数)
#选项
-p 指定读取值时的提示符
-t 指定读取值时的等待时间
参数：
变量 指定读取值的变量名
```

## 实例

```txt
读取控制台输入一个num值 如果在10s内不输入就不等待
```

```bash
#!/bin/bash
read -t 10 -p "请输入一个数NUM1=" NUM1
echo "你输入的NUM1=$NUM1"
```