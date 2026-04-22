---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - 安装"
category: "Linux笔记"
date: 2026-04-22
published: 2026-04-22
author: "Rin"
---

Mycat是开源的、活跃的、基于Java语言编写的MySQL数据库中间件。可以像使用mysql一样来使用mycat，对于开发人员来说根本感觉不到mycat的存在。

优势：
- 性能可靠稳定
- 强大的技术团队
- 体系完善
- 社区活跃

## 环境准备

| 服务器             | 安装软件            | 说明          |
| --------------- | --------------- | ----------- |
| 192.168.200.210 | JDK、Mycat、MySQL | MyCat中间件服务器 |
| 192.168.200.213 | MySQL           | 分片服务器       |
| 192.168.200.214 | MySQL           | 分片服务器       |


```bash
#下载地址 https://github.com/MyCATApache/Mycat-Server/releases
#环境准备好MySQL JDK Mycat
#自己下载完手动上传 或者wget
wget https://github.com/MyCATApache/Mycat-Server/releases/download/Mycat-server-1.6.7.4-release/Mycat-server-1.6.7.4-release-20200105164103-linux.tar.gz

#210配置MyCat和JDK
#JDK
#把JDK和MyCat的tar包先传到服务器
#解压
tar -zxvf jdk -C /usr/local
#配置jdk环境
vim /etc/profile
JAVA_HOME=/usr/local/jdk1.8.0_202
PATH=$PATH:$JAVA_HOME/bin
#重新执行profile
source /etc/profile
#测试
java -version

#安装MyCat
tar -zxvf MyCat -C /usr/local
cd /usr/local
cd mycat
#ll可以发现几个文件
#替换掉mysql的驱动包 替换成和服务器mysql版本对应的
cd lib
rm -rf mysql-connector-java-5.1.35.jar
#重新上传一个高版本的
#授权
chmod 777 mysql-connector-java-8.0.22.jar
```

Mycat各目录的用法
bin：存放可执行文件 用于启动停止MyCat
conf：存放mycat的配置文件
lib：存放mycat的项目依赖包
logs：存放mycat的日志文件