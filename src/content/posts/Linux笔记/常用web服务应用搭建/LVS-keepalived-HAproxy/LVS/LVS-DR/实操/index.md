---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - LVS - LVS-DR - 实操"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 环境
四台主机
- 客户机：192.168.2.106
- LVS：192.168.29.135 负载均衡器 虚拟IP：192.168.29.123
- web1：192.168.29.137 虚拟IP：192.168.29.123
- web2：192.168.29.136 虚拟IP：192.168.29.123

```bash
#LVS准备VIP和路由 ens33:0的意思是 给ens33这个网卡额外配置一个IP 因为LVS服务器需要一个对外的虚拟IP和对内的真实IP broadcast是配置广播地址 一般c段和前面一样 D段配置255 netmask是子网掩码 up是使配置生效
ifconfig ens33:0 192.168.29.123 broadcast 192.168.29.255 netmask 255.255.255.0 up

#配置路由 这个路由必须通过设备ens33:0通信 VIP和RIP要配置在同一个网卡上
route add -host 192.168.29.123 dev ens33:0

#设置路由转发
vim /etc/sysctl.conf
#写入
net.ipv4.ip_forward = 1 #开启路由功能
net.ipv4.conf.all.send_redirects = 0 #禁止转发重定向报文
net.ipv4.conf.ens33.send_redirects = 0 #禁止ens33转发重定向报文
net.ipv4.conf.default.send_redirects = 0 #禁止转发默认重定向报文

#设置负载均衡条目规则
#先安装一下包
yum install -y ipvsadm
ipvsadm -C #清除所有ipvs规则
ipvsadm -A -t 192.168.29.123:80 -s rr #启用轮询算法 对外的IP是192.168.29.123
ipvsadm -a -t 192.168.29.123:80 -r 192.168.29.137:80 -g 
ipvsadm -a -t 192.168.29.123:80 -r 192.168.29.136:80 -g

#配置永久生效
ipvsadm-save > /etc/sysconfig/ipvsadm
systemctl enable ipvsadm
```

## 配置web集群
```bash
#集群里的每个服务器都要执行以下流程
#先自己装个httpd服务和nginx
#修改一下内容 方便之后测试
vim /var/www/html/index.html
#自己想写什么就写什么

#启动服务
systemctl start httpd
systemctl enable httpd

#配置虚拟IP
#给web服务器的lo网卡设置子网掩码为32位vip lo是本机的虚拟网卡 该接口只用于测试 不用作通信 32位代表子网掩码是255.255.255.255 意思是这个子网掩码有且只有一个 而平常我们都写的是/24 代表的是255.255.255.0
ifconfig lo:0 192.168.29.123/32

#给web服务器设置内核参数
echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore #忽略arp响应 不允许收
echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce #为了让vip发包出去 但允许发
```

## 测试
```bash
#直接访问192.168.29.123就行
#如果出问题了可以用以下命令找问题
ipvsadm -Lnc #检查访问信息
ipvsadm -Ln  #检查本机的规则
```