---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - Script - LVS-NAT脚本配置"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

脚本1：lvs.sh 是配置在负载均衡端
脚本2：realserver.sh 是配置后端Real Server服务器上的
脚本3：check_lvs.sh 是用在负载均衡端上来测试后端服务器的健康状态的脚本，如有一个Real Server 宕机就会自动清除，如果恢复了就再加上，后端所有服务器都宕机了，会把负载均衡端提供的错误页面加到集群中来。

规划：

  负载均衡：

   DIP:192.168.1.11  

   VIP:192.168.1.10

  后台Real Server有两个分别为：

   rs1:192.168.1.9 

   rs2:192.168.1.8

```bash
#在负载均衡端安装ipvsadm和httpd服务，当在后端服务器都宕机时提供错误页面
yum install ipvsadm -y
yum install httpd -y

#在rs1,rs2上分别安装httpd服务,并启动服务，提供网页
yum install httpd -y

#在192.168.1.11服务器上编写脚本lvs.sh
cd /opt/scripts
vim lvs.sh

#写入
#!/bin/bash
#
# LVS script for VS/DR
# chkconfig: - 90 10
#
.  /etc/rc .d /init .d /functions
#
  
VIP=192.168.1.10
DIP=192.168.1.11
RIP1=192.168.1.9
RIP2=192.168.1.8
PORT=80
RSWEIGHT1=2
RSWEIGHT2=5
  
case  "$1"  in
     start)
         /sbin/ifconfig  eth0:0 $VIP broadcast $VIP netmask 255.255.255.255 up 
         #启用eth0:0来配置VIP
         /sbin/route  add -host $VIP dev eth0:0
         #添加VIP路由信息
  
         echo  1 >  /proc/sys/net/ipv4/ip_forward
         #打开ip转发功能
  
         /sbin/iptables  -F
         /sbin/iptables  -Z
         #清空iptables规则
         
         /sbin/ipvsadm  -C
         /sbin/ipvsadm  -A -t $VIP:80 -s wlc
         /sbin/ipvsadm  -a -t $VIP:$PORT -r $RIP1:$PORT -g -w $RSWEIGHT1
         /sbin/ipvsadm  -a -t $VIP:$PORT -r $RIP2:$PORT -g -w $RSWEIGHT2
         
         #添加ipvs规则
         
         /bin/touch  /var/lock/subsys/ipvsadm  &>  /dev/null
         #创建锁文件
     ;;
  
     stop)
         echo  0 >  /proc/sys/net/ipv4/ip_forward
  
         /sbin/ipvsadm  -C
         /sbin/ifconfig  eth0:0 down
         /sbin/route  del $VIP
  
         /bin/rm  -f  /var/lock/subsys/ipvsadm
  
         echo  "ipvs is stopped...."
     ;;
  
     status)
         if  [ ! -e  /var/lock/subsys/ipvsadm  ];  then
             echo  "ipvsadm is stopped ..."
         else
             echo  "ipvs is running ..."
             ipvsadm -L -n
         fi
     ;;
  
     *)
         echo  "Usge: $0 {start|stop|status}"
     ;;
esac
#此脚本可以加到系统服务列表中，并可以设置开机自动启动。
```

在后端服务器rs1和rs2中编写脚本realserver.sh

```bash
#!/bin/bash
#
# Script to start LVS DR real server.
# chkconfig: - 90 10
# description: LVS DR real server
#
.   /etc/rc .d /init .d /functions
 
VIP=192.168.1.10
 
host=` /bin/hostname `
 
case  "$1"  in
     start)
         /sbin/ifconfig  lo down
         /sbin/ifconfig  lo up
         echo  1 >  /proc/sys/net/ipv4/conf/lo/arp_ignore
         echo  2 >  /proc/sys/net/ipv4/conf/lo/arp_announce
         echo  1 >  /proc/sys/net/ipv4/conf/all/arp_ignore
         echo  2 >  /proc/sys/net/ipv4/conf/all/arp_announce
 
         /sbin/ifconfig  lo:0 $VIP broadcast $VIP netmask 255.255.255.255 up
         /sbin/route  add -host $VIP dev lo:0
     ;;
 
     stop)
         /sbin/ifconfig  lo:0 down
         echo  0 >  /proc/sys/net/ipv4/conf/lo/arp_ignore
         echo  0 >  /proc/sys/net/ipv4/conf/lo/arp_announce
         echo  0 >  /proc/sys/net/ipv4/conf/all/arp_ignore
         echo  0 >  /proc/sys/net/ipv4/conf/all/arp_announce
     ;;
 
     status)
         islothere=` /sbin/ifconfig  lo:0 |  grep  $VIP`
         isrothere=` netstat  -rn |  grep  "lo:0"  |  grep  $VIP`
         if  [ !  "$islothere"  -o !  "isrothere"  ]; then
             # Either the route or the lo:0 device
             # not found.
             echo  "LVS-DR real server Stopped."
         else
             echo  "LVS-DR real server Running."
         fi
     ;;
 
     *)
         echo  "$0: Usage: $0 {start|status|stop}"
         exit  1
     ;;
esac
```

完成后可以启动脚本了

LVS自身没有对后端服务器的健康状态检测功能，下面在192.168.1.11服务器上来使用脚本来每5s种检测下后台服务器健康状态，并实现自动清除宕机的服务器，恢复后可以自动添加

```bash
vim check_lvs.sh

#写入
#!/bin/bash
#
#
VIP=192.168.19.211
CPORT=80
FAIL_BACK=127.0.0.1
RS=( "192.168.19.245"  "192.168.19.219" )  #定义一个数组并赋值
declare  -a RSSTATUS  #定义一个空数组
RW=( "2"  "1" )
RPORT=80
TYPE=g  #定义为DR模型
CHKLOOP=3
LOG= /var/log/ipvsmonitor .log
 
  #定义一个添加规则的函数 
addrs() {
     if  ipvsadm -L -n |  grep  "$1:$RPORT"  &>  /dev/null ; then
         return  0
     else
         ipvsadm -a -t $VIP:$CPORT -r $1:$RPORT -$TYPE -w $2
         [ $? - eq  0 ] &&  return  0 ||  return  1
     fi
}
  
#定义删除规则的函数 
delrs() {
     if  ipvsadm -L -n |  grep  "$1:$RPORT"  &>  /dev/null ; then
         ipvsadm -d -t $VIP:$CPORT -r $1:$RPORT
         [ $? - eq  0 ] &&  return  0 ||  return  1
     else
         return  0
     fi
}
  
#定义是否要添加错误页面的规则的函数 
ifaddls() {
     if  [ ${RSSTATUS[0]} - eq  0 ]; then
         if  [ ${RSSTATUS[1]} - eq  0 ]; then
             if  ipvsadm -L -n |  grep  "127.0.0.1:80"  &>  /dev/null ; then
                 echo  "`date '+%F %T'` All RS is Down and Local web is up"  >> $LOG
             else
                 ipvsadm -a -t $VIP:$CPORT -r 127.0.0.1:80 -$TYPE
                 [ $? - eq  0 ];  echo  "`date '+%F %T'` All RS is Down! Local 127.0.0.1:80 is up!!!"  >> $LOG
             fi
         else
             if  ipvsadm -L -n |  grep  "127.0.0.1:80"  &>  /dev/null ; then
                 ipvsadm -d -t $VIP:$CPORT -r 127.0.0.1:80
             fi
         fi
     else
         if  ipvsadm -L -n |  grep  "127.0.0.1:80"  &>  /dev/null ; then
             ipvsadm -d -t $VIP:$CPORT -r 127.0.0.1:80
         fi
     fi
}
  
#定义检测后端服务器服务健康状态的函数  
checkrs() {
     local  I=1
     while  [ $I - le  $CHKLOOP ]; do
         if  curl --connect-timeout 1 http: // $1 &>  /dev/null ;  then
             return  0
         fi
         let  I++
     done
     return  1
}
 
#检测脚本初始化函数  
initstatus() {
     local  I
     local  COUNT=0
     for  I  in  ${RS[*]}; do
         if  ipvsadm -L -n |  grep  "$I:$RPORT"  && >  /dev/null ;  then
             RSSTATUS[$COUNT]=1
         else
             RSSTATUS[$COUNT]=0
         fi
         let  COUNT++
     done
}
#脚本开始执行： 
initstatus
ifaddls
  
while  :;  do  #无限循环
     let  COUNT=0
     for  I  in  ${RS[*]}; do
         if  checkrs $I;  then
             if  [ ${RSSTATUS[$COUNT]} - eq  0 ]; then
                 addrs $I ${RW[$COUNT]}
                 [ $? - eq  0 ] && RSSTATUS[$COUNT]=1 &&  echo  "`date '+%F %T'`, $I is back."  >> $LOG
             fi
         else
             if  [ ${RSSTATUS[$COUNT]} - eq  1 ];  then
                 delrs $I
                 [ $? - eq  0 ] && RSSTATUS[$COUNT]=0 &&  echo  "`date '+%F %T'`, $I is gone."  >> $LOG
             fi
         fi
         let  COUNT++
     done
     ifaddls
     sleep  5  #睡眠5s再循环
done
```

本文参考：[负载均衡之LVS--Shell脚本配置LVS-阿里云开发者社区](https://developer.aliyun.com/article/477385)