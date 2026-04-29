---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - 分片规则"
category: "Linux笔记"
date: 2026-04-29
published: 2026-04-29
author: "Rin"
---

## 范围分片
根据指定的字段及其配置的范围与数据节点的对应情况 来决定数据属于哪一个分片 
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
```

```txt
    # range start-end ,data node index
# K=1000,M=10000.
0-500M=0
500M-1000M=1
1000M-1500M=2

这是txt中的内容 代表的是每个分片数据存储的范围
```

## 取模分片
根据制定的字段值与节点的数量进行求模运算 根据运算的结果来决定数据属于哪一个分片

```xml
<tableRule name="mod-long">
        <rule>
            <columns>id</columns>
            <algorithm>mod-long</algorithm>
        </rule>
    </tableRule>
    
        <function name="mod-long" class="io.mycat.route.function.PartitionByMod">
        <!-- how many data nodes -->
        <property name="count">3</property>
    </function>
```

## 一致性hash算法
hash算法指的是 在分片时计算指定字段的哈希值 根据哈希值来决定当前这条记录要落在哪一个分片节点中
所谓一致性哈希就是 相同的哈希因子计算值总是被划分到相同的分区表中 不会因为分区节点的增加而改变原来数据的分区位置

```xml
<tableRule name="sharding-by-murmur">
        <rule>
            <columns>id</columns>
            <algorithm>murmur</algorithm>
        </rule>
    </tableRule>
    
    
        <function name="murmur"
              class="io.mycat.route.function.PartitionByMurmurHash">
        <property name="seed">0</property><!-- 默认是0 -->
        <property name="count">2</property><!-- 要分片的数据库节点数量，必须指定，否则没法分片 -->
        <property name="virtualBucketTimes">160</property><!-- 一个实际的数据库节点被映射为这么多虚拟节点，默认是160倍，也就是虚拟节点数是物理节点数的160倍 -->
        <!-- <property name="weightMapFile">weightMapFile</property> 节点的权重，没有指定权重的节点默认是1。以properties文件的格式填写，以从0开始到count-1的整数值也就是节点索引为key，以节点权重值为值。所有权重值必须是正整数，否则以1代替 -->
        <!-- <property name="bucketMapPath">/etc/mycat/bucketMapPath</property>
            用于测试时观察各物理节点与虚拟节点的分布情况，如果指定了这个属性，会把虚拟节点的murmur hash值与物理节点的映射按行输出到这个文件，没有默认值，如果不指定，就不会输出任何东西 -->
    </function>
```

## 枚举分片
通过在配置文件中配置可能的枚举值 指定数据分布到不同数据节点上 本规则适用于按照省份、性别、状态拆分数据等业务

```xml
    <tableRule name="sharding-by-intfile">
        <rule>
            <columns>sharding_id</columns>
            <algorithm>hash-int</algorithm>
        </rule>
    </tableRule>
    
    <function name="hash-int"
              class="io.mycat.route.function.PartitionByFileMap">
        <property name="defaultNode">2</property>
        <property name="mapFile">partition-hash-int.txt</property>
    </function>
    
    <!-- ps：columns这个值是指定枚举分片的值的字段名的 每个配置只能指定一个  这就导致了如果你想要有多个表都使用枚举分片 但是需要枚举的字段名不同 配置文件会冲突 建议自己复制这个枚举配置 然后改个名 当做一个新的分片规则来写 再把需要枚举的表的rule标签指向你自定义的分片规则就可以解决了 当然 分片规则自定义时 function也是可以自定义的 你可以再写一个新的function 指定一个新的配置文件去配置字段值对应的数据节点 -->
    
    <!-- 自定义举例 -->
        <tableRule name="sharding-by-intfile-enumstatus">
        <rule>
            <columns>status</columns>
            <algorithm>hash-int-enumstatus</algorithm>
        </rule>
    </tableRule>
    
    <function name="hash-int-enumstatus"
              class="io.mycat.route.function.PartitionByFileMap">
        <property name="defaultNode">2</property> <!--这个配置是当字段值和枚举值不同时 存放的默认节点 -->
        <property name="mapFile">partition-hash-int-enumstatus.txt</property>
    </function>
    
```

```txt
10000=0
10010=1

这里是配置枚举值落到哪个数据节点的
```

## 应用指定算法
运行阶段由应用自主决定路由到那个分片 直接根据字符子串(必须是数字）计算分片号

```xml
    <tableRule name="sharding-by-substring">
        <rule>
            <columns>id</columns>
            <algorithm>sharding-by-substring</algorithm>
        </rule>
    </tableRule>
    
        <function name="sharding-by-substring"
              class="io.mycat.route.function.PartitionDirectBySubString">
        <property name="startIndex">0</property>   <!-- 从第一个位置开始截取 -->
        <property name="size">2</property> <!-- 截取字符串的长度 -->
        <property name="partitionCount">3</property> <!-- 分片数量 -->
        <property name="defaultPartition">2</property>
    </function>
```

## 固定分片hash算法
该算法类似于十进制的求模运算 但是为二进制的操作 例如 取id的二进制低10位与1111111111进行位&运算

特点：
- 如果是求模 连续的值 分别分配到各个不同的分片 但是此算法可能会将连续的值分配到相同的分片 降低事务处理的难度
- 可以均匀分配 也可以非均匀分配
- 分片字段必须为数字类型

```xml
<tableRule name="sharding-by-long-hash">
        <rule>
            <columns>id</columns>
            <algorithm>sharding-by-long-hash</algorithm>
        </rule>
    </tableRule>
    
    <function name="sharding-by-long-hash" class="io.mycat.route.function.PartitionByLong">
        <property name="partitionCount">2,1</property>
        <property name="partitionLength">256,512</property>
    </function> <!-- 这两个配置指的是 一共有3个节点 前两个节点模运算之后存储的数值是0-255 256-511 第3个节点存储的数值是512-1023 -->

```

```txt
固定分片hash算法的约束：
分片长度默认最大为1024
Count Length的数组长度必须一致
```

## 字符串hash解析
截取字符串中的指定位置的子字符串 进行hash算法 算出分片

```xml
    <tableRule name="sharding-by-stringhash">
        <rule>
            <columns>name</columns>
            <algorithm>sharding-by-stringhash</algorithm>
        </rule>
        
            <function name="latestMonth"
              class="io.mycat.route.function.PartitionByString">
        <property name="partitionLength">512</property>
        <property name="partitionCount">2</property>
        <property name="hashSlice">0:2</property> <!-- hash运算位 格式为start:end 0在end中出现代表str.length() -1代表str.length()-1 大于0代表数字本身 -->
    </function>
```

## 按天分片
```xml
    <tableRule name="sharding-by-date">
        <rule>
            <columns>create_time</columns>
            <algorithm>sharding-by-date</algorithm>
        </rule>
    </tableRule>
    
        <function name="sharding-by-date"
              class="io.mycat.route.function.PartitionByDate">
        <property name="dateFormat">yyyy-MM-dd</property>
        <property name="sBeginDate">2026-01-01</property>
        <property name="sEndDate">2026-01-31</property>
        <property name="sPartionDay">10</property>
    </function>
    <!-- 从2026-01-01开始计算 每10天为一个分界点 分到不同的数据分片 到了2026-01-31之后从第一个数据分片重新开始计算 -->
    <!-- ps:在schema.xml中配置节点数量的时候 要保证数据节点的数量和这里分片规则计算之后的节点数量一致 例如dataNode配置了3个节点 但是开始日期是2026-01-01 结束日期是2026-12-31 每10天一个分片 那么就需要37个分片 这样配置会冲突 -->
```

## 按自然月分片
```xml
    <tableRule name="sharding-by-month">
        <rule>
            <columns>create_time</columns>
            <algorithm>partbymonth</algorithm>
        </rule>
    </tableRule>
    
        <function name="partbymonth"
              class="io.mycat.route.function.PartitionByMonth">
        <property name="dateFormat">yyyy-MM-dd</property>
        <property name="sBeginDate">2026-01-01</property>
        <property name="sEndDate">2026-03-31</property>
    </function>
    <!-- 同样地 这里的分片数量也要和schema.xml的节点数量一致 -->
```