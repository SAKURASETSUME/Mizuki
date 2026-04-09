---
title: "Linux笔记 - 常用服务搭建 - Nexus - Nexus私服部署"
category: "Linux笔记"
date: 2026-03-20
published: 2026-03-20
author: "Rin"
---

```bash
#安装jdk8
yum install java-1.8.0-openjdk-devel

#配置环境
vim /etc/profile

export JAVA_HOME=/usr/local/java/jdk1.8.0_202
export PATH=$JAVA_HOME/bin:$PATH

#加载配置文件
source /etc/profile

#查看java版本

#下载wget
yum install -y wget

#安装Nexus Repository Manager
cd /data/

[Download](https://help.sonatype.com/en/download.html) 开源站

tar -zxvf 

#出于安全考虑 尽量不要用root用户运行Nexus 最好创一个专门的nexus用户来运行
useradd nexus
chown -R nexus:nexus /data/nexus
chmod -R 755 /data/nexus

#配置Nexus为后台服务
vi /etc/systemd/system/nexus.service

#写入
[Unit]
Description=Nexus Repository Manager
After=network.target
 
[Service]
Type=forking
ExecStart=/data/nexus/bin/nexus start #注意路径
ExecStop=/data/nexus/bin/nexus stop #注意路径
User=nexus
LimitNOFILE=65536
TimeoutStartSec=30
 
[Install]
WantedBy=multi-user.target

#重新加载systemd服务
systemctl daemon-reload

#启动Nexus服务
systemctl start nexus

#设置开机自启
systemctl enable nexus

#检查服务状态
systemctl status nexus

#查看初始密码 （nexus服务启动之后等几分钟 需要初始化之后才会有文件 才能访问页面）
cat /data/sonatype-work/nexus3/admin.password
```

## 配置Nexus作为Maven私服

在Nexus Web UI中，你可以创建多个仓库来存储不同类型的Maven依赖。以创建一个`maven-releases`仓库和一个`maven-snapshots`仓库为例

- 登陆到Nexus web UI
- 进入Responsitory页面
- 选择Setting Respository 创建 选择Maven 2(hosted)类型
- 配置仓库： 
Name：maven-releases
Blob store 默认
Version policy ：Release
其它默认
- 保存并创建

- 再用同样的步骤创建一个`maven-snapshots`仓库，设置 `Version policy` 为 `Snapshot`

## 配置Maven settings.xml

为了让本地Maven构建工具能够将依赖上传到我们的Nexus私服，需要在Maven的`settings.xml`文件中配置Nexus的地址

**修改settings.xml**

打开Maven的`settings.xml`配置文件，通常在`~/.m2/settings.xml`，如果没有这个文件，可以手动创建。添加以下配置

```xml
<servers>
    <server>
        <id>nexus-releases</id>
        <username>admin</username>
        <password>admin_password</password>
    </server>
    <server>
        <id>nexus-snapshots</id>
        <username>admin</username>
        <password>admin_password</password>
    </server>
</servers>
 
<mirrors>
    <mirror>
        <id>nexus</id>
        <mirrorOf>external:http://repo1.maven.org/maven2</mirrorOf>
        <url>http://<server-ip>:8081/repository/maven-public/</url>
        <blocked>false</blocked>
    </mirror>
</mirrors>
```

```txt
 <id>：设置为你在Nexus中创建的仓库名称
 <username>和<password>：默认用户名和密码
 <url>：Nexus仓库的URL地址
```

**配置Maven上传插件**

在`pom.xml`中，配置上传的插件，来将本地构建的jar包上传到Nexus仓库

```xml
<distributionManagement>
    <repository>
        <id>nexus-releases</id>
        <url>http://<server-ip>:8081/repository/maven-releases/</url>
    </repository>
    <snapshotRepository>
        <id>nexus-snapshots</id>
        <url>http://<server-ip>:8081/repository/maven-snapshots/</url>
    </snapshotRepository>
</distributionManagement>

```

## 上传和下载Maven依赖

上传一个Maven项目时，只需使用以下命令即可将项目发布到Nexus私服

```xml
mvn clean deploy
```

Maven将会把构建后的jar包上传到配置的Nexus仓库中

**配置Maven使用私服下载依赖**

在Maven的`pom.xml`文件中添加以下配置，以便从私服下载依赖

```xml
<repositories>
    <repository>
        <id>nexus-releases</id>
        <url>http://<server-ip>:8081/repository/maven-releases/</url>
    </repository>
    <repository>
        <id>nexus-snapshots</id>
        <url>http://<server-ip>:8081/repository/maven-snapshots/</url>
    </repository>
</repositories>
```

参考：[Linux部署maven私服_nexus 3.68.1-CSDN博客](https://blog.csdn.net/qq_62851576/article/details/144337703)