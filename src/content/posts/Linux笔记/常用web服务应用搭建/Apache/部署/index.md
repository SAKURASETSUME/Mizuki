---
title: "Further relax access to the default document root:"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/常用web服务应用搭建/Apache/部署/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#检查是否安装了Apache的服务器软件
rpm -qa | grep -i httpd

#如果装了 卸载
dnf remove httpd*
#如果没装dn f 自己装一下
yum install epel-release
yum install dnf -y

#再次检查
rpm -qa | grep -i httpd

#安装Apache服务器软件
dnf -y install httpd*

#查询是否安装成功
rpm -qa | grep -i httpd

#启动httpd服务 并添加到开机启动
systemctl enable httpd
systemctl start httpd
```

## 配置

### 常用配置文件


| /etc/httpd                 | 服务目录     |
| -------------------------- | -------- |
| /etc/httpd/conf/httpd.conf | 主配置文件    |
| /var/www/html              | 网站数据目录   |
| /var/log/httpd/access_log  | 访问日志     |
| /var/log/httpd/error_log   | 错误日志     |
| /etc/httpd/conf.d          | 附加模块配置文件 |
| /etc/httpd/modules         | 模块文件路径链接 |
| /etc/httpd/bin/            | 二进制命令    |
| /etc/httpd/logs            | 默认日志文件位置 |

### 主配置文件介绍

```bash
vim /etc/httpd/conf/httpd.conf

#三种信息 注释行 全局配置 区域配置
```


| 参数             | 作用            |
| -------------- | ------------- |
| ServerRoot     | 服务目录          |
| ServerAdmin    | 管理员邮箱         |
| User           | 运行服务的用户       |
| Group          | 运行服务的用户组      |
| ServerName     | 网站服务器的域名      |
| DocumentRoot   | 网站数据目录        |
| Listen         | 监听的IP地址与端口号   |
| DirectoryIndex | 默认的索引页页面      |
| ErrorLog       | 错误日志文件        |
| CustomLog      | 访问日志文件        |
| Timeout        | 网页超时时间 默认300s |
### 修改Apache网页的默认页

```bash
# Further relax access to the default document root:
<Directory "/var/www/html">
    #
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"

    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks

    #
    # AllowOverride controls what directives may be placed in .htaccess files.
    # It can be "All", "None", or any combination of the keywords:
    #   Options FileInfo AuthConfig Limit
    #
    AllowOverride None

    #
    # Controls who can get stuff from this server.
    #
    Require all granted
</Directory>
#从这段能看出默认页面的路径

#直接改目标文件的页面样式
cd /var/www/html
vim index.html
#自己随便写点东西 然后访问就发现页面改变了
```

## 自定义网站存放目录

```bash
mkdir /home/wwwroot

#打开httpd服务程序的主配置文件，修改网站数据保存路径的参数，将119行的DocumentRoot修改为/home/wwwroot，将定义目录权限的参数124行和131行的Directory的路径也修改为/home/wwwroot。
vim /etc/httpd/conf/httpd.conf
#修改

#写个默认页面
echo "test" > /home/wwwroot/index.html
#重启httpd服务
systemctl restart httpd
#重新访问发现页面改变了
```

### 配置Selinux安全子系统

```bash
vim /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

#可以看出 Selinux安全子系统是处理强制运行状态
#把Selinux的运行模式修改为强制启用状态
#修改
SELINUX=enforcing
#重启
reboot
#检查是否启用
getenforce

#执行
setenforce 1
#设置自定义网站目录Selinux安全上下文
semanage fcontext -a -t httpd_sys_content_t /home/wwwroot

semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/*

#刷新Selinux安全上下文
restorecon -Rv /home/wwwroot/
#访问
```

参考：[apache安装与配置 linux-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2507864)
[linux安装Apache服务及配置详解-CSDN博客](https://blog.csdn.net/weixin_57839268/article/details/124154870)