---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - 简单入门"
category: "Linux笔记"
date: 2026-04-22
published: 2026-04-22
author: "Rin"
---

## 需求
```txt
由于tb_order表中数据量很大，磁盘IO及容量都到达了瓶颈，现在需要对tb_order表进行数据分片，分为三个数据节点，每一个节
点主机位于不同的服务器上，具体的结构，参考下面
```

tb_order
- dataNode1  -> db01
- dataNode2 -> db01
- dataNode3 -> db01

## 环境准备
- MyCat中间件服务器 192.168.200.210
- MySQL 192.168.200.210
- MySQL 192.168.200.213
- MySQL 192.168.200.214

```mysql
#在三台MySQL创建数据库db01
#后面所有的操作在MyCat操作
```

## 实操

```mysql
#创建mycat专用账户
create user 'mycat'@'%' identified by 'Zerotwo02';  
grant all privileges on db01.* to 'mycat'@'%';  
flush privileges;
```

```xml
#配置Mycat
vim /usr/local/mycat/conf/schema.xml

<?xml version="1.0"?>

<!DOCTYPE mycat:schema SYSTEM "schema.dtd">

<mycat:schema xmlns:mycat="http://io.mycat/">

  

<!-- 这里配置逻辑库 -->

    <schema name="db01" checkSQLschema="true" sqlMaxLimit="100" randomDataNode="dn1">

        <!-- auto sharding by id (long) -->

        <!--splitTableNames 启用<table name 属性使用逗号分割配置多个表,即多个表使用这个配置-->

        <!-- 这里配置逻辑表 rule属性是分片规则 具体配置在rule.xml中-->

        <table name="tb_order" dataNode="dn1,dn2,dn3" rule="auto-sharding-long" splitTableNames ="true"/>

        <!-- <table name="oc_call" primaryKey="ID" dataNode="dn1$0-743" rule="latest-month-calldate"

            /> -->

    </schema>

    <!-- <dataNode name="dn1$0-743" dataHost="localhost1" database="db$0-743"

        /> -->

        <!-- 这里配置数据节点 -->

    <dataNode name="dn1" dataHost="dhost1" database="db01" />

    <dataNode name="dn2" dataHost="dhost2" database="db01" />

    <dataNode name="dn3" dataHost="dhost3" database="db01" />

    <!--<dataNode name="dn4" dataHost="sequoiadb1" database="SAMPLE" />

     <dataNode name="jdbc_dn1" dataHost="jdbchost" database="db1" />

    <dataNode   name="jdbc_dn2" dataHost="jdbchost" database="db2" />

    <dataNode name="jdbc_dn3"   dataHost="jdbchost" database="db3" /> -->

  

    <!-- 这里配置节点主机 dbDriver最好选jdbc native兼容性不太好-->

    <dataHost name="dhost1" maxCon="1000" minCon="10" balance="0"

              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">

        <heartbeat>select user()</heartbeat>

        <!-- can have multi write hosts -->

        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.210:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"

                   password="Zerotwo02">

        </writeHost>

        <!-- <writeHost host="hostM2" url="localhost:3316" user="root" password="123456"/> -->

    </dataHost>

  

    <dataHost name="dhost2" maxCon="1000" minCon="10" balance="0"

              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">

        <heartbeat>select user()</heartbeat>

        <!-- can have multi write hosts -->

        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.213:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"

                   password="Zerotwo02">

        </writeHost>

        <!-- <writeHost host="hostM2" url="localhost:3316" user="root" password="123456"/> -->

    </dataHost>

  

    <dataHost name="dhost3" maxCon="1000" minCon="10" balance="0"

              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">

        <heartbeat>select user()</heartbeat>

        <!-- can have multi write hosts -->

        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.214:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"

                   password="Zerotwo02">

        </writeHost>

        <!-- <writeHost host="hostM2" url="localhost:3316" user="root" password="123456"/> -->

    </dataHost>

    <!--

        <dataHost name="sequoiadb1" maxCon="1000" minCon="1" balance="0" dbType="sequoiadb" dbDriver="jdbc">

        <heartbeat>         </heartbeat>

         <writeHost host="hostM1" url="sequoiadb://1426587161.dbaas.sequoialab.net:11920/SAMPLE" user="jifeng"  password="jifeng"></writeHost>

         </dataHost>

  

      <dataHost name="oracle1" maxCon="1000" minCon="1" balance="0" writeType="0"   dbType="oracle" dbDriver="jdbc"> <heartbeat>select 1 from dual</heartbeat>

        <connectionInitSql>alter session set nls_date_format='yyyy-mm-dd hh24:mi:ss'</connectionInitSql>

        <writeHost host="hostM1" url="jdbc:oracle:thin:@127.0.0.1:1521:nange" user="base"   password="123456" > </writeHost> </dataHost>

  

        <dataHost name="jdbchost" maxCon="1000"     minCon="1" balance="0" writeType="0" dbType="mongodb" dbDriver="jdbc">

        <heartbeat>select   user()</heartbeat>

        <writeHost host="hostM" url="mongodb://192.168.0.99/test" user="admin" password="123456" ></writeHost> </dataHost>

  

        <dataHost name="sparksql" maxCon="1000" minCon="1" balance="0" dbType="spark" dbDriver="jdbc">

        <heartbeat> </heartbeat>

         <writeHost host="hostM1" url="jdbc:hive2://feng01:10000" user="jifeng"     password="jifeng"></writeHost> </dataHost> -->

  

    <!-- <dataHost name="jdbchost" maxCon="1000" minCon="10" balance="0" dbType="mysql"

        dbDriver="jdbc"> <heartbeat>select user()</heartbeat> <writeHost host="hostM1"

        url="jdbc:mysql://localhost:3306" user="root" password="123456"> </writeHost>

        </dataHost> -->

</mycat:schema>
```

```bash
#分片配置
vim /usr/local/mycat/conf/server.xml
```

```xml
    <user name="mycat" defaultAccount="true">

        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->

        <property name="schemas">db01</property>

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

  

    <user name="user">

        <property name="password">user</property>

        <property name="schemas">db01</property>

        <property name="readOnly">true</property>

        <property name="defaultSchema">db01</property>

    </user>
```

## 测试
```bash
#切换到mycat的安装目录 启动 占用端口号8066
cd /usr/local/mycat
bin/mycat start
bin/mecat stop #这个是停止

#查看启动是否成功从日志可以看到
tail -f /usr/local/mycat/logs/wrapper.log 
```

分片测试
```bash
#登录mycat
mysql -h 192.168.200.210 -P 8066 -uroot -p
```

```mysql
#创建表
use db01;
CREATE TABLE TB_ORDER
id BIGINT(20) NOTNULL,
title VARCHAR(100) NOTNULL,
PRIMARY KEY (id）
) ENGINE=INNODB DEFAULT CHARSET=Utf8;
INSERT INTO TB_ORDER(id,title) VALUES(1,'goods1');
INSERT INTO TB_ORDER(id,title) VALUES(2,'goods2');
INSERT INTO TB_ORDER(id,title) VALUES(3,'goods3');
INSERT INTO TB_ORDER(id,title) VALUES(1000000,'goods1000000');
INSERT INTO TB_ORDER(id,title) VALUES(100000001,'goods10000000');
```