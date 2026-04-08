---
title: "问题集 - 使用SakuraFrp实现内网穿透"
published: 2026-04-08
pinned: true
description: "用SakuraFrp来实现把内网的服务部署到外网上去"
tags: [Study, Blog]
category: 问题集
licenseName: "Unlicensed"
author: Rin
draft: false
date: 2026-04-08
pubDate: 2026-04-08
---

 

## 先下载SakuraFrp软件

进入官网 注册账号 实名认证

官网地址

https://www.natfrp.com/?page=panel&module=download

下载软件并复制密钥 启动客户端 粘贴密钥进行登录

## 创建隧道并配置

建立一个新的TCP隧道 这里以nginx服务为例

端口选择80端口(nginx默认端口) https要打开

面板参数介绍

- 隧道名(必填）：自定义隧道名称，只能使用字母、数字、下划线。

- 备注：可以留空不写

- 本地IP：一般都是自己的电脑需要对外提供服务 留空不写 或者写其他电脑的IP地址

- 本地端口（必填）： 自己电脑上的服务跑在什么端口，你就填什么端口。比如：nginx 服务跑在80端口，你就填80。游戏我的世界默认运行端口是25565， 你就填25565。

- 远程端口：一般留空 系统自动分配

- 自动HTTPS：TCP隧道一般保持禁用 启用后 系统会自动为隧道分配 HTTPS 域名并配置证书，适合 Web 服务，游戏联机一般保持默认。

- 访问密码：用于保护隧道访问，可手动输入或点击生成自动创建强密码。

- 隧道自定义设置：

   

  键值对形式（key = value），用于传递高级配置参数（具体含义请参考官方文档）。常见参数如下：

  - 带宽限制（如 `bandwidth_limit = 10M`）

  - 连接超时设置（如 `timeout = 30s`）
  - 额外协议参数（如 TCP_NODELAY 等）

配好之后开启隧道

查看日志 访问Sakura生成的链接

成功出现nginx页面就是成功了

如果出现如下报错:

```txt
No connection could be made because the target machine actively refused it.
```

证明你的本地服务没开起来 自己检查