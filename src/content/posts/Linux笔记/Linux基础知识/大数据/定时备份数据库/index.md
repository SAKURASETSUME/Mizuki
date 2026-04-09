---
title: "Linux笔记 - Linux基础知识 - 大数据 - 定时备份数据库"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 需求分析

```txt
每天凌晨2:30备份数据库test12DB到/data/backup/db
备份开始和备份结束能够给出相应的提示信息
备份后的文件要求以备份时间为文件名，并打包成.tar.gz的形式，比如：2021-03-12_230201.tar.gz
在备份的同时，检查是否有10天前备份的数据库文件，如果有就将其删除。
```

## 思路分析

- /usr/sbin/mysql_db_backup.sh 该脚本完成备份任务 (选用这个路径是因为这个路径只有root用户才有权限)
- 每天凌晨两点半备份：使用crond来定时调用写好的shell脚本
- 写shell脚本 测试能够完成需求后 再用crond定时调用

```bash
#备份脚本
vim /usr/sbin/mysql_db_backup.sh

#写入
#!/bin/bash
#备份目录
BACKUP=/data/backup/db
#获取当前的时间
DATETIME=$(date + %Y-%m-%d_%H%M%S)
#数据库地址
HOST=localhost
#数据库用户名
DB_USER=root
#数据库密码
DB_PWD=root
#备份的数据库
DATABASE=test12DB

#创建备份目录 如果不存在 就创建
[ ! -d "${BACKUP}/${DATETIME}" ] && mkdir -p "${BACKUP}/${DATETIME}"

#备份数据库
mysqldump -u${DB_USER} -p${DB_PWD} --host=${HOST} -q -R --databases ${DATABASE} | gzip > ${BACKUP}/${DATETIME}/$DATETIME.sql.gz

#将文件处理成tar.gz
cd ${BACKUP}
tar -zcvf $DATETIME.tar.gz ${DATETIME}
#删除对应的备份目录
rm -rf ${BACKUP}/${DATETIME}

#删除10天前的备份文件
find ${BACKUP} -atime +10 -name "*.tar.gz" -exec rm -rf {} \;
echo "备份数据库${DATABASE}成功"

#定时调度
crontab -e
30 2 * * * /usr/sbin/mysql_db_backup.sh

#确认定时调度是否添加成功
crontab -l
```