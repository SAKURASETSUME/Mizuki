---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - 水平分表"
category: "Linux笔记"
date: 2026-04-23
published: 2026-04-23
author: "Rin"
---

## 场景
```txt
在业务系统中 有一张表（日志表） 业务系统每天都会产生大量的日志数据 单台服务器的数据存储及处理能力是有限的 可以对数据库表进行拆分
```

## 思路
```txt
对tb_log进行水平拆分
在Mycat中定义逻辑表tb_log
这张逻辑表中的数据要均匀分散在节点当中
```

## 环境准备
- MyCat -> 192.168.200.210
- MySQL -> 192.168.200.210
- MySQL -> 192.168.200.213
- MySQL -> 192.168.200.214

```mysql
在三台MySQL服务器上创建数据库
create database itcast;
```

## schema.xml
```xml
<schema name="itcast" checkSQLschema="true" sqlMaxLimit="100" randomDataNode="dn1">
        <table name="tb_log" dataNode="dn4,dn5,dn6" rule="mod-long" primaryKey="id"/>
    </schema>
    
    <dataNode name="dn4" dataHost="dhost1" database="itcast" />
    <dataNode name="dn5" dataHost="dhost2" database="itcast" />
    <dataNode name="dn6" dataHost="dhost3" database="itcast" />
    
    <dataHost name="dhost1" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.210:3306/itcast?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>
    <dataHost name="dhost2" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.213:3306/itcast?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>

    <dataHost name="dhost3" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.214:3306/itcast?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>
```

## server.xml
```xml
  
    <user name="mycat" defaultAccount="true">

        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->

        <property name="schemas">shopping,itcast</property>

        <property name="defaultSchema">shopping</property>

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

  

    <user name="user">

        <property name="password">user</property>

        <property name="schemas">shopping,itcast</property>

        <property name="readOnly">true</property>

        <property name="defaultSchema">shopping</property>

    </user>
```

## rule.xml
```xml
<!--这里的3代表的是根据主键取模的数字 可以自行配置-->
	<function name="mod-long" class="io.mycat.route.function.PartitionByMod">
		<!-- how many data nodes -->
		<property name="count">3</property>
	</function>
```
## 测试
```bash
cd /usr/local/mycat
bin/mycat stop
bin/mycat start
tail -f log/wrapper.log

#登录mycat
mysql -h 192.168.200.210 -P 8066 -uroot -p
```

```mysql
show databases;
use itcast;
show tables;
#自己在真实服务器提前创建好了itcast这个数据库和tb_log这个表 MyCat中存在的只是逻辑表 真实服务器中如果没有这个表或者数据库 执行会报错
#自行导入数据
source /root/log.sql

#查看数据 如果数据是按主键取模 均衡分布的 配置就成功
```