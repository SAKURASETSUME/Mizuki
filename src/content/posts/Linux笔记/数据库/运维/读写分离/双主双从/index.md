---
title: "Linux笔记 - 数据库 - 运维 - 读写分离 - 双主双从"
category: "Linux笔记"
date: 2026-04-30
published: 2026-04-30
author: "Rin"
---

## 介绍
一个主机Master1用于处理所有写请求，它的从机Slave1和另一台主机Master2还有它的从机Slave2负责所有读请求。当Master1主机宕机后，Master2主机负责写请求，Master1 、Master2互为备机 互相复制。

## 搭建
五台服务器准备：
- MyCat：192.168.200.210
- MySQL：192.168.200.211 -> MATSR1
- MySQL：192.168.200.212 -> SLAVE1
- MySQL：192.168.200.213 -> MASTER2
- MySQL：192.168.200.214 -> SLAVE2

### 主库配置
Master1(192.168.200.211)
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#mysql服务ID 保证整个集群环境中唯一 取值范围：1-2^32 -1 默认为1
server-id=1
#指定同步的数据库 即要进行主从复制的数据库
binlog-do-db=db01
binlog-do-db=db02
binlog-do-db=db03
#在作为从数据库的时候 有写入操作也要更新二进制日志文件
log-slave-updates

#重启mysql
systemctl restart mysqld
```

Master2(192.168.200.213)
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#mysql服务ID 保证整个集群环境中唯一 取值范围：1-2^32 -1 默认为1
server-id=3
#指定同步的数据库 即要进行主从复制的数据库
binlog-do-db=db01
binlog-do-db=db02
binlog-do-db=db03
#在作为从数据库的时候 有写入操作也要更新二进制日志文件
log-slave-updates

#重启mysql
systemctl restart mysqld
```

### 创建用于主从复制的账号
```mysql
#两台主库中都要执行
#登陆mysql
#创建itcast用户 并设置密码 该用户可以在任意主机连接该MySQL服务
create user 'itcast'@'%' identified with mysql_native_password by 'Root@123456';
#为'itcast'@'%'用户分配主从复制权限
grant replication slave on *.* to 'itcast'@'%';

#查看二进制日志坐标 记住位置
show master status;
```

### 丛库配置

Slave1(192.168.200.212)
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#mysql服务ID 保证整个集群环境中唯一 取值范围：1-2^32 -1 默认为1
server-id=2

#重启mysql
systemctl restart mysqld
```

Slave2(192.168.200.214)
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#mysql服务ID 保证整个集群环境中唯一 取值范围：1-2^32 -1 默认为1
server-id=4

#重启mysql
systemctl restart mysqld
```

### 把slave和master关联起来
slave1(192.168.200.212)
```mysql
#在两个从库分别执行
#登陆mysql
change master to master_host='192.168.200.211',master_user='itcast',master_password='Root@123456',master_log_file='binlog_000002',master_log_pos=663;

#启动主从复制 查看从库状态
start slave;
show slave status;\G
```

slave2(192.168.200.214)
```mysql
#登陆mysql
change master to master_host='192.168.200.213',master_user='itcast',master_password='Root@123456',master_log_file='binlog_000002',master_log_pos=663;

#启动主从复制 查看从库状态
start slave;
show slave status;\G
```

### 把master1和master2关联起来
两台主库相互复制
master1(192.168.200.211)
```mysql
change master to master_host='192.168.200.213',master_user='itcast',master_password='Root@123456',master_log_file='binlog_000002',master_log_pos=663;

start slave;
show slave status;\G
```

master2(192.168.200.213)
```mysql
change master to master_host='192.168.200.211',master_user='itcast',master_password='Root@123456',master_log_file='binlog_000002',master_log_pos=663;

start slave;
show slave status;\G
```

### 测试
在master1插入数据 看看数据会不会同步到master2、slave1、slave2
在master2插入数据 看看数据会不会同步到master1、slave1、slave2

## 读写分离
MyCat控制后台数据库的读写分离和负载均衡由schema.xml文件datahost标签的balance属性控制，通过writeType及switchType来完成失败自动切换的。
schema.xml
```xml
    <schema name="ITCAST_RW2" checkSQLschema="true" sqlMaxLimit="100" dataNode="dn7">
    </schema>
    
    <dataNode name="dn7" dataHost="dhost7" database="db01" />
    
    
    
        <dataHost name="dhost7" maxCon="1000" minCon="10" balance="1"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <!-- can have multi write hosts -->
        <writeHost host="master1" url="jdbc:mysql://192.168.200.211:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02">
                   
                  <readHost host="slave1" url="jdbc:mysql://192.168.200.212:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02">
                   </readHost>
        </writeHost>
        <!-- <writeHost host="hostM2" url="localhost:3316" user="root" password="123456"/> -->
        
        <writeHost host="master2" url="jdbc:mysql://192.168.200.213:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02">
                   
                  <readHost host="slave2" url="jdbc:mysql://192.168.200.214:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02">
                   </readHost>
        </writeHost>
    </dataHost>
```

server.xml
```xml
<user name="mycat" defaultAccount="true">
        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->
        <property name="schemas">ITCAST_RW2</property>
        <property name="defaultSchema">db01</property>
        <!--No MyCAT Database selected 错误前会尝试使用该schema作为schema，不设置则为null,报错 -->
        <!-- 表级 DML 权限设置 -->
        <!--        
        <privileges check="false">
            <schema name="TESTDB" dml="0110" >
                <table name="tb01" dml="0000"></table>
                <table name="tb02" dml="1111"></table>
            </schema>
        </privileges>      
         -->
    </user>
```

balance=1 ：代表全部的readHost与stand by writeHost参与select语句的负载均衡 简单地说 当双主双从模式正常情况下 M2 S1 S2都参与select语句的负载均衡

writeType：
- 0：写操作都转发到第一台writeHost， writeHost1挂了 会切换到writeHost2上
- 1：所有的写操作都随机地发送到配置噩writeHost上

switchType
- -1：不自动切换
- 1：自动切换

### 测试读写分离
登陆MyCat 测试查询以及更新操作 判断是否能正常进行读写分离 以及读写分离的策略是否正确
查询的测试方法：在从库更新一条测试数据 从库更新的数据不会同步到主库 执行查询语句 看测试数据是否是被更改过的（如果能正常查到被更改过的数据 但是还能查询到没被更改过的数据 那就是备用主库的数据 并不是配置失效了）
更新的测试方法：在MyCat执行更新数据操作 查看另外三台服务器是否正常更新

当主库挂掉一个后 是否能够自动切换（测试查询、插入是否正常执行）