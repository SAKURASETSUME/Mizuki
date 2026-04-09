---
title: "Linux笔记 - Linux基础知识 - 实操 - 实用指令 - 时间日期指令"
category: "Linux笔记"
date: 2026-03-10
published: 2026-03-10
author: "Rin"
---

```bash
#显示当前时间
date

#显示当前年份
date +%Y

#显示当前月份
date +%m

#显示当前是哪一天
date +%d

#显示年月日时分秒
date "+%Y-%m-%d %H:%M:%S"

#设置日期
date -s 字符串时间
#例如
date -s "2026-11-11 20:05:10"

#查看日历
cal [选项] #选项写数字 可以查看指定年份的日历
```