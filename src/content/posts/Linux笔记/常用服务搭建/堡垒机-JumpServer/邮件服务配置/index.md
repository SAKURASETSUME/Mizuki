---
title: "邮件服务配置"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/常用服务搭建/堡垒机-JumpServer/邮件服务配置/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 申请邮件服务 以QQ邮箱为例

**登陆之后 点开设置 账号设置 打开SMTP服务 生成一下授权码**

**SMTP主机为smtp.qq.com
端口号是465
账号是邮箱
SMTP密码是授权码
使用SSL服务**

**如果堡垒机不是部署在公网上的话 跳转会出错 跳转的地址是系统设置中的URL 如果部署在内网 只能通过内网访问**