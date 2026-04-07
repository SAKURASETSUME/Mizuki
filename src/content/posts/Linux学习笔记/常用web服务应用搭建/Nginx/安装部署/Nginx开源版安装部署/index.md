---
title: "Nginx开源版安装部署"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/常用web服务应用搭建/Nginx/安装部署/Nginx开源版安装部署/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#自己在本机下 下完传过去
tar -zxvf nginx-1.20.2

cd nginx-1.20.2/

#安装依赖
yum install -y gcc
yum install -y pcre pcre-devel
yum install -y zlib zlib-devel

#安装
./configure --prefix=/usr/local/nginx #这里是安装路径

#接下来执行
make 
make install

#手动启动
cd sbin
./nginx

#验证服务是否启动成功 默认监听80端口
./nginx #启动
./nginx-s stop #快速停止
./nginxI-s quit #优雅关闭，在退出前完成已经接受的连接请求
./nginx-s reload #重新加载配置

#把nginx安装成系统服务
#新建并配置
vim /usr/lib/systemd/system/nginx.service
#写入 如果安装路径不同 自己改一下配置文件的路径
[Unit]
Description=nginx - web server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/usr/local/nginx/sbin/nginx -s stop
PrivateTmp=true

[Install]
WantedBy=multi-user.target

#重新加载系统服务
systemctl daemon-reload

#检查一下nginx是否在运行
ps -aux | grep nginx
#如果在运行就关一下
./nginx -s stop

#启动服务
systemctl start nginx.service

#设置开机启动
systemctl enable nginx.service

#容器（Docker）安装
```