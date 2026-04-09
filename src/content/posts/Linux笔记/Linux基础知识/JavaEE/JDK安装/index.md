---
title: "Linux笔记 - Linux基础知识 - JavaEE - JDK安装"
category: "Linux笔记"
date: 2026-03-12
published: 2026-03-12
author: "Rin"
---

## 安装步骤

- 创建文件夹存放jdk

```bash
mkdir /opt/jdk
```

- 通过xftp6 上传到/opt/jdk下

- cd /opt/jdk

- 解压

```
tar -zxvf jdk-8u202-linux-x64.tar.gz
```

- mkdir /usr/local/java

- mv /opt/jdk/jdk1.8.0_202 /usr/local/java

- 配置环境变量的配置文件

```bash
vim /etc/profile

export JAVA_HOME=/usr/local/java/jdk1.8.0_202
export PATH=$JAVA_HOME/bin:$PATH

#让新的环境生效
source /etc/profile
```

- 测试是否安装成功(自己写一个helloworld)