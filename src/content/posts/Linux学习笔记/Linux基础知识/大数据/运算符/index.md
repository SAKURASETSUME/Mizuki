---
title: "运算符"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/大数据/运算符/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 基本语法

```bash
"$((运算式))" 或 "$[运算式]" 或者expr m + n
```

- 注意expr运算符间要有空格
- expr m - n **注意：如果要把expr表达式的结果赋给变量 需要用反引号括起来**
- expr `\*`, / , % 乘 除 取余

## 实例

- 计算 (2+3) \*4的值

```bash
echo "(2+3)*4=$[(2+3)*4]"
```

- 求出命令行的两个参数\[整数]的和

```bash
#执行时传入两个数
#sh /root/shcode/expression.sh 10 20
echo "$1+$2=$[$1+$2]"
```