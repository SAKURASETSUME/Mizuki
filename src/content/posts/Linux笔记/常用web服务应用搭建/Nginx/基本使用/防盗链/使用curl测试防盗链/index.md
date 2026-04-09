---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 防盗链 - 使用curl测试防盗链"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```bash
#测试 不展示内容 展示响应请求头的信息
curl -I http://nakatsusizuru.top/img/logo.png

#带引用
curl -e "http://baidu.com" -I http://nakatsusizuru.top/img/logo.png
```