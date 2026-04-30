---
title: "Linux笔记 - 数据库 - 运维 - 读写分离 - 一主一从"
category: "Linux笔记"
date: 2026-04-30
published: 2026-04-30
author: "Rin"
---

## 准备工作
- MASTER：192.168.200.211
- SLAVE：192.168.200.212

搭建好主从数据库

## 读写分离
schema.xml
MyCat控制后台数据库的读写分离和负载均衡由schema.xml文件datahost标签的balance属性控制的
```xml
    <schema name="ITCAST_RW" checkSQLschema="true" sqlMaxLimit="100" dataNode="dn7">
        <!-- auto sharding by id (long) -->
        <!--splitTableNames 启用<table name 属性使用逗号分割配置多个表,即多个表使用这个配置-->
        <!-- 这里配置逻辑表 rule属性是分片规则 具体配置在rule.xml中-->
       <!-- <table name="tb_order" dataNode="dn1,dn2,dn3" rule="auto-sharding-long" splitTableNames ="true"/> -->
        <!-- <table name="oc_call" primaryKey="ID" dataNode="dn1$0-743" rule="latest-month-calldate"
           /> -->
    </schema>
    
    <dataNode name="dn7" dataHost="dhost7" database="itcast" />
    
    
    
        <dataHost name="dhost7" maxCon="1000" minCon="10" balance="1"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <!-- can have multi write hosts -->
        <writeHost host="master" url="jdbc:mysql://192.168.200.211:3306/itcast?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02">
                   
                  <readHost host="slave" url="jdbc:mysql://192.168.200.212:3306/itcast?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="root"
                   password="Zerotwo02"/>
        </writeHost>
        <!-- <writeHost host="hostM2" url="localhost:3316" user="root" password="123456"/> -->
    </dataHost>
```

server.xml
```xml
<user name="mycat" defaultAccount="true">
        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->
        <property name="schemas">db01,ITCAST,ITCAST_RW</property>
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


| balance | 含义                                                    |
| ------- | ----------------------------------------------------- |
| 0       | 不开启读写分离机制 所有读操作都发送到当前可用的writeHost上                    |
| 1       | 全部的readHost与备用的writeHost都参与select语句的负载均衡（主要针对于双主双从模式） |
| 2       | 所有的读写操作都随机在writeHost，readHost上分发                      |
| 3       | 所有的读请求随机分发到writeHost对应的readHost上执行 writeHost不负担读压力    |

## 一主一从存在的问题
主节点master宕机之后 业务系统只能进行读操作 不能进行写操作了 解决方法是用双主双从架构