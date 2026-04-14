---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - 常用命令"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

场景：启动一个nginx 并将它的首页改为自己的页面 发布出去 让所有人都能使用
## 镜像操作
```bash
#下载nginx软件镜像
docker search nginx #找一下有没有这个镜像 如果要下载指定版本的镜像 建议去docker hub去搜索
docker pull nginx #下载 这里下载的默认是最新版本 如果想要下载指定版本 就把nginx换成镜像名：标签(版本) 比如你要下载nginx1.26.0 docker pull nginx:1.26.0
docker image ls #查看已经下载过的镜像
docker rmi 镜像名:标签 / IMAGE ID #删除镜像

#提交修改
docker commit -m "update index.html" mynginx mynginx:v1.0
#保存镜像为一个tar包
docker save -o mynginx.tar mynginx:v1.0
#加载tar包
docker load -i mynginx.tar

#分享镜像
#登陆到docker hub
docker login
#把镜像改名
docker tag 原镜像名:tag dockerhub的用户名/新镜像名:tag
#推送
docker push nakatsusizuru/dockertest:v1.0 #这里建议推送的时候准备两个版本 一个是latest 一个是当前的版本号 之后把两个都推送一次
```

docker hub：[Docker Hub Container Image Library | App Containerization](https://hub.docker.com/)

## 容器操作
```bash
docker run 镜像#运行
docker ps #查看
docker stop ID #停止
docker start ID #启动
docker restart ID #重启
docker stats #状态
docker logs ID #日志
docker exec #进入容器内部
docker rm ID #删除容器 如果容器停不掉 想要强制删除 加个-f参数
docker rmi ID #删除镜像

#运行nginx镜像
docker run -d --name mynginx nginx:1.26.0 #后台启动nginx容器 这个容器命名为mynginx 现在这个容器运行在自己的环境内 从外部无法访问 使用端口映射才能访问
docker run -d --name mynginx -p 80:80 nginx:1.26.0 #这次多加了一个端口映射的参数 意思是把Docker Host的80端口映射到nginx单独环境的80端口 这样访问外部主机的时候就会访问到nginx了 注意 -p参数 Docker Host的端口不能有冲突 但是docker容器的端口是可以重复的 因为每个容器都是独立的一个Linux服务器

#以交互模式 bash进入nginx容器中 修改页面
docker exec -it mynginx /bin/bash
echo "nginx test" > /usr/share/nginx/html/inedx.txt
#访问

#批量删除所有容器
docker rm f- $(docker ps -aq) #里面的命令意思是把所有正在运行的容器id打印出来
```