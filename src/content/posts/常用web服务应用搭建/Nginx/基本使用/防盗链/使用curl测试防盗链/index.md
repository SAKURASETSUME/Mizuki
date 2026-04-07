---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/使用curl测试防盗链/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#测试 不展示内容 展示响应请求头的信息
curl -I http://nakatsusizuru.top/img/logo.png

#带引用
curl -e "http://baidu.com" -I http://nakatsusizuru.top/img/logo.png
```