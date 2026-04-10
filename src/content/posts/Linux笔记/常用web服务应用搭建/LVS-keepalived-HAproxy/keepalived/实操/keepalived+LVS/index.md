---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - keepalived - 实操 - keepalived+LVS"
category: "Linux笔记"
date: 2026-04-10
published: 2026-04-10
author: "Rin"
---

## 环境准备

- LVS1：192.168.0.116 BACKUP
- LVS2：192.168.0.117 MASTER
- Web1：192.168.0.118
- Web2：192.168.0.119

## 在MASTER上修改配置文件

```bash
#先装上keepalived和ipvsadm 注意ipvsad不要启动 keepalived集成了ipvsadm 会冲突
yum install -y keepalived ipvsadm

#修改配置文件
vim /etc/keepalived/keepalived.conf

#写入
!Configuration File for keepalived
global_defs {
router_id Director1 #两台LVS机子要不同命名
}

vrrp_instance VI_1 {
state MASTER #另外一台机器是BACKUP
interface ens33 #心跳网卡
virtual_router_id 51 #虚拟路由编号 主备一致
priority 150 #优先级
advert_int 1 #检查间隔 秒

authentication { #密码认证
auth_type PASS
auth_pass 1234
}

virtual_ipaddress {
192.168.0.20/24 dev ens33  #这里配的是VIP和工作接口 VIP要配一个没有被占用过的IP
}
}

virtual_server 192.168.0.20 80 { #LVS配置 VIP
delay_loop 3 #服务轮询的时间间隔 每3秒检查一次real_server状态
lb_algo rr #LVS调度算法
lb_kind DR #LVS集群模式
protocol TCP
real_server 192.168.0.118 80 { #后端服务器的IP
weight 1
TCP_CHECK {
connect_timeout 3 #健康检查方式 连接超时时间
}
}
}
real_server 192.168.0.119 80 {
weight 1
TCP_CHECK {
connect_timeout 3
}
}
}
```

## 在BACKUP写入和MASTER相同的配置

```bash
#直接用xftp把keepalived.conf传过去就行 如果是公网服务器直接远控上传
#如果是vmware环境下可以用下面的命令直接传
scp MASTER的IP:/etc/keepalived/keepalived.conf /etc/keepalived/
#输入MASTER的密码
#把配置改一下 改成BACKUP的
#修改
!Configuration File for keepalived
global_defs {
router_id Director2 #两台LVS机子要不同命名
}

vrrp_instance VI_1 {
state BACKUP
interface ens33 #心跳网卡
virtual_router_id 51 #虚拟路由编号 主备一致
priority 100 #优先级
advert_int 1 #检查间隔 秒

authentication { #密码认证
auth_type PASS
auth_pass 1234
}

virtual_ipaddress {
192.168.0.20/24 dev ens33  #这里配的是VIP和工作接口 VIP要配一个没有被占用过的IP
}
}

virtual_server 192.168.0.20 80 { #LVS配置 VIP
delay_loop 3 #服务轮询的时间间隔 每3秒检查一次real_server状态
lb_algo rr #LVS调度算法
lb_kind DR #LVS集群模式
protocol TCP
real_server 192.168.0.118 80 { #后端服务器的IP
weight 1
TCP_CHECK {
connect_timeout 3 #健康检查方式 连接超时时间
}
}
real_server 192.168.0.119 80 {
weight 1
TCP_CHECK {
connect_timeout 3
}
}
}
```

**两台LVS都配好之后 把keepalived启动**

```bash
systemctl start keepalived
systemctl enable keepalived
systemctl reload keepalived

#重启两台机子
reboot

#检查一下虚拟IP是否成功存在于MASTER
ip a
#如果没有 检查一下keepalived启没启动
#如果起不来 检查一下日志 看看是不是keepalived配置写错了
cat /var/log/messages
```

## 配置web服务器 两台都一样

```bash
#先下httpd
yum install -y httpd && systemctl start httpd && systemctl enable httpd

#装好之后查一下80端口起没起来
netstat -ntlp | grep 80
#或者
ss -anpt | grep 80

#配置虚拟地址
#这次用配置文件配 之前在DR模式的实操那里已经写过用ifconfig配的方法了
cp /etc/sysconfig/network-scripts/ifcfg-lo /etc/sysconfig/network-scripts/ifcfg-lo:0 #拷贝一份

#修改配置
vim /etc/sysconfig/network-scripts/ifcfg-lo:0

#修改
DEVICE=lo:0
IPADDR=192.168.0.20 #这里是改成keepalived的虚拟IP
NETMASK=255.255.255.255 #子网掩码
ONBOOT=yes #开机启动
#其它全部注释掉

#在后端机器上，添加一个路由：routeadd－host 192.168.0.20 dev lo:0确保如果请求的目标IP是$VIP，那么让出去的数据包的源地址也显示为$VIP 并且每次开机都生效
vim /etc/rc.local

#写入
/sbin/route add -host 192.168.0.20 dev lo:0

#配置arp
vim /etc/sysctl.conf

#写入
net.ipv4.conf.all.arp_ignore = 1
net.ipv4.conf.all.arp_announce = 2
net.ipv4.conf.default.arp_ignore = 1
net.ipv4.conf.default.arp_announce = 2
net.ipv4.conf.lo.arp_ignore = 1
net.ipv4.conf.lo.arp_announce = 2

#重启
reboot
```


**注意：实际在keepalived配置文件写的时候 注释要写在上面 不能写行尾 会报错**

## 测试

**把MASTER断了 看一下BACKUP的地址是否有keepalived的虚拟地址 再访问一下虚拟地址 如果能正常访问页面 就是配好了**