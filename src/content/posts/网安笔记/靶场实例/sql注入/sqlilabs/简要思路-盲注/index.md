---
title: "网安笔记 - 靶场实例 - sql注入 - sqlilabs - 简要思路-盲注"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

### 主要类型
* 基于布尔 SQL 盲注
	
* 基于时间的 SQL 盲注
	select if(mid(database(),1,1)='s',sleep(5),sleep(0));
	select if(substr(database(),1,1)='s',sleep(5),sleep(0));
	select if(substring(database(),1,1)='s',sleep(5),sleep(0));
	select if(left(database(),1)='s',sleep(5),sleep(0));
* 基于报错的 SQL 盲注