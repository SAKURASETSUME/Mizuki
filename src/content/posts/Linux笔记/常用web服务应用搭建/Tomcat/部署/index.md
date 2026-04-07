---
title: "Linux笔记 - 常用web服务应用搭建 - Tomcat - 部署"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```bash
#Tomcat的安装分为两个步骤：安装JDK和安装Tomcat.
#JDK (Java Development Kit)是Sun Microsystems针对Java开发员的产品。自从Java推出以来， JDK已经成为使用最广泛的Java SDK.JDK是整个Java的核心，包括了Java运行环境，Java工具和Java基础的类库。所以要想运行jsp的程序必须要有JDK的支持，理所当然安装Tomcat的前提是安装好JDK.

#查看系统是否有jdk
rpm -qa | grep java

#删除包
rpm -e --nodeps +包名

#安装jdk
cd /usr/local/src/

#下载
wget 链接
#或者自己从官网下 用xftp传过去也行

#压缩包解压
tar -zxvf 包名
cp -p 文件名 /usr/local/java

#配置环境变量
vim /etc/profile

#写入
export JAVA_HOME=/usr/local/java/jdk1.8
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

#重载配置文件
source /etc/profile

#测试
java -version
java
javac -version

#安装Tomcat 此处以TOmcat7.0.104为例
cd /usr/local/src
wget https://archive.apache.org/dist/tomcat/tomcat-7/v7.0.104/bin/apache-tomcat-7.0.104.tar.gz

#赋权
chmod 755 /etc/init.d/tomcat
chkconfig --add tomcat
chkconfig tomcat on

#启动 默认端口8080
service tomcat start
#或者
cd /usr/local/tomcat/bin
./startup.sh
#或者
sh startup.sh

#查看是否启动成功
ps -aux | grep tomcat
ps -rf | grep tomcat

#开启防火墙端口
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --reload
firewall-cmd --zone=public --query-port=8080/tcp

#配置账号密码
cd /usr/local/tomcat/conf/tomcat-users.xml
#找到字段
<role rolename="manager-gui"/>

<user username="tomcat" password="123456" roles="manager-gui"/>

#保存 重启Tomcat
```

## Tomcat目录结构介绍

![Tomcat目录](https://i-blog.csdnimg.cn/blog_migrate/0521a39dcc324f6408205121fdc513db.png)

参考：[linux中tomcat的安装和配置（最全最详细）_linux tomcat安装及配置教程-CSDN博客](https://blog.csdn.net/qq_37839971/article/details/96693989)

[Apache Tomcat 历史版本下载地址 官网地址-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2629356)