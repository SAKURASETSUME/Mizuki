---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 防盗链 - 基本概念"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

**防盗链 就是校验http请求的referer请求头 后端服务器只允许网关服务器进行资源的访问 不能被别的任何服务器访问 防盗链通过校验referer请求头就可以知道是谁在访问后端服务器里的资源 如果是外部来的访问 就直接打回**