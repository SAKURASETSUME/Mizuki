---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - MyCat管理与监控 - MyCat管理工具"
category: "Linux笔记"
date: 2026-04-29
published: 2026-04-29
author: "Rin"
---

建议在了解MyCat的管理与监控之前 先去了解一下MyCat的运行原理
[31. 运维-分库分表-Mycat管理与监控-原理_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Kr4y1i7ru?spm_id_from=333.788.videopod.episodes&vd_source=05d71ca20d1a62ee1c802b01999e7379&p=183)
## 管理工具
MyCat默认开通2个端口 可以在server.xml中修改
- 8066数据访问端口 即进行DML和DDL操作
- 9066数据库管理端口 即mycat服务管理控制功能 用于管理mycat的整个集群状态

通过mysql来连接9066端口
```bash
mysql -h 192.168.200.210 -P 9066 -u root -p
```

mycat管理工具使用

| 命令                | 含义               |
| ----------------- | ---------------- |
| show @@help       | 查看Mycat管理工具的帮助文档 |
| show @@version    | 查看MyCat的版本       |
| reload @@config   | 重新加载MyCat的配置文件   |
| show @@datanode   | 查看MyCat现有的分片节点信息 |
| show @@threadpool | 查看MyCat的线程池信息    |
| show @@sql        | 查看执行的sql         |
| show @@sql.sum    | 查看执行的sql统计       |