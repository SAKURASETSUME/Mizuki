---
title: "Linux笔记 - 常用服务搭建 - Zookeeper - 部署"
category: "Linux笔记"
date: 2026-04-29
published: 2026-04-29
author: "Rin"
---

```bash
#安装Zookeepr
#下载安装包 上传到服务器
#https://zookeeper.apache.org/releases.html
#解压
tar -zxvf apache-zookeeper-3.5.7-bin.tar.gz -C /usr/local/
#修改配置
mv zoo_sample.cfg zoo.cfg
vim zoo.cfg
#修改
dataDir=/usr/local/apache-zookeeper-3.5.7-bin/zkData
#之所以要修改这个路径，是因为dataDir 默认路径在ltemp目录下，这个目录是Linux.系统的临时目录，会定期自动删除。具体将dataDir路径修改到哪没有强制要求，但是最好改到Zookeeper 根目录下的某个目录中，比如根目录下的zkData目录，所以我们要回到Zookeeper根目录去创建一个zkData目录。
mkdir zkData

#启动服务端
bin/zkServer.sh start
#查看进程
jps
#有QuorumPeerMain就是启动了
#查看状态
bin/zkServer.sh status
#启动客户端
bin/zkCli.sh
#退出客户端
quit
#停止服务端
bin/zkServer.sh stop
```

## 配置文件说明
```shell
#The number of milliseconds of each tick
#通信心跳时间，Zookeeper服务器与客户端心跳时间，单位毫秒。
tickTime=2000
# The number of ticks that the initial#synchronization phase can take
#LF初始通信时限。
# Leader和Follower初始连接时能容忍的最多心跳数，单位次（即tickTime的数量)。
initLimit=10
#The number of ticks that can pass between
#sending a request and getting an acknowledgement#LF同步通信时限。
# Leader和Follower连接之后，通信时能容忍的最多心跳数，单位次。
#时间如果超过syncLimit * tickTime，,Leader认为Follwer挂掉，从服务器列表中删除Follwer。
syncLimit=5
# the directory where the snapshot is stored.# do not use /tmp for storage,/tmp here is just# example sakes.
#保存Zookeeper中的数据的目录。
dataDir=/opt /module/ apache-zookeeper-3.5.7-bin/zkData
#the port at which the clients will connect
#客户端连接端口，通常不做修改。
clientPort=2181
```

## 集群安装
```bash
#配置节点编号
#服务器hadoop102
#创建目录/zkData
mkdir /zkData
vi myid
#写入 这里编号不作强制要求 建议有规律
2
#在zoo.cfg配置集群节点信息
#cluster
server.2=hadoop102:2888:3888
server.3=hadoop103:2888:3888
server.4=hadoop104:2888:3888
#配置说明
#格式: server.A=B:C:D
#A是一个数字，表示这个是第几号服务器;集群模式下配置一个文件myid，这个文件在dataDir目录下，这个文件里面有一个数据就是A的值，Zookeeper启动时读取此文件，拿到里面的数据与zoo.cfg里面的配置信息比较从而判断到底是哪个server。
#B是这个服务器的地址;
#C是这个服务器Follower与集群中的Leader 服务器交换信息的端口;
#D是万一集群中的Leader服务器挂了，需要一个端口来重新进行选举，选出一个新的Leader，而这个端口就是用来执行选举时服务器相互通信的端口。

#在其余节点安装Zookeeper 直接将hadoop102的目录apache-zookeeper-3.5.7-bin整个分发到其它服务器的相应目录下 之后把myid的编号改了
#启动集群并查询状态
bin/zkServer.sh start
bin/zkServer.sh status
```