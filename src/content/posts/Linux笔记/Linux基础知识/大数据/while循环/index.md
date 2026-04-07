---
title: "while循环"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/大数据/while循环/
categories:
  - Linux笔记
  - Linux基础知识
  - 大数据
  - while循环
tags:
  - Study
---

## 基本语法1

```bash
while [ 条件判断式 ]
do
程序
done
```

## 案例

```txt
统计从1加到n
```

```bash
#!/bin/bash
SUM=0
i=0
while [ $i -le $1 ]
do
        SUM=$[$SUM+$i]
        i=$[$i+1]
done
        echo "从1加到$1=$SUM"
```