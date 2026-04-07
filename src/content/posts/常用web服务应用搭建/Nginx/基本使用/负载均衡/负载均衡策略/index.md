---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/负载均衡策略/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 权重、down、backup

```bash
 #定义一组服务器
 #按照每10次访问中 8次访问888这个服务器 2次访问7777这个服务器的权重来分
    upstream servertest {
        server 192.168.29.50:888 weight=8;
        server 192.168.29.50:7777 weight=2;
    }
    
        #定义一组服务器
#写了down之后 888这台机器就不参与负载均衡了 也就是不会被访问到
    upstream servertest {

        server 192.168.29.50:888 weight=8 down;
        server 192.168.29.50:7777 weight=2;
 }
    
    
        #定义一组服务器
#写了backup之后 这台机器就会被当作备用机 正常情况下不会访问这台机器 只有当其它机器都出故障了才会访问这台机器
    upstream servertest {

        server 192.168.29.50:888 weight=8 backup; 
        server 192.168.29.50:7777 weight=2;  
    }
```


## ip_hash、fair、leastconn与无状态会话解决方案

- ip_hash:根据客户端ip地址转发同一台服务器 可以保持会话
- least_conn:最少连接访问
- url_hash:根据用户访问的url定向转发请求
- fair:根据后端服务器的响应时间来转发请求

**这四种方式一般都不会使用 因为这四种方式都不能以服务器集群的方式来动态上下线服务器 如果真的要用这些功能 可以使用LUA脚本的方式在nginx进行编程来自定义转发规则**

**状态保持需要在服务器里存session 之后用户用cookie来登陆 如果把session存储到集群中的一台服务器中 用户下次操作有可能就会访问集群的另外一台服务器 那么那台服务器中没有存这个用户的session 就会导致用户需要重新登陆 无法保持状态
其中一个解决方法就是不把session存到集群的任何一台服务器上 而是单开一台数据库服务器来存session 通过修改配置文件使服务器需要使用session的时候不从服务器本身去找 而是在数据库服务器去找  -> 这种方式只能在小项目中使用 并不适用于大规模高并发的项目 高并发的场景需要用到真正的无状态会话 即下发token**