---
title: "统计文件个数和行数"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/面试题/统计文件个数和行数/
categories:
  - Linux笔记
  - Linux基础知识
  - 面试题
  - 统计文件个数和行数
tags:
  - Study
---

```txt
Shell脚本里如何检查一个文件是否存在 并给出提示
```

```bash
if [ -f 文件路径 ]
then
	echo "文件存在"
else
	echo "文件不存在"
fi
```

```txt
用shell写一个脚本 对文本t3.txt中无序的一列数字排序 并将总和输出
9
8
7
6
5
4
3
2
10
```

```bash
sort -n /opt/interview/t3.txt | awk '{sum+=$0 ; print $0} END {print "和="sum}'
```

```txt
请用指令写出查找当前文件夹（/home）下所有的文本文件内容中包含有字符“cat”的文件名称
```

```bash
grep -r "cat" /home | awk -F ":" '{print $1}'
```

```txt
请写出统计/home目录下所有文件个数和所有文件总行数的指令
```

```bash
find /home -name "*.*" | wc -l

find /home -name "*.*" | xargs wc -l
```