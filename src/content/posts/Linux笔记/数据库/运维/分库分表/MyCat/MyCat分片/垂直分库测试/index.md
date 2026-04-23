---
title: "Linux笔记 - 数据库 - 运维 - 分库分表 - MyCat - MyCat分片 - 垂直分库测试"
category: "Linux笔记"
date: 2026-04-23
published: 2026-04-23
author: "Rin"
---

## 测试数据是否正常

```bash
#重启mycat服务
cd /usr/local/mycat
bin/mycat stop
bin/mycat start

#查看日志是否正常启动
tail -f log/wrapper.log

#测试
mysql -h 192.168.200.210 -P 8066 -uroot -p

#连接之后
```

```mysql
show databases;
#如果有逻辑库 就切换过去
use shopping;
show tables;
#应该能看到在schema.xml中定义过的逻辑表 但是这时候只是逻辑上存在 在真实服务器中 也就是物理上并不存在 我们要现在真实服务器中定义这几张表 并且添加数据
#自行添加
#使用source导入sql脚本
source /root/shopping-tables.sql
source /root/shopping-insert.sql
#查看数据是否正常即可
```

## 测试多表联查
```mysql
#查询用户的收件人及收件人地址信息(包含省、市、区) 这条应该是可以正常执行的
select ua.user_id,ua.contact,p.province,c.city,ua.address from tb_user_address ua, tb_areas_city c , tb_areas_provinces p , tb_areas_region r where ua.province_id=p.provinceid and ua.city_id = c.cityid and ua.town_id = r.areaid;

#查询每一笔订单及订单的收件地址信息（包含省、市、区） 如果没有配置全局表 这条是会报错的 因为这一条语句关联到的表不在同一个真实数据库 虽然你在逻辑库中能看到 但是实际上是无法关联到的 这就涉及到了MyCat的路由问题 解决方法就是配置全局表
select order_id , payment , receiver , province , city , area from tb_order_master o ,tb_areas_provinces p , tb_areas_city c , tb_areas_region r where o.receiver_province = p.provinceid and o.receiver_city = c.cityid and o.receiver_region = r.areaid;
```