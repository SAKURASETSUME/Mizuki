---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - keepalived - 实操 - 简单使用"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 实现web服务器的高可用集群

- Server1:192.168.0.118
- Server2:192.168.0.119
- VIP：192.168.0.10

```bash
#先安装keepalived
yum install -y keepalived

#编辑配置文件
vim /etc/keepalived/keepalived.conf

#写入
!Configuration File for keepalived
global_defs {
router_id 1 #设备在组中的标识 设置不一样就行
}

#vrrp_script chk_nginx {  #健康检查
#script "/etc/keepalived/ck_ng.sh" #检查脚本 这里是脚本名 自己和实际的脚本名对照一下
#interval 2 #检查频率 秒
#weight -5 #priority减5
#fall 3 #失败三次
#}

vrrp_instance VI_1 { #VI_1 实例名两台路由器相同
state MASTER #主或从状态
interface ens33 #监控插心跳线的网卡
mcast_src_ip 192.168.0.118 #心跳源IP
virtual_router_id 55 #虚拟路由编号 主备要一致
priority 100 #优先级
advert_int 1 #心跳间隔

 authentication { #秘钥认证(1-8位)
 auth_type PASS
 auth_pass 123456
 }
 
 virtual_ipaddress { #VIP
 192.168.0.10/24
 }
 
 # track_script { #引用脚本
 # chk_nginx
 #}
}

#启动起来
systemctl start keepalived.service
systemctl enable keepalived.service

#自己装个nginx 改一下默认页面区分主机从机

#去从机服务器
#同样装个keepalived
#配置文件把router_id改一下
#把MASTER改成BACKUP
#网络接口如果不一样就改一下
#心跳源IP地址变一下
#优先级改一下

#重启keepalived
systemctl restart keepalived
#装一下nginx 改默认页面 然后连接192.168.0.10测试
```