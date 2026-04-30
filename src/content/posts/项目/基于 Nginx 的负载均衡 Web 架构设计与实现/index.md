---
title: "项目 - 基于 Nginx 的负载均衡 Web 架构设计与实现"
category: "项目"
date: 2026-04-30
published: 2026-04-30
author: "Rin"
---



## 项目思路

搭建一个通过Nginx实现负载均衡的架构

## 环境准备

- Nginx 192.168.29.138
- web1 192.168.29.142
- web2 192.168.29.143

## 实现步骤

### web服务器

搭建测试页面

```bash
#下载httpd服务
yum install -y httpd
#写一个测试页面
echo "web1" > /var/www/html/index.html
#另外一个web服务器同样的步骤
echo "web2" > /var/www/html/index.html

#如果访问不了 就在防火墙把80端口开了
firewall-cmd --zone=public --add-port=80/tcp --permanent

#测试页面搭建好了
```



### nginx服务器搭建

```bash
#安装nginx
#使用wget命令下tar包
wget https://nginx.org/download/nginx-1.20.2.tar.gz

#解压
tar -zxvf nginx-1.20.2.tar.gz -C /usr/local/

#安装依赖
yum install -y gcc
yum install -y pcre pcre-devel
yum install -y zlib zlib-devel

#安装
./configure --prefix=/usr/local/nginx

#编译
make
make install

#修改配置文件
vim /usr/local/nginx/conf/nginx.conf
#修改
upstream servertest {
		ip_hash;
        server 192.168.29.142:80 weight=7;
        server 192.168.29.143:80 weight=3;
}
    server {
        listen       80;
		#server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
          proxy_pass      http://servertest;  
        }
        
        
#开放防火墙80端口
firewall-cmd --zone=public --add-port=80/tcp --permanent
#重载防火墙配置
systemctl reload firewalld
```

## 访问测试

```bash
#访问192.168.29.138
#web1和web2交替显示 负载均衡配置正确
#模拟节点宕机
#web1的httpd服务关闭
systemctl stop httpd
#访问nginx 查看负载均衡是否正常工作
#只显示web2 工作正常

#模拟配置文件ip错误
server 192.168.29.144 weight 2;
#发现有一个页面访问异常 被重定向到web1了
#查看日志
cat /usr/local/nginx/logs/error.log

2026/04/30 15:15:11 [error] 7812#0: *5 connect() failed (113: No route to host) while connecting to upstream, cl
ient: 192.168.29.1, server: , request: "GET / HTTP/1.1", upstream: "http://192.168.29.144:80/", host: "192.168.2
9.138"
#定位问题 nginx和192.168.29.144连接失败了 修改配置文件改回143 正常运行
```

## nginx进阶配置

```bash
#配置会话保持
upstream servertest {
    ip_hash;
    server 192.168.29.142:80;
    server 192.168.29.143:80;
}
#测试 用同一台主机访问nginx 获得的页面应该是同一个

#配置最少连接 当前请求将被发送到保持连接数最少的服务器
upstream servertest {
    least_conn;
    server 192.168.29.142:80;
    server 192.168.29.143:80;
}

#加入健康状态参数 10s内连接失败两次 就把失败服务器禁用10s
upstream servertest {
    server 192.168.29.142:80 max_fails=2 fail_timeout=10s;
    server 192.168.29.143:80 max_fails=2 fail_timeout=10s;
}

#测试 把web1停了 连续访问nginx 会发现一开始有时会卡一下 这就是在访问web1 后面就会只访问web2了

#配置proxy头和超时控制 host参数是把客户端请求的host头传给后端的 比如用户访问www.test.com 如果你不配置host参数 那么后端看到的是nginx服务器的ip 配了之后 后端看到的就是www.test.com了
#X-Real-IP这个参数 作用是把客户端的真实IP传给后端 如果不加 192.168.29.1访问nginx 那么后端日志看到的IP就是nginx服务器的IP了 加了之后 后端就可以拿到192.168.29.1
#proxy_connect_timout控制的是连接时间 如果配置了这个参数 当客户端与服务器连接时间超过3s的时候 那么客户端会直接看到连接超时的页面
#proxy_read_timeout控制的是响应时间 配置之后 当客户端成功与服务器建立连接 但是一定时间内没有被服务器响应 就会返回错误页面
#这两条超时时间如果想要在超时之后定向到其它服务器 需要额外配置参数proxy_next_upstream
location / {
    proxy_pass http://servertest;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_connect_timeout 3s;
    proxy_read_timeout 5s;
}
```



## 最终配置

```bash
upstream servertest {
		least_conn;
        server 192.168.29.142:80 weight=7 max_fails=2 fail_timeout=10s;
        server 192.168.29.143:80 weight=3 max_fails=2 fail_timeout=10s;
}
    server {
        listen       80;
		#server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

 location / {
    proxy_pass http://servertest;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_connect_timeout 3s;
    proxy_read_timeout 5s;
}
```



## 后续优化方向(暂定 慢慢实现)

- 通过keepalived来实现双nginx架构
- 使用docker部署此项目