---
title: "Linux笔记 - 常用服务搭建 - FTP - 部署"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```bash
#安装ftp软件
yum install vsftpd -y

#启动服务
systemctl start vsftpd

#查看状态
systemctl status vsftpd

#配置
#创建ftp目录
mkdir /ftp

#配置文件
vim /etc/var/vsftpd/vsftpd.conf
#第12行 即anonymous_enable=YES下面
#添加访问代码
anon_root=/ftp #使用ftp协议默认访问的目录
anon_upload_enable=YES #是否允许用户上传文件
anon_mkdir_write_enable=YES #是否允许用户创建文件
 
#重启服务
systemctl restart vsftpd

#赋权 如果想在其他机子上传文件 那么其他用户需要有w权限
chmod 757 ftp
#或者把拥有者改成ftp 这个ftp是ftp协议自动创建的
chown ftp ftp

#回到物理机 在资源管理器通过ftp协议访问虚拟机
ftp://192.168.29.50
```

参考：