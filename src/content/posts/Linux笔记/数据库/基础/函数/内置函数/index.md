---
title: "Linux笔记 - 数据库 - 基础 - 函数 - 内置函数"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

## 字符串函数
```mysql
#举例
#将工号填充成5位 不足的在前面补0
update emp set workno = lpad(workno,5,'0');
```

| 函数                       | 功能                               |
| ------------------------ | -------------------------------- |
| concat(s1,s2,....,sn)    | 字符串拼接 将s1 s2...sn拼接成一个字符串        |
| lower(str)               | 将字符串str转小写                       |
| upper(str)               | 将字符串str转大写                       |
| lpad(str,n,pad)          | 左填充 用字符串pad对str的左边进行填充 达到n个字符串长度 |
| rpad(str,n,pad)          | 右填充                              |
| trim(str)                | 去掉字符串头部和尾部的空格                    |
| substring(str,start,len) | 返回字符串str从start位置起的len个长度的字符串     |
## 数值函数
```mysql
#举例
#通过数据库的函数 生成一个6位随机数字的验证码
select lpad( round( rand()*999999,0 ),6,'0' );
```

| 函数         | 功能                |
| ---------- | ----------------- |
| ceil(x)    | 向上取整              |
| floor(x)   | 向下取整              |
| mod(x,y)   | 返回x/y的模           |
| rand()     | 返回0-1的随机数         |
| round(x,y) | 求参数x的四舍五入值 保留y位小数 |
## 日期函数
```mysql
#举例
#查询所有员工的入职天数 并根据入职天数倒序排序
select name , datediff (curdate() , entrydate) 'entryday' from emp order by 'entryday' ;
```

| 函数                                | 功能                          |
| --------------------------------- | --------------------------- |
| curdate()                         | 返回当前日期                      |
| curtime()                         | 返回当前时间                      |
| now()                             | 返回当前日期和时间                   |
| year(date)                        | 获取指定date年份                  |
| month(date)                       | 获取指定date月份                  |
| day(date)                         | 获取指定date日期                  |
| date_add(date,interval expr type) | 返回一个日期/时间值加上一个时间间隔expr后的时间值 |
| datediff(date1,date2)             | 返回起始时间date1 和结束时间date2之间的天数 |

## 流程控制函数
```mysql
#举例
#查询emp表的员工姓名和工作地址（北京/上海-->一线城市，其他--->二线城市）
select name , (case workaddress when '北京' then '一线城市' when '上海' then '一线城市' else '二线城市' end ) as '工作地址' from emp;

#统计班级各个学员的成绩 展示的规则如下
# >=85 优秀 >=60 展示及格 否则 展示不及格
select 
id,
name,
(case when math>=85 then '优秀' when math >=60 then '及格' else '不及格' end) '数学',
(case when english>=85 then '优秀' when english >=60 then '及格' else '不及格' end) '英语',
(case when chinese>=85 then '优秀' when chinese >=60 then '及格' else '不及格' end) '语文'
from score;
```

| 函数                                                        | 功能                                         |
| --------------------------------------------------------- | ------------------------------------------ |
| if(value , t ,f)                                          | 如果value为true 返回t 否则返回f                     |
| ifnull(value1 , value2)                                   | 如果value1不为空 返回value1 否则返回value2            |
| case when [val1] then [res1] ... else [default] end       | 如果val1为true 返回res1 , ... 否则返回返回default默认值  |
| case [expr] when [val1] then [res1] ...else [default] end | 如果expr的值等于val1 返回res1 , ... 否则返回default默认值 |