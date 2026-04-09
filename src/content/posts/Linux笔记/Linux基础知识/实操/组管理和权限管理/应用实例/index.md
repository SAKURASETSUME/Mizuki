---
title: "Linux笔记 - Linux基础知识 - 实操 - 组管理和权限管理 - 应用实例"
category: "Linux笔记"
date: 2026-03-11
published: 2026-03-11
author: "Rin"
---

## 实例1

```txt
police , bandit
jack,jerry:警察
xh,xq:土匪
1.创建组
2.创建用户
3.jack创建一个文件，自己可以读写，本组人可以读，其它组没人任何权限
4.jack修改该文件，让其它组人可以读，本组人可以读写
5.xh投靠警察，看看是否可以读写。
```

**命令 (直接复制的history 序号对不上是因为删除了多余的命令)**

```bash
  491  groupadd police
  492  groupadd bandit
  493  useradd -g police jack
  494  useradd -g police jerry
  495  id jack
  496  id jerry
  497  useradd -g bandit xh
  498  useradd -g bandit xq
  499  id xh
  500  id xq
  501  su - jack
  502  touch test.txt
  503  chmod u=rw,g=r,o= /home/jack/test.txt 
  504  ll /home/jack
  506  chmod o=r,g=rw /home/jack/test.txt
  510  usermod -g police xh 
  511  su - xh
  512  ll /home/jack/test.txt 
  515  mv /home/jack/test.txt  /opt/
  516  cat /opt/test.txt
  517  echo "123" >> /opt/test.txt
```


## 实例2

```txt
建立两个组（神仙（sx）妖怪（yg））建立四个用户（唐僧，悟空，八戒，沙僧）设置密码
把悟空，八戒放入妖怪 唐僧沙僧在神仙
用悟空建立一个文件（monkey.java 该文件要输出i am monkey）给八戒一个可以rw的权限
八戒修改monkeyjava 加入一句话（i am pig)
唐僧 沙僧 对该文件没有权限
把沙僧放入妖怪组
让沙僧修改该文件monkey，加入一句话（我是沙僧，我是妖怪！）;
对文件夹rwx的细节讨论和测试！！!
```

**命令实现**

```bash
groupadd sx
groupadd yg
useradd tangseng
useradd wukong
useradd bajie
useradd shaseng
passwd tangseng
passwd wukong
passwd bajie
passwd shaseng
usermod -g yg wukong
usermod -g yg bajie
usermod -g sx tangseng
usermod -g sx shaseng
su - wukong
touch monkey.java
vim monkey.java #写入内容
chmod 660 monkey.java
mv /home/wukong/monkey.java /opt/
logout
su - bajie
cat /opt/monkey.java
vim /opt/monkey.java #写入内容
logout
su - tangseng
cat /opt/monkey.java
echo "测试写入" >> /opt/monkey.java #预期提示：权限不足/Permission denied
logout
su - shaseng
cat /opt/monkey.java #预期提示：权限不足
echo "测试写入" >> /opt/monkey.java #预期提示：权限不足
logout
usermod -g yg shaseng
su - shaseng
cat /opt/monkey.java
vim /opt/monkey.java #写入内容
logout
```