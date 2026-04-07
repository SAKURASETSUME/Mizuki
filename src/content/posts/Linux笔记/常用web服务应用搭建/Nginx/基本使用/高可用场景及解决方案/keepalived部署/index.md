---
title: "keepalived部署"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/常用web服务应用搭建/Nginx/基本使用/高可用场景及解决方案/keepalived部署/
categories:
  - Linux笔记
  - 常用web服务应用搭建
  - Nginx
  - 基本使用
  - 高可用场景及解决方案
  - keepalived部署
tags:
  - Study
---

```bash
#yum安装
yum install keepalived

#配置文件位置
/etc/keepalived/keepalived.conf
```

```bash
#主配置文件最小配置
! Configuration File for keepalived

  

global_defs {

   router_id lb52 #自己改下 方便记忆

  

}

  

#这个方法名也可以改成自己方便记的

vrrp_instance nakatsusizuru {

    state MASTER

    interface ens33 #自己记住网卡名字 这里要改

    virtual_router_id 51

    priority 100

    advert_int 1

    authentication {

        auth_type PASS

        auth_pass 1111

    }

    virtual_ipaddress { #虚拟IP 可以写很多个 注意C段和自己的IP对上

        192.168.29.111

    }

}
```

```bash
#备份配置文件
! Configuration File for keepalived

  

global_defs {

   router_id lb53 #自己改下 方便记忆

  

}

  

#这个方法名也可以改成自己方便记的

vrrp_instance nakatsusizuru {

    state BACKUP

    interface ens33 #自己记住网卡名字 这里要改

    virtual_router_id 51

    priority 50

    advert_int 1

    authentication {

        auth_type PASS

        auth_pass 1111

    }

    virtual_ipaddress { #虚拟IP 可以写很多个 注意C段和自己的IP对上

        192.168.29.111

    }

}
```

```bash
#配置完之后手动启动
systemctl start keepalived
systemctl enable keepalived
```

**注意 主机和备用机的keepalived版本要一样 不然会导致漂移失败**
