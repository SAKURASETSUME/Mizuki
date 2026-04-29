---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - MyCat管理与监控 - MyCat图形化监控"
category: "Linux笔记"
date: 2026-04-29
published: 2026-04-29
author: "Rin"
---

## Mycat-eye
### 介绍
Mycat-web(Mycat-eye)是对mycat-server提供监控服务，功能不局限于对mycat-server使用。他通过JDBC连接对Mycat、Mysql监控，监控远程服务器(目前仅限于linux系统)的cpu、内存、网络、磁盘。

Mycat-eye运行过程中需要依赖zookeeper，因此需要先安装zookeeper

## 部署Mycat-web
```bash
#把安装包上传到服务器
#解压
tar -zxvf Mycat-web.tar.gz -C /usr/local/
cd /usr/local/mycat-web
#启动
sh start.sh
#注意 如果你的zookeeper不在mycat这台服务器上 你需要去修改一下配置文件
vim /usr/local/mycat-web/WEB_INF/classes/mycat.properties
#修改
zookeeper=IP:port

#访问
192.168.200.210:8082/mycat
```

### 使用
- 先在mycat服务管理中配置好初始参数 管理端口默认9066 服务端口默认8066
- 经常使用的是mycat性能监控和mysql的分析