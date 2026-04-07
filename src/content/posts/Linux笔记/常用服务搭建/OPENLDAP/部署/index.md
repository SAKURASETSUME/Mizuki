---
title: "部署"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/常用服务搭建/OPENLDAP/部署/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#yum方式安装
yum -y install openldap compat-openldap openldap-clients openldap-servers openldap-servers-sql openldap-devel migrationtools

#查看openLDAP版本
slapd -VV

#配置openLDAP
#配置管理员密码
slappasswd 
#配置过后会输出一段加密过的密码 自己保存一下 后面配置文件要用
{SSHA}/K+wc9QaTGOhk8GZjcQ1JLO62GiTlZSX

#修改olcDatabase={2}hdb.ldif文件 cn=root中的root表示OpenLDAP管理员的用户名，而olcRootPW表示OpenLDAP管理员的密码
vim /etc/openldap/slapd.d/cn=config/olcDatabase\=\{2\}hdb.ldif

#修改后的内容
olcSuffix: dc=test,dc=com olcRootDN: cn=root,dc=test,dc=com olcRootPW: 密码的密文 #这一段自己写进配置文件 缩进用tab 别用空格 不然会出问题

#修改olcDatabase={1}monitor.ldif文件
vim /etc/openldap/slapd.d/cn=config/olcDatabase\=\{1\}monitor.ldif

#修改
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" read by dn.base=”cn=root,dc=test,dc=com” read by * none
#注意 如果上面自定义了用户名 这里引号的用户名记得改了

#验证环境的配置
slaptest -u

69bcd2cd ldif_read_file: checksum error on "/etc/openldap/slapd.d/cn=config/olcDatabase={1}monitor.ldif"
69bcd2cd ldif_read_file: checksum error on "/etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif"
config file testing succeeded
#出现这个就是对了

#启动openLDAP服务
systemctl enable slapd
systemctl start slapd
systemctl status slapd

#验证端口
netstat -ntlp | grep 389 #默认端口是389

#配置数据库
#openLDAP默认用的数据库是BerkeleyDB /var/lib/ldap就是BerkeleyDB数据库的默认存储路径
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
chown ldap:ldap -R /var/lib/ldap
chmod 700 -R /var/lib/ldap
ll /var/lib/ldap/

#导入基本Schema

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/core.ldif 
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/collective.ldif 
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/corba.ldif 
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/duaconf.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/dyngroup.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/java.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/misc.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/openldap.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/pmi.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/ppolicy.ldif

#修改migrate_common.ph文件
vim /usr/share/migrationtools/migrate_common.ph +71

#修改
$DEFAULT_MAIL_DOMAIN = “test.com”;
$DEFAULT_BASE = “dc=test,dc=com”;
$EXTENDED_SCHEMA = 1;

#添加用户及用户组
#默认情况下OpenLDAP是没有普通用户的，但是有一个管理员用户。管理用户就是前面我们刚刚配置的root。

#现在我们把系统中的用户，添加到OpenLDAP中。为了进行区分，我们现在新加两个用户ldapuser1和ldapuser2，和两个用户组ldapgroup1和ldapgroup2

groupadd ldapgroup1
groupadd ldapgroup2

useradd -g ldapgroup1 ldapuser1
useradd -g ldapgroup2 ldapuser2
echo 'Zerotwo02' | passwd --stdin ldapuser1
echo 'Zerotwo02' | passwd --stdin ldapuser2

#把刚刚添加的用户和用户组提取出来，包括该用户的密码和其他相关属性
grep ":10[0-9][0-9]" /etc/passwd > /root/users
grep ":10[0-9][0-9]" /etc/group > /root/groups
cat users
cat groups

#根据上述生成的用户和用户组属性，使用migrate_passwd.pl文件生成要添加用户和用户组的ldif

/usr/share/migrationtools/migrate_passwd.pl /root/users > /root/users.ldif
/usr/share/migrationtools/migrate_group.pl /root/groups > /root/groups.ldif
cat users.ldif
cat groups.ldif

#导入用户及用户组到openLDAP数据库
vim /root/base.ldif

#写入
dn: dc=test,dc=com
o: test com
dc: test
objectClass: top
objectClass: dcObject
objectclass: organization

dn: cn=root,dc=test,dc=com
cn: root
objectClass: organizationalRole
description: Directory Manager

dn: ou=People,dc=test,dc=com
ou: People
objectClass: top
objectClass: organizationalUnit

dn: ou=Group,dc=test,dc=com
ou: Group
objectClass: top
objectClass: organizationalUnit

#导入基础数据库、导入用户到数据库，导入用户组到数据库
ldapadd -x -W -D "cn=root,dc=test,dc=com" -f /root/base.ldif
ldapadd -x -W -D "cn=root,dc=test,dc=com" -f /root/users.ldif
ldapadd -x -W -D "cn=root,dc=test,dc=com" -f /root/groups.ldif
#这里需要输你刚才设置的openLDAP的密码

#查看BerkeleyDB数据库文件
ll /var/lib/ldap/
#*.bdb

#查询openLDAP相关信息
ldapsearch -x -b "dc=test,dc=com" -H ldap://127.0.0.1

#查询添加的openLDAP用户信息
ldapsearch -LLL -x -D 'cn=root,dc=test,dc=com' -w "Zerotwo02" -b 'dc=test,dc=com' 'uid=ldapuser1'

#查询添加的openLDAP用户组信息
ldapsearch -LLL -x -D 'cn=root,dc=test,dc=com' -w "Zerotwo02" -b 'dc=test,dc=com' 'cn=ldapgroup1'

#把openLDAP用户加入到用户组
#在OpenLdap中添加组的功能，所以需要添加memberOf功能
#新建文件memberof_load_configure.ldif
#在/root目录下新建文件memberof_load_configure.ldif
#写入
dn: cn=module{0},cn=config
objectClass: olcModuleList
cn: module{0}
olcModulepath: /usr/lib64/openldap
olcModuleload: {0}memberof.la

dn: olcOverlay={0}memberof,olcDatabase={2}hdb,cn=config
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: olcConfig
objectClass: top
olcOverlay: {0}memberof

#说明：上面的参数请根据实际情况修改（比如32的系统的话olcModulepath为/usr/lib/openldap）  
dn: cn=module{0},cn=config 如果/etc/openldap/slapd.d/cn=config目录下已经存在cn=module{0}.ldif 文件的话，你就需要修改 module后面的数字了  
dn: olcOverlay={0}memberof,olcDatabase={2}bdb,cn=config 这行中 如果上述目录中没有olcDatabase={2}bdb.ldif文件就把 olcDatabase={2}bdb改成olcDatabase={2}hdb
#添加
ldapadd -Q -Y EXTERNAL -H ldapi:/// -f memberof_load_configure.ldif

#测试添加group
#在root目录下新建文件addgroup.ldif

#写入
dn: cn=gitlab,ou=Group,dc=test,dc=com
objectClass: top
objectClass: groupOfNames
cn: gitlab
member: uid=testuser,ou=People,dc=test,dc=com

#使用ldapadmin工具查看
#下载链接
https://sourceforge.net/projects/ldapadmin/files/ldapadmin/1.8.3/

#其中host填写OpenLDAP的主机地址，port填写OpenLDAP的监听端口，base填写的OpenLDAP的DN -> dc=test,dc=com

#在Account部分中的Username填写的是管理员，password填写的是管理员的密码。

#注意：Username部分不像我们平时使用的系统一样填写一个root，在此我们要填写完整的RDN -> cn=root,dc=test,dc=com

#卸载
#停止服务
systemctl stop slapd
systemctl disable slapd

#卸载
yum -y remove openldap-servers openldap-clients

#删除残留文件
rm -rf /var/lib/ldap

#删除ldap用户及组
userdel ldap
userdel 曾创建的其他ldap相关用户
groupdel 曾创建的其他ldap相关组

#删除openldap目录
rm -rf /etc/openldap
#注意：此处删除前，需要将该路径下的certs文件夹备份留存，重装时，此文件夹不会再下载，由此会引起OpenLDAP重装后服务无法启动

```

参考来源:[Linux的centos7中OpenLDAP的安装，卸载与重装_openldap卸载-CSDN博客](https://blog.csdn.net/weixin_45536587/article/details/120626150)
https://www.ilanni.com/?p=13775
https://blog.csdn.net/TangHao_0226/article/details/80737708
[ldap删除](https://www.cnblogs.com/cyxroot/p/11868714.html)