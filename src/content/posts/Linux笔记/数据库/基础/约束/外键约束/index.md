---
title: "Linux笔记 - 数据库 - 基础 - 约束 - 外键约束"
category: "Linux笔记"
date: 2026-04-16
published: 2026-04-16
author: "Rin"
---

## 语法
```mysql
#建表时添加外键
create 表名(
    字段名 数据类型,
    ...
    [constraint] [外键名称] foreign key(外键字段名) references 主表(主表列名)
);

#创表之后添加外键
alter table 表名 add constraint 外键名称 foreign key(外键字段名) references 主表(主表列名);

#删除外键
alter table 表名 drop foreign key 外键名称;
```

## 删除/更新行为
```mysql
#基础语法
alter table 表名 add constraint 外键名称 foreign key (外键字段) references 主表名(主表字段名) on update cascade on delete cascade;
```

| 行为          | 说明                                                          |
| ----------- | ----------------------------------------------------------- |
| no action   | 当在父表中删除/更新对应记录时，先检查该记录是否有对应外键，如果有则不允许删除/更新。(与RESTRICT一致）    |
| restrict    | 当在父表中删除/更新对应记录时，先检查该记录是否有对应外键，如果有则不允许删除/更新。(与NOACTION致)     |
| cascade     | 当在父表中删除/更新对应记录时，先检查该记录是否有对应外键，如果有，则也删除/更新外键在子表中的记录。         |
| set null    | 当在父表中删除对应记录时，先检查该记录是否有对应外键，如果有则设置表中该外键值为null（这就要求该外键允许取nu）。 |
| set default | 父表有变更时，表将外键列设置成个默认的值(Innodb不持)                              |