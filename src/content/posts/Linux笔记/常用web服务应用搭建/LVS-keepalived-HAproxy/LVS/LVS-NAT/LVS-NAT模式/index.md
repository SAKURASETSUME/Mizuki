---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - LVS - LVS-NAT - LVS-NAT模式"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 实验环境

### 方案一
两台可以互通的机器：
- 公网主机1：47.86.1.42
- 公网主机2：119.84.246.218
- 公网主机2内网IP：192.168.29.100

与公网主机2处于同一局域网的服务器：
- 服务器1:192.168.29.52
- 服务器2:192.168.29.50

ps:这两台服务器之间也要互通 用vmware就可以

### 方案2

使用Vmware的Vmnet功能就能实现

想要让两台虚拟机处于同一局域网中 只需要让两台虚拟机的网卡使用同一个虚拟网卡就可以了

具体教程:[007.大型网站高并发集群LVS-LVS-NAT模式实验环境_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1gz4y1y7Nx/?p=7&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=05d71ca20d1a62ee1c802b01999e7379)

## 实验架构

client -> 公网主机1 这台主机只需要能通LVS服务器就可以
LVS -> 公网主机2 这台主机既要能通client 又要和server web处于同一局域网下
server web -> 两台内网服务器

## 实操

**为了更直观 虽然使用的是方案二的操作流程 但是IP地址都使用方案一的IP地址**

这里以方案二为例

**先把IP都配好 LVS服务器注意要配两块虚拟网卡**

**这里两台内网服务器是不通外网的 但是测试需要 建议先连上外网 下个httpd的服务 再改回内网环境**

这里为了测试方便 把防火墙和selinux也关了

### web1服务器

```bash
#先部署好httpd
yum install -y httpd
systemctl start httpd
systemctl status httpd
systemctl enable httpd

#做个测试页出来
echo web1 > /var/www/html/index.html

#配置路由 把外网ip引导至LVS服务器上 -net参数是外部网络 gw是网关 也就是网络的出口
route add -net 外网ip(注意这里要写整个网段 比如外网ip是47.86.1.42 那你就要写47.86.1.0)/24 gw LVS内网ip
```

### web2服务器

**这里为了更直观 把ip配成方案一写过的ip**

```bash
yum install -y httpd
systemctl start httpd
systemctl status httpd
echo web2 > /var/www/html/index.html
route add -net 47.86.1.0/24 gw 192.168.29.100
```

### LVS服务器

```bash
#启动路由功能
echo 1 > /proc/sys/net/ipv4/ip_forward

#部署ip虚拟服务管理器 也就是LVS
yum install -y ipvsadm

#这里配的是LVS在外网的地址 -A指对外提供的地址  -t指tcp端口 -s指策略 rr就是轮询策略
ipvsadm -A -t 119.84.246.218:80 -s rr

#-a是指对内的服务器 所以后面两个服务器要配内网的服务器 -m是指NAT模式
ipvsadm -a -t 119.84.246.218:80 -r 192.168.29.52:80 -m
ipvsadm -a -t 119.84.246.218:80 -r 192.168.29.50:80 -m
```

### 测试

使用客户机访问LVS服务器就可以了

```bash
#Linux环境下
elink --dump 119.84.246.218 #如果没有的话就用yum自己装
#或者用curl
curl 119.84.246.218

#如果你是windows那应该就不用我教了
```

## 整个过程总结

**把客户机的IP称为CIP LVS的外网IP称为VIP 内网IP称为DIP 两台服务器的IP称为VIP1和VIP2**

当客户机访问目标站点的时候 IP地址是这样转变的：源地址为CIP 目标地址为VIP -> 当请求发送到LVS服务器的时候 源地址还是CIP 但是目标地址会被转换成VIP1或VIP2 -> 服务器的其中一台收到请求之后 会把响应发送给LVS 这时源地址为VIP1或者VIP2 目标地址为CIP -> LVS收到服务器的响应后 将响应转发给客户机 这时源地址为VIP 目标地址为CIP

## 优缺点

- 优点：
网络隔离 安全性较高
节约IP地址

- 缺点：
所有的信息都需要经过LVS服务器的转发 所以LVS服务器的压力很大 很有可能成为系统的性能瓶颈 一般来说小于20台服务器就可以用LVS-NAT模式 再高了带宽就跟不上了