---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/搭建dns局域网/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 部署


```bash
#更新系统包
yum update -y

#安装bind以及相关工具
yum install bind -y

#配置文件位置
/etc/named.conf #主配置文件
/var/named/ #区域文件

#编辑主配置文件
vim /etc/named.conf
#写入
options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };        
        directory       "/var/named";        
        dump-file       "/var/named/data/cache_dump.db";                     statistics-file "/var/named/data/named_stats.txt";                   memstatistics-file "/var/named/data/named_mem_stats.txt";            recursing-file  "/var/named/data/named.recursing";                   secroots-file   "/var/named/data/named.secroots";                    allow-query     { any; };
};

#定义正向查询
zone "example.com" IN {
	type master;
    file "example.com.zone";
    allow-update { none; };
 };

#定义反向查询
zone "180.168.192.in-addr.arpa" IN {
	     type master;
         file "example.com.arpa";
         allow-update { none; };
 }; 
 
#检查是否语法错误
named-checkconf /etc/named.conf

#开始修改正反区域文件
#进入区域文件目录
cd /var/named/

#复制两份区域文件 方便一会使用
cp -p named.empty example.com.zone #正向解析
cp -p named.empty example.com.arpa #反向解析

#加入正向解析
vim example.com.zone

#写入
$TTL 1D
@       IN SOA  example.com. root.example.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        
@       IN NS   dns.example.com.
dns     IN A    192.168.29.50 
www     IN A    192.168.29.52  
exam    IN A    192.168.29.53
ftp     IN A    192.168.29.54
sun     IN A    192.168.29.55

#加入反向解析
vim example.com.arpa

#写入
$TTL 1D
@       IN SOA  example.com. root.example.com. (
                                        0           ; serial
                                        1D          ; refresh
                                        1H          ; retry
                                        1W          ; expire
                                        3H )     ; minimum
@       IN NS   dns.example.com.
50      IN PTR  dns.example.com. 
52      IN PTR  www.example.com. 
53      IN PTR  exam.example.com.
54      IN PTR  ftp.example.com.
55      IN PTR  sun.example.com.

#检查语法
named-checkzone example.com /var/named/example.com.zone
named-checkzone 29.168.192.in-addr.arpa /var/named/example.com.arpa #反向区域是29.168.192.in-addr.arpa 要和named.conf里zone的名称完全一致
#保存重启
systemctl restart named

#打开客户机
#将dns指向dns服务器
vim /etc/resolv.conf

#写入
nameserver 192.168.29.50

#正向解析测试
nslookup xxx.example.com #看IP地址是不是和自己配的一样

#反向解析测试
nslookup 192.168.29.x #看域名和自己配的是不是一样
```

## 主配置文件含义

```txt
options： 这个部分包含了DNS服务器的一般选项设置。

  

listen-on port 53 { any; }： 指定DNS服务器监听的端口。在这个示例中，DNS服务器监听在53端口，允许任何IP地址连接到该端口。这意味着DNS服务器会接受来自任何IP地址的DNS查询请求。

  

listen-on-v6 port 53 { ::1; }： 指定IPv6地址的监听端口。在这个示例中，DNS服务器监听IPv6地址的53端口，只允许本地IPv6地址（::1）连接到该端口。

  

directory "/var/named";： 指定存储DNS服务器相关数据文件的目录路径。在这个示例中，数据文件存储在/var/named目录下。

  

dump-file "/var/named/data/cache_dump.db";： 指定DNS服务器在关闭时将缓存内容写入的文件路径。这个文件通常用于调试和故障排除。

  

statistics-file "/var/named/data/named_stats.txt";： 指定DNS服务器的统计信息输出文件路径，用于记录DNS服务器的运行统计数据。

  

memstatistics-file "/var/named/data/named_mem_stats.txt";： 指定DNS服务器的内存使用统计输出文件路径，用于记录DNS服务器的内存使用情况。

  

recursing-file "/var/named/data/named.recursing";： 指定DNS服务器递归查询的记录文件路径。

  

secroots-file "/var/named/data/named.secroots";： 指定DNS服务器的安全根文件路径。

  

allow-query { any; };： 指定允许查询的IP地址范围。在这个示例中，允许任何IP地址进行DNS查询。






type master;: 表明这是主 DNS 服务器，负责提供 "example.com" 区域的数据。

  

file "example.com.zone";: 指定了包含 "example.com" 区域数据的文件的路径。

  

allow-update { none; };: 指定了允许对区域进行动态更新的权限。在这种情况下，none 表示不允许任何动态更新，因此区域数据只能通过手动编辑区域文件来更新。
```

## 正向配置文件含义

```txt
example.com.: 指定了主域名为 example.com。

  

root.example.com.: 这个字段指定了负责管理该域名的DNS服务器的邮箱地址，形式为 root@example.com。root 是指定了这个域名的管理员（或者叫根管理员），而 example.com 是该管理员的邮箱地址的域名部分。

  

@ IN NS dns.example.com.：这行指定了域名 example.com 的DNS服务器是 dns.example.com。NS记录（Name Server）指定了管理特定区域的DNS服务器。

  

dns IN A 192.168.180.188：这行指定了主机名 dns 对应的IP地址是 192.168.180.188。A记录（Address Record）用于将域名解析为IPv4地址。

  

www IN A 192.168.180.189：这行指定了主机名 www 对应的IP地址是 192.168.180.189。

  

exam IN A 192.168.180.190：这行指定了主机名 exam 对应的IP地址是 192.168.180.190。

  

ftp IN A 192.168.180.191：这行指定了主机名 ftp 对应的IP地址是 192.168.180.191。

  

sun IN A 192.168.180.44：这行指定了主机名 sun 对应的IP地址是 192.168.180.44。
```

## 反向配置文件含义

```txt
PTR 记录将 IP 地址映射到相应的域名。

  

@ IN NS dns.example.com.：这行指定了该反向区域的DNS服务器是 dns.example.com。NS记录（Name Server）指定了管理特定区域的DNS服务器。

  

188 IN PTR dns.example.com.：这行指定了IP地址以 188 结尾的主机对应的域名是 dns.example.com。PTR记录（Pointer Record）用于将IP地址解析为域名。

  

189 IN PTR www.example.com.：这行指定了IP地址以 189 结尾的主机对应的域名是 www.example.com。

  

190 IN PTR exam.example.com.：这行指定了IP地址以 190 结尾的主机对应的域名是 exam.example.com。

  

191 IN PTR ftp.example.com.：这行指定了IP地址以 191 结尾的主机对应的域名是 ftp.example.com。

  

44 IN PTR sun.example.com.：这行指定了IP地址以 44 结尾的主机对应的域名是 sun.example.com。
```

参考：[CentOS使用BIND搭建DNS服务器并配置正反向解析-开发者社区-阿里云](https://developer.aliyun.com/article/1501006)