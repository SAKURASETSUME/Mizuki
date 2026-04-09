---
title: "Linux笔记 - 常用服务搭建 - 邮件服务器 - Postfix+Dovecot"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```bash
#开启防火墙25和110端口 或者直接把防火墙关了
firewall-cmd --add-port=25/tcp --permanent

firewall-cmd –-add-port=110/tcp --permanent

firewall-cmd --reload

#查看是否安装sendmail
rpm -qa | grep sendmail
#卸载掉sendmail
yum remove sendmail

#安装postfix 不过centos7一般自带
yum install postfix

#修改配置文件
vim /etc/postfix/main.cf

#修改
# 75行: 取消注释，设置hostname 
myhostname = mail.abc.com 
# 83行: 取消注释，设置域名 
mydomain = abc.com 
# 99行: 取消注释 
myorigin = $mydomain 
# 116行: 默认是localhost，我们需要修改成all
inet_interfaces = all 
# 119行: 推荐ipv4，如果支持ipv6，则可以为all 
inet_protocols = ipv4 
# 164行: 添加 
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain 
# 264行: 取消注释，指定内网和本地的IP地址范围，以网段格式 
mynetworks = 127.0.0.0/8
# 419行: 取消注释，邮件保存目录
 home_mailbox = Maildir/ 
# 571行: 添加 
smtpd_banner = $myhostname ESMTP 
# 添加到最后 
# 规定邮件最大尺寸为10M 
message_size_limit = 10485760 
# 规定收件箱最大容量为1G 
mailbox_size_limit = 1073741824 
# SMTP认证 
smtpd_sasl_type = dovecot 
smtpd_sasl_path = private/auth 
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous 
smtpd_sasl_local_domain = $myhostname 
smtpd_recipient_restrictions = permit_mynetworks,permit_auth_destination,permit_sasl_authenticated,reject

#开启postfix服务并自启动
systemctl restart postfix
systemctl enable postfix

#安装配置dovecot
#安装
yum install dovecot

#配置
vim /etc/dovecot/dovecot.conf 

# 26行: 如果不使用IPv6，请修改为* 
listen = *
#在主配置文件中的第48行，设置允许登录的网段地址，也就是说我们可以在这里限制只有来自于某个网段的用户才能使用电子邮件系统。如果想允许所有人都能使用，则不用修改本参数
login_trusted_networks = 192.168.10.0/24更改内容

#编辑文件 10-auth.conf
vim /etc/dovecot/conf.d/10-auth.conf 

# 9行: 取消注释并修改 disable_plaintext_auth = no 
# 97行: 添加 auth_mechanisms = plain login 

#编辑文件10-mail.conf
vim /etc/dovecot/conf.d/10-mail.conf

# 30行: 取消注释并添加 mail_location = maildir:~/Maildir

#编辑文件10-master.conf
vim /etc/dovecot/conf.d/10-master.conf

# 88-90行: 取消注释并添加 # Postfix smtp验证 
unix_listener /var/spool/postfix/private/auth { 
mode = 0666 
user = postfix
group = postfix
}

#编辑文件10-ssl.conf
vim /etc/dovecot/conf.d/10-ssl.conf

# 8行: 将ssl的值修改为 ssl = no

#启动dovecot并自启动
systemctl restart dovecot
systemctl enable dovecot

#添加收发邮件账户
#邮件的用户是和系统用户一致的，也就是说系统用户可以当做邮件用户，所以直接添加系统用户就行
useradd sendroot
passwd sendroot
useradd receive
passwd receive

#如果想把所有经过SMTP服务器的邮件都归档到一个用户里，这个用户可以接收所有邮件，需要做个转发，接收到邮件就转发给这个用户可使用配置里的always_bcc字段
vi /etc/postfix/main.cf
#增加
always_bcc = receive@abc.com
#重启postfix
systemctl restart postfix

#发送邮件测试
telnet  ip 25
Trying ip...
Connected to ip.
Escape character is '^]'.
220 mail.abc.com ESMTP

mail from:sendroot@abc.com
250 2.1.0 Ok
rcpt to:receive@abc.com
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject hello receive
my name is sendroot
.
250 2.0.0 Ok: queued as E7E082004AE8
quit
221 2.0.0 Bye
Connection closed by foreign host.

#接收邮件测试
telnet ip 110
Trying ip...
Connected to ip.
Escape character is '^]'.
+OK Dovecot ready.
user receive
+OK
pass Zerotwo02
+OK Logged in.
list
+OK 1 messages:
1 307
.
retr 1
+OK 307 octets
Return-Path: <sendroot@abc.com>
X-Original-To: receive@abc.com
Delivered-To: receive@abc.com
Received: from unknown (unknown [])
        by mail.abc.com (Postfix) with SMTP id E7E082004AE8
        for <receive@abc.com>; Thu, 26 Nov 2020 16:14:31 +0800 (CST)

subject hello receive
my name is sendroot
.
QUIT
+OK Logging out.

#自建邮箱客户端收发测试
#foxmail客户端
#注册其它邮箱
#创建账号 账号为receive@abc.com
#选择手动设置 SMTP和POP服务器填入部署了dovecot和postfix的服务器ip
#如果发现里面有一些crontab发给邮箱的邮件 不想要可以配置
#方法一 把crond发送的邮件设置为空白
vi /etc/crontab

SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=""

service crond restart

#方法二 修改crond服务禁用发送邮件
vi /etc/sysconfig/crond

# Settings for the CRON daemon.
# CRONDARGS= :  any extra command-line startup arguments for crond
CRONDARGS=-s -m off

systemctl restart crond.service

```

参考：[Linux搭建邮件服务器收发邮件详细步骤_linux中server2mail怎么收发邮件-CSDN博客](https://blog.csdn.net/cheng9587/article/details/110221232)