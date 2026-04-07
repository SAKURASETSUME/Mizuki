---
title: "知识补充-截取字符串函数"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/.trash/知识补充-截取字符串函数/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

三大法宝：mid(),substr(),left()

**mid()函数**

此函数为截取字符串一部分。MID(column_name,start[,length])

|   |   |
|---|---|
|**参数**|**描述**|
|column_name|必需。要提取字符的字段。|
|start|必需。规定开始位置（起始值是 1）。|
|length|可选。要返回的字符数。如果省略，则 MID() 函数返回剩余文本。|

Eg:      str="123456"     mid(str,2,1)    结果为2

Sql用例：

（1）MID(DATABASE(),1,1)>’a’,查看数据库名第一位，MID(DATABASE(),2,1)查看数据库名第二位，依次查看各位字符。

（2）MID((SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE T table_schema=0xxxxxxx LIMIT 0,1),1,1)>’a’此处column_name参数可以为sql语句，可自行构造sql语句进行注入。

 **substr()函数**

    Substr()和substring()函数实现的功能是一样的，均为截取字符串。

    string substring(string, start, length)

    string substr(string, start, length)

    参数描述同mid()函数，第一个参数为要处理的字符串，start为开始位置，length为截取的长度。

Sql用例：

(1) substr(DATABASE(),1,1)>’a’,查看数据库名第一位，substr(DATABASE(),2,1)查看数据库名第二位，依次查看各位字符。

(2) substr((SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE T table_schema=0xxxxxxx LIMIT 0,1),1,1)>’a’此处string参数可以为sql语句，可自行构造sql语句进行注入。

**L****eft()函数**

Left()得到字符串左部指定个数的字符

Left ( string, n )        string为要截取的字符串，n为长度。

Sql用例：

(1) left(database(),1)>’a’,查看数据库名第一位，left(database(),2)>’ab’,查看数据库名前二位。

(2) 同样的string可以为自行构造的sql语句。

同时也要介绍ORD()函数，此函数为返回第一个字符的ASCII码，经常与上面的函数进行组合使用。

例如ORD(MID(DATABASE(),1,1))>114 意为检测database()的第一位ASCII码是否大于114，也即是‘r’