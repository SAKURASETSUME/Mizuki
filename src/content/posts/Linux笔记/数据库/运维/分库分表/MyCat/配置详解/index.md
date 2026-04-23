---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - 配置详解"
category: "Linux笔记"
date: 2026-04-23
published: 2026-04-23
author: "Rin"
---

## schema.xml
schema.xml作为MyCat中最重要的配置文件之一 涵盖了MyCat的逻辑库、逻辑表、分片规则、分片节点及数据源的配置
主要包含以下三组标签：
 - schema标签
 - datanode标签
 - datahost标签

```xml
<!--schema标签-->
<!--用于定义MyCat实例中的逻辑库 一个MyCat实例当中 可以有多个逻辑库 可以通过schema标签来划分不同的逻辑库-->
<!--MyCat中的逻辑库的概念 等同于MySQL中的database概念 需要操作某个逻辑库下的表时 也需要切换逻辑库 use xxx;-->
<schema name="db01" checkSQLschema="true" sqlMaxLimit="100" randomDataNode="dn1">
        <table name="tb_order" dataNode="dn1,dn2,dn3" rule="auto-sharding-long" splitTableNames ="true"/>
    </schema>

<!--dataNode标签-->
    <dataNode name="dn1" dataHost="dhost1" database="db01" />
    <dataNode name="dn2" dataHost="dhost2" database="db01" />
    <dataNode name="dn3" dataHost="dhost3" database="db01" />
    
    <!--dataHost标签-->
    <dataHost name="dhost1" maxCon="1000" minCon="10" balance="0"
              writeType="0" dbType="mysql" dbDriver="jdbc" switchType="1"  slaveThreshold="100">
        <heartbeat>select user()</heartbeat>
        <writeHost host="hostM1" url="jdbc:mysql://192.168.200.210:3306/db01?useSSL=false&amp;serverTimezone=Asia/Shanghai&amp;characterEncoding=utf8&amp;allowPublicKeyRetrieval=true" user="mycat"
                   password="Zerotwo02">
        </writeHost>
    </dataHost>
```
**schema标签：**
核心属性：
- name：指定自定义的逻辑库库名
- checkSQLschema：在SQL语句操作时 如果指定了数据库名称(比如select \* from db01.tb_order) 执行时是否自动去除
- sqlMaxLimit：如果未指定limit进行查询 列表查询模式查询多少条记录

schema标签（table）：table标签定义了MyCat中逻辑库schema下的逻辑表 所有需要拆分的表都需要在table标签中定义
核心属性：
- name：定义逻辑库库名 在该逻辑库下唯一
- dataNode：定义数据库所属的dataNode 该属性需要与dataNode标签中的name对应 多个dataNode用逗号分隔
- rule：分片规则的名字 分片规则名字实在rule.xml中定义的
- primaryKey：逻辑表对应真实表的主键
- type：逻辑表的类型 目前逻辑表只有全局表和普通表 如果未配置 就是普通表 全局表配置为global

**dataNode标签：**
dataNode标签定义了MyCat中的数据节点 也就是我们通常说的数据分片 一个dataNode标签就是一个独立的数据分片

核心属性：
- name：定义数据节点名称
- dataHost：数据库实例主机名称 引用自dataHost标签中name属性
- database：定义分片所属的数据库

**dataHost标签：**
该标签在MyCat逻辑库中作为底层标签存在 直接定义了具体数据库实例、读写分离、心跳语句
核心属性：
- name：唯一标识 供上层标签使用
- maxCon/minCon：最大/最小连接数
- balance：负载均衡策略 取值0 1 2 3
- writeType：写操作分发方式（0：写操作转发到第一个writeHost 第一个挂了 切换到第二个；1：写操作随机分发到配置的writeHost）
- dbDriver：数据库驱动 支持native jdbc

指向顺序：schema(逻辑数据库) -> dataNode(逻辑节点) -> dataHost(实例主机)

## rule.xml
```xml
<tableRule name="auto-sharding-long">
        <rule>
            <columns>id</columns>
            <algorithm>rang-long</algorithm>
        </rule>
    </tableRule>
    
    
    <function name="rang-long"
              class="io.mycat.route.function.AutoPartitionByLong">
        <property name="mapFile">autopartition-long.txt</property>
    </function>
    
# range start-end ,data node index
# K=1000,M=10000.
0-500M=0
500M-1000M=1
1000M-1500M=2
```

rule.xml中定义所有拆分表的规则 在使用过程中可以灵活的使用分片算法 或者对同一个分片算法使用不同的参数 它让分片过程可配置化 主要包含两类标签：
tableRule Function

## server.xml
server.xml配置文件包含了MyCat的系统配置信息 主要有两个重要的标签：system user

```xml
<system>

    <property name="nonePasswordLogin">0</property> <!-- 0为需要密码登陆、1为不需要密码登陆 ,默认为0，设置为1则需要指定默认账户-->

    <property name="ignoreUnknownCommand">0</property><!-- 0遇上没有实现的报文(Unknown command:),就会报错、1为忽略该报文，返回ok报文。

    在某些mysql客户端存在客户端已经登录的时候还会继续发送登录报文,mycat会报错,该设置可以绕过这个错误-->

    <property name="useHandshakeV10">1</property>

    <property name="removeGraveAccent">1</property>

    <property name="useSqlStat">1</property>  <!-- 1为开启实时统计、0为关闭 -->

    <property name="useGlobleTableCheck">0</property>  <!-- 1为开启全加班一致性检测、0为关闭 -->

        <property name="sqlExecuteTimeout">300</property>  <!-- SQL 执行超时 单位:秒-->

        <property name="sequnceHandlerType">1</property>

        <!--<property name="sequnceHandlerPattern">(?:(\s*next\s+value\s+for\s*MYCATSEQ_(\w+))(,|\)|\s)*)+</property>

        INSERT INTO `travelrecord` (`id`,user_id) VALUES ('next value for MYCATSEQ_GLOBAL',"xxx");

        -->

        <!--必须带有MYCATSEQ_或者 mycatseq_进入序列匹配流程 注意MYCATSEQ_有空格的情况-->

        <property name="sequnceHandlerPattern">(?:(\s*next\s+value\s+for\s*MYCATSEQ_(\w+))(,|\)|\s)*)+</property>

    <property name="subqueryRelationshipCheck">false</property> <!-- 子查询中存在关联查询的情况下,检查关联字段中是否有分片字段 .默认 false -->

    <property name="sequenceHanlderClass">io.mycat.route.sequence.handler.HttpIncrSequenceHandler</property>

      <!--  <property name="useCompression">1</property>--> <!--1为开启mysql压缩协议-->

        <!--  <property name="fakeMySQLVersion">5.6.20</property>--> <!--设置模拟的MySQL版本号-->

    <!-- <property name="processorBufferChunk">40960</property> -->

    <!--

    <property name="processors">1</property>

    <property name="processorExecutor">32</property>

     -->

        <!--默认为type 0: DirectByteBufferPool | type 1 ByteBufferArena | type 2 NettyBufferPool -->

        <property name="processorBufferPoolType">0</property>

        <!--默认是65535 64K 用于sql解析时最大文本长度 -->

        <!--<property name="maxStringLiteralLength">65535</property>-->

        <!--<property name="sequnceHandlerType">0</property>-->

        <!--<property name="backSocketNoDelay">1</property>-->

        <!--<property name="frontSocketNoDelay">1</property>-->

        <!--<property name="processorExecutor">16</property>-->

        <!--

            <property name="serverPort">8066</property> <property name="managerPort">9066</property>

            <property name="idleTimeout">300000</property> <property name="bindIp">0.0.0.0</property>

            <property name="dataNodeIdleCheckPeriod">300000</property> 5 * 60 * 1000L; //连接空闲检查

            <property name="frontWriteQueueSize">4096</property> <property name="processors">32</property> -->

        <!--分布式事务开关，0为不过滤分布式事务，1为过滤分布式事务（如果分布式事务内只涉及全局表，则不过滤），2为不过滤分布式事务,但是记录分布式事务日志-->

        <property name="handleDistributedTransactions">0</property>

            <!--

            off heap for merge/order/group/limit      1开启   0关闭

        -->

        <property name="useOffHeapForMerge">0</property>

  

        <!--

            单位为m

        -->

        <property name="memoryPageSize">64k</property>

  

        <!--

            单位为k

        -->

        <property name="spillsFileBufferSize">1k</property>

  

        <property name="useStreamOutput">0</property>

  

        <!--

            单位为m

        -->

        <property name="systemReserveMemorySize">384m</property>

  
  

        <!--是否采用zookeeper协调切换  -->

        <property name="useZKSwitch">false</property>

  

        <!-- XA Recovery Log日志路径 -->

        <!--<property name="XARecoveryLogBaseDir">./</property>-->

  

        <!-- XA Recovery Log日志名称 -->

        <!--<property name="XARecoveryLogBaseName">tmlog</property>-->

        <!--如果为 true的话 严格遵守隔离级别,不会在仅仅只有select语句的时候在事务中切换连接-->

        <property name="strictTxIsolation">false</property>

        <property name="useZKSwitch">true</property>

        <!--如果为0的话,涉及多个DataNode的catlet任务不会跨线程执行-->

        <property name="parallExecute">0</property>

    </system>
    


<!--user标签-->
    <user name="mycat" defaultAccount="true">

        <property name="password">Zerotwo02</property> <!--这里配置的是连接mycat的密码-->

        <property name="schemas">db01</property>     <!--这里配置的是用户以上面配置的用户名和密码登录之后 可以访问的数据库 可以配置多个数据库 用逗号分隔-->

        <property name="defaultSchema">db01</property> 

        <!--No MyCAT Database selected 错误前会尝试使用该schema作为schema，不设置则为null,报错 -->

        <!-- 表级 DML 权限设置 -->

       <!--         

        <privileges check="false">
 
            <schema name="db01" dml="1110" >  #配置指定逻辑库权限

                <table name="tb_order" dml="0000"> </table> #配置制定逻辑表权限 配置多个时候遵循就近原则 4个数字代表增 改 查 删 即IUSD

                <table name="tb_order" dml="1111"></table> 

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