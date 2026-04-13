---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - HAproxy - 实操 - 简单使用"
category: "Linux笔记"
date: 2026-04-13
published: 2026-04-13
author: "Rin"
---

## 环境准备

- 客户机：192.168.122.1/24
- HAproxy：192.168.122.254/24
- web1：192.168.122.10/24
- web2：192.168.122.20/24

## 操作步骤

```bash
#两台web做个测试页
#第一台web
yum install -y httpd
echo web1 > /var/www/html/index.html

#第二台web上
yum install -y httpd
echo web2 > /var/www/html/index.html

#负载均衡器配置
#安装HAproxy
yum install -y epel-release
yum install -y haproxy

#配置HAproxy
vim /etc/haproxy/haproxy.cfg

#haproxy配置的五部分内容 看下面的表格

#配置示例
global #全局配置

        log 127.0.0.1 local3 info #日志配置

        maxconn 4096 #最大连接数

    user nobody #用户

#   uid 99 #这个也是用户配置

    group nobody #组用户

#   gid 99

        daemon #守护进程运行 常驻系统内存

        nbproc 1 #haproxy进程数 该值的设置应该和服务器的CPU核心数一致

        pidfile /run/haproxy.pid #haproxy的进程id存储位置

defaults #默认配置

        log         global  #日志配置按照全局配置中的配置进行配置

        mode    http #模式 配置haproxy到底工作在第七层(http 检查URL)还是第四层(tcp 检查IP:port)

        maxconn 2048 #最大连接数

        retries 3 #健康检查的次数 3次连接失败就认为服务不可用

        option redispatch #服务不可用后的操作 这里配置的是重定向到其它服务器

        contimeout 5000 #三个计时器 这一条是haproxy把客户端请求转发给服务器所等待的超时时长

        clitimeout 50000 #haproxy作为客户 和后端服务器之间空闲连接的超时时间

        srvtimeout 50000 #haproxy作为服务器 和客户机之间空闲连接的超时时间

#timeout connect 5000 #旧版写法 这个也能用

#timeout client 50000

#timeout server 50000        

    option abortonclose #当服务器负载很高的时候 自动结束掉当前队列处理比较久的链接

  

    stats uri /admin?stats #设置统计页面的uri为/admin?stats

    stats realm Private lands #设置统计页面认证时的提示内容

    stats auth admin:password #设置统计页面认证的用户和密码 如果要设置多个 另起一行写入即可

    stats hide-version #隐藏统计页面上的haproxy版本信息

  

frontend http-in #前端配置

  

    bind 0.0.0.0:80 #对外提供服务的绑定地址 这里配置的是haproxy这个机器拥有的全部ip都会转发

    mode http #面对前端的模式 这里是检查url

    log global #日志配置

    option httplog #日志配置

    option httpclose #关闭在队列时间长的空闲连接

 acl html url_reg -i \.html$ #访问控制列表名称html 规则要求访问以html结尾的url时

 use_backend html-server if html #如果满足acl html规则 则推送给后端服务器 html-server

 default_backend html-server #默认的后端服务器是html-server 如果用户访问的不是以html结尾的url时 那么就把请求转发给html服务器

  

 backend html-server #后端服务器名称为html-server

        mode http

        balance roundrobin #轮询

        option httpchk GET /index.html #以GET方式去请求服务器后端的网页 如果和上面配置的一样 3次健康检查之后没反应 就认为服务器宕机 转发给集群中的另外的服务器

        cookie SERVERID insert indirect nocache #缓存服务器的ID 并插入到对用户的回复中 这个配置可以实现让用户在携带同一cookie访问时 访问到同一台服务器

        server html-A web1:80 weight 1 cookie 3 check inter 2000 rise 2 fall 5 # cookie 3 服务器ID 避免rr算法将客户机请求转发给其它服务器 ui后端服务器的健康状况检查为2000ms 连续2次健康检查成功 则认为是有效的 连续5次健康检查失败 则认为服务器宕机

        server html-A web2:80 weight 1 cookie 4 check inter 2000 rise 2 fall 5  # 服务器名在这里配置之后 需要单独做域名解析
```

## 域名解析

```bash
#四台都要配 可以只给一台客户机配 用scp拷过去
vim /etc/hosts

#写入
192.168.122.1 client
192.168.122.254 haproxy
192.168.122.10 web1
192.168.122.20 web2

#跨主机拷贝
scp /etc/hosts haproxy:/etc/
scp /etc/hosts web1:/etc/
scp /etc/hosts web2:/etc/


```

## 测试
```bash
#查看日志内容
cat /var/log/message

#访问HAproxy网站就可以测试了
```

| 字段       | 配置内容                                         |
| -------- | -------------------------------------------- |
| global   | 设置全局配置参数 属于进程的配置 通常和操作系统有关                   |
| defaults | 配置默认参数 这些参数可以被用到frontend backend Listen组件    |
| frontend | 接收请求的前端虚拟节点 Frontend可以更加规则直接指定具体使用后端的backend |
| backend  | 后端服务集群的配置 是真实服务器 一个Backend对应一个或多个实体服务器       |
| Listen   | frontend和backend的组合体                         |