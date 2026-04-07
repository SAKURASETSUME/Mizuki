---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/权限思考题/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```txt
1.用户tom对目录/home/test有执行和读写权限，/home/test/hello.java是只读文件，问tom对hello.java文件能读吗？能修改吗？能删除吗？ -> 能读 能删 不能改

2.用户tom对目录/home/test只有读写权限，/home/test/hello.java是只读文件，问tom对hello.java文件能读吗？能修改吗？能删除吗？  -> 不能读(进不去test目录 无法执行命令) 不能删 不能改

3.用户tom对目录/home/test只有执行权限，/home/test/hello.java是只读文件，问tom对hello.java文件能读吗？能修改吗？能删除吗？   -> 能读 不能删和改

4.用户tom对目录/home/test只有执行和写权限，/home/test/hello.java是只读文件，问tom对hello.java文件能读吗？能修改吗？能删除吗？ -> 能读 能删 不能改

```