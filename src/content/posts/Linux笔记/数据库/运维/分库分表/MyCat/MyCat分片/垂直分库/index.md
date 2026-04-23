---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - 垂直分库"
category: "Linux笔记"
date: 2026-04-23
published: 2026-04-23
author: "Rin"
---

## 场景
```txt
在业务系统中 涉及以下表结构 但是由于用户与订单每天都会产生大量的数据 单台服务器的数据存储及处理能力是有限的 可以对数据库表进行拆分 原有的数据库表如下
```

```txt
省 市 区字典：
tb_areas_city
tb_areas_provinces
tb_areas_region 

商品：
tb_goods_base
tb_goods_brand
tb_goods_cat
tb_goods_item

订单：
tb_order_item
tb_order_master
tb_order_pay_log

用户：
tb_user
tb_user_address
```

## 思路
```txt
分成三个数据库来存储
第一个数据库 存储商品表 -> dataNode1
第二个数据库 存储订单表 -> dataNode2
第三个数据库 存储用户表和字典表 -> dataNode3
```

## 环境准备
- MyCat ->  192.168.200.210
- MySQL -> 192.168.200.210
- MySQL -> 192.168.200.213
- MySQL -> 192.168.200.214

```mysql
#创建数据库shopping 后面的表就放在这个数据库当中
create database shopping;
```

## MyCat配置
### 逻辑库配置
```xml
<?xml version="1.0"?>

<!DOCTYPE mycat:schema SYSTEM "schema.dtd">

<mycat:schema xmlns:mycat="http://io.mycat/">
    <schema name="shopping" checkSQLschema="true" sqlMaxLimit="100" randomDataNode="dn1">
        <!--商品库-->
        <table name="tb_goods_base" dataNode="dn1"  primaryKey="id"/>
        <table name="tb_goods_brand" dataNode="dn1" primaryKey="id"/>
        <table name="tb_goods_cat" dataNode="dn1"   primaryKey="id"/>
        <table name="tb_goods_item" dataNode="dn1"  primaryKey="id"/>
        
        <!--订单库-->
        <table name="tb_order_item" dataNode="dn2"  primaryKey="id"/>
        <table name="tb_order_master" dataNode="dn2" primaryKey="id"/>
        <table name="tb_order_pay_log" dataNode="dn2"  primaryKey="id"/>
        
        <!--用户库-->
        <table name="tb_user" dataNode="dn3"  primaryKey="id"/>
        <table name="tb_user_address" dataNode="dn3"  primaryKey="id"/>
        
        <!--全局表-->
        <table name="tb_areas_city" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
        <table name="tb_areas_provinces" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
        <table name="tb_areas_region" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
    </schema>
    
    <dataNode name="dn1" dataHost="dhost1" database="shopping" />
    <dataNode name="dn2" dataHost="dhost2" database="shopping" />
    <dataNode name="dn3" dataHost="dhost3" database="shopping" />

    <dataHost name="dhost1" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.210:3306/shopping?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8mb4&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>

    <dataHost name="dhost2" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.213:3306/shopping?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8mb4&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>
    
    <dataHost name="dhost3" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.214:3306/shopping?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8mb4&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>
</mycat:schema>
```

### server.xml配置
```xml
    <user name="mycat" defaultAccount="true">

        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->

        <property name="schemas">shopping</property>

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

        <property name="schemas">shopping</property>

        <property name="readOnly">true</property>

        <property name="defaultSchema">shopping</property>

    </user>
```

## 全局表的配置
对于省、市、区/县表 tb_areas_provinces , tb_areas_city , tb_areas_region 是属于字典表 在多个业务模块中都有可能会用到 可以将其设置为全局表 利于业务操作

```xml
 <table name="tb_areas_city" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
        <table name="tb_areas_provinces" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
        <table name="tb_areas_region" dataNode="dn1,dn2,dn3"  primaryKey="id" type="global"/>
```

**在mycat中进行操作 对全局表进行修改之后 每个节点的全局表数据都会更新**