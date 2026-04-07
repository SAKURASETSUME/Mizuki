---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/case语句/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 基本语法

```bash
case $变量名 in
"值1")
如果变量的值等于值1 则执行程序1
;;
"值2")
如果变量的值等于值2 则执行程序2
;;
...
*)
如果变量的值都不是以上的值 则执行此程序
;;
esac
```

## 案例

```txt
当命令行参数是1 输出周一 命令行参数是2 输出周二 其它other
```

```bash
#!/bin/bash
case $1 in
"1")
        echo "周一"
;;
"2")
        echo "周二"
;;
*)
        echo "other"
;;
esac
```