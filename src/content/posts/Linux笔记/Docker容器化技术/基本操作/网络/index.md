---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - 网络"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

## 自定义网络
```bash
#每个应用启动之后都会加入一个叫docker0的网络
#每个应用都有单独的一个被docker分配的ip
#查看
docker inspect nginx #有一个值 "IPAddress": "172.17.0.2", 这个就是他的IP

#进入到nginx 直接访问另一个nginx
docker exec -it nginx bash
curl 172.17.0.3
#能够成功访问 说明容器之间可以通过docker0进行相互访问
#但是这种方式有个缺点 ip会有各种各样的原因被改变
#使用自定义网络的方法来解决

#创建自定义网络
docker network create mynet
#查看
docker network ls
#运行容器时加入自定义网络
docker run -p 80:80 --name nginx --network mynet mynginx:v1.0
docker run -p 88:80 --name nginx2 --network mynet mynginx:v1.0
#进入容器 直接用容器名访问
docker exec -it nginx bash
curl http://nginx2
#能够正常访问 说明配置成功
```

## 用Redis启动一个主从同步集群
```bash
#启动两个Redis容器
#一个作为MASTER 一个作为SLAVE SLAVE要同步MASTER的数据
#实现读写分离 写请求给MASTER 读请求交给SLAVE
#把redis里/bitnami/redis/data挂载到Docker Host的/app/rd1和/app/rd2
#建议使用bitnami的镜像
#MASTER运行
docker run -p 6379:6379 -d \
-v /app/rd1:/bitnami/redis/data \
-e REDIS_REPLICATION_MODE=master \
-e REDIS_PASSWORD=123456 \
--name redis01 --network mynet \
bitnami/redis


#赋权
chmod -R 777 /app/rd1

#SLAVE运行
docker run -p 6380:6379 -d \
--name redis02 --network mynet\
-v /app/rd2:/bitnami/redis/data  \
-e REDIS_REPLICATION_MODE=slave  \
-e REDIS_MASTER_HOST=redis01 \
-e REDIS_MASTER_PORT_NUMBER=6379 \
-e REDIS_MASTER_PASSWORD=123456 \
-e REDIS_PASSWORD=123456 \
bitnami/redis

#赋权
chmod -R 777 /app/rd2
```

### Redis同步环境变量配置
```bash
#主机
REDIS_REPLICATION_MODE=master
REDIS_PASSWORD=123456

#从机
REDIS_REPLICATION_MODE=slave
REDIS_MASTER_HOST=redis01
REDIS_MASTER_PORT_NUMBER=6379
REDIS_MASTER_PASSWORD=123456
REDIS_PASSWORD=123456
```