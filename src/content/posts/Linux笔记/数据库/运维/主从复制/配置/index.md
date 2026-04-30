---
title: "Linux笔记 - 数据库 - 运维 - 主从复制 - 配置"
category: "Linux笔记"
date: 2026-04-22
published: 2026-04-22
author: "Rin"
---

## 环境准备
主库：192.168.200.200(master)
从库：192.168.200.201(slave)

开放两台服务器的3306端口
```bash
firewall-cmd --zone=public --add-port=3306/tcp -permanent
firewall-cmd -reload
```
## 主库配置
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#mysql服务ID 保证整个集群环境唯一 取值范围 1 ~ 2^32-1 默认为1
server-id=1
#是否只读 1代表只读 0代表读写
read-only=0
#忽略的数据 指不需要同步的数据库
#binlog-ignore-db=mysql
#制定同步的数据库
#binlog-do-db=db01

#重启mysql
systemctl restart mysqld

#登录mysql 创建远程连接账号 并授予主从复制的权限
mysql -uroot -p
```

```mysql
#创建itcast用户 并设置密码 该用户可以在任意主机连接该MySQL服务
create user 'itcast'@'%' identified with mysql_native_password by 'Root@123456';
#为'itcast'@'%'用户分配主从复制权限
grant replication slave on *.* to 'itcast'@'%';
#通过指令 查看二进制日志坐标
show master status;

#字段含义说明
# file：从哪个日志文件开始推送日志文件
# position：从哪个位置开始推送日志
# binlog_ignore_db：指定不需要同步的数据库
```


## 从库配置
```bash
#修改配置文件
vim /etc/my.cnf

#写入
#服务ID不和主库一致且在范围内即可
server-id=2
#这个只读是对普通用户来说的 超级用户依然可以读写
read-only=1
#这个配置是禁止超级管理员的写权限的
#super-read-only=1

#重启mysql
systemctl restart mysqld
```

登录mysql 设置主库配置
```mysql
change replication source to source_host='xxx.xxx',source_user='xxx',source_password='xxx',source_log_file='xxx',source_log_pos=xxx;

#上述是8.0.23中的语法 如果mysql是8.0.23之前的版本 用下面的
change master to master_host='xxx.xxx.xxx.xxx',master_user='xxx',master_password='xxx',master_log_file='xxx',master_log_pos=xxx;
```

开启同步操作
```mysql
start replica; #8.0.22之后
start slave; #8.0.22之前
```

查看主从同步状态
```mysql
show replica status\G; #\G是把列转换为行来展示 用于数据库比较大 默认查看不方便看的情况
show slave status\G;
#只要看到了Slave_IO_Running为YES Slave_SQL_Running也为YES就是配置成功
```