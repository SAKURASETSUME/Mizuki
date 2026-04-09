---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 目录结构与基本原理"
category: "Linux笔记"
date: 2026-03-27
published: 2026-03-27
author: "Rin"
---

| conf | 配置文件 |
| ---- | ---- |
| html | 页面   |
| logs | 日志文件 |
| sbin | 主程序  |

## 基本运行原理

sbin下的nginx运行之后 会启动一个master进程 来读取并校验配置文件 这个是主进程 -> 主进程启动之后 会启动子进程worker worker会根据配置文件去找目录和文件 来响应用户请求