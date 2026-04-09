---
title: "Linux笔记 - Linux基础知识 - 大数据 - read获取输入"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
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