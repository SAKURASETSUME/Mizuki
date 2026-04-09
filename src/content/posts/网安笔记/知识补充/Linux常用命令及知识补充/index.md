---
title: "网安笔记 - 知识补充 - Linux常用命令及知识补充"
category: "网安笔记"
date: 2025-11-08
published: 2025-11-08
author: "Rin"
---

## 一、基本命令

```text
uname -m 显示机器的处理器架构
uname -r 显示正在使用的内核版本
dmidecode -q 显示硬件系统部件
(SMBIOS / DMI) hdparm -i /dev/hda 罗列一个磁盘的架构特性
hdparm -tT /dev/sda 在磁盘上执行测试性读取操作系统信息
arch 显示机器的处理器架构
uname -m 显示机器的处理器架构
uname -r 显示正在使用的内核版本
dmidecode -q 显示硬件系统部件 - (SMBIOS / DMI)
hdparm -i /dev/hda 罗列一个磁盘的架构特性
hdparm -tT /dev/sda 在磁盘上执行测试性读取操作
cat /proc/cpuinfo 显示CPU info的信息
cat /proc/interrupts 显示中断
cat /proc/meminfo 校验内存使用
cat /proc/swaps 显示哪些swap被使用
cat /proc/version 显示内核的版本
cat /proc/net/dev 显示网络适配器及统计
cat /proc/mounts 显示已加载的文件系统
lspci -tv 罗列 PCI 设备
lsusb -tv 显示 USB 设备
date 显示系统日期
cal 2007 显示2007年的日历表
date 041217002007.00 设置日期和时间 - 月日时分年.秒
clock -w 将时间修改保存到 BIOS
```

## 2、系统性能

```text
arch 显示机器的处理器架构
uname -m 显示机器的处理器架构
uname -r 显示正在使用的内核版本 
dmidecode -q 显示硬件系统部件 - (SMBIOS / DMI) 
hdparm -i /dev/hda 罗列一个磁盘的架构特性 
hdparm -tT /dev/sda 在磁盘上执行测试性读取操作 
cat /proc/cpuinfo 显示CPU info的信息 
cat /proc/interrupts 显示中断 
cat /proc/meminfo 校验内存使用 
cat /proc/swaps 显示哪些swap被使用 
cat /proc/version 显示内核的版本 
cat /proc/net/dev 显示网络适配器及统计 
cat /proc/mounts 显示已加载的文件系统 
lspci -tv 罗列 PCI 设备 
lsusb -tv 显示 USB 设备 
date 显示系统日期 
cal 2007 显示2007年的日历表 
date 041217002007.00 设置日期和时间 - 月日时分年.秒 
clock -w 将时间修改保存到 BIOS 
```

## 3、服务与进程

```text
netstat -ntlp :查看服务器所有被占用端口
netstat -lnp|grep 端口号/进程号/进程名 :根据查端口是否打开确认服务是否启动，配合ps命令可查服务占用的端口
常用参数：
-p：获取进程名、进程号；
-n：禁用域名解析功能，查出IP且速度快；
-l：只列出监听中的连接；
-t：只列出 TCP协议的连接。
示例：ps aux|grep tomcat netstat -lnp|grep 进程号 ：查tomcat服务占用的端口；
ps aux|grep 进程号/进程启动命令/服务名 :进程查看命令ps(可查进程状态；进程占用cpu、内存；配合netstat根据某服务端口查出进程号用于杀进程，查服务启动命令及服务路径 ）
sudo systemctl start ssh  //启动ssh服务
sudo systemctl status ssh //查看ssh状态
sudo systemctl enable ssh //设置ssh开机自启
```

## 4、开关机

```text
shutdown -h now 关闭系统
init 0 关闭系统
init 6 重启系统
telinit 0 关闭系统
shutdown -h hours:minutes & 按预定时间关闭系统 
shutdown -c 取消按预定时间关闭系统 
shutdown -r now 重启
reboot 重启
logout 注销
```

## 5、文件和目录

```text
cd /home 进入 '/ home' 目录' 
cd .. 返回上一级目录 
cd ../.. 返回上两级目录 
cd 进入个人的主目录 
cd ~user1 进入个人的主目录 
cd - 返回上次所在的目录 
pwd 显示工作路径 
ls 查看目录中的文件 
ls -F 查看目录中的文件 
ls -l 显示文件和目录的详细资料 
ls -a 显示隐藏文件 
ls *[0-9]* 显示包含数字的文件名和目录名 
tree 显示文件和目录由根目录开始的树形结构
lstree 显示文件和目录由根目录开始的树形结构
mkdir dir1 创建一个叫做 'dir1' 的目录' 
mkdir dir1 dir2 同时创建两个目录 
mkdir -p ./dir1/dir2 :递归创建目录（-p：父目录不存在时，同时建立） 
rm -f file1 删除一个叫做 'file1' 的文件' 
rmdir dir1 删除一个叫做 'dir1' 的目录' 
rm -rf 目录或文件 ：强制删除，如：rm -rf * 为删除当前目录下所有文件
rm -rf dir1 dir2 同时删除两个目录及它们的内容 
cp dir/* . 复制一个目录下的所有文件到当前工作目录 
cp -a /tmp/dir1 . 复制一个目录到当前工作目录 
cp -a dir1 dir2 复制一个目录 
file 文件或目录 ：显示文件的类型（目录、text、zip、shell脚本等）
mkdir dir1 :创建目录(dir1)（mkdir为make directory的缩写）
mkdir -p ./dir1/dir2 :递归创建目录（-p：父目录不存在时，同时建立）
touch a.txt :创建文件a.txt
rm 文件 ：删除文件
mv 原源文件名 新文件名 ：修改文件名称
mv /opt/git/g /opt/a ：移动g到opt目录下并改名为a（a目录不存在，若存在则为移动g到a目录下）
mv -t ./test a.txt b.txt ：移动多个文件到某目录下
​cp:复制文件或目录；cp命令可以将单个或多个文件复制到一个已经存在的目录下；
cp -ai /opt/11abc /opt/git/ ：复制11abc目录（或文件）到git目录下（选项a表示文件的属性也复制、目录下所有文件都复制；i表示覆盖前询问）
ln [-s] 源文件 目标文件
ln -s /opt/a.txt /opt/git/ :对文件创建软链接（快捷方式不改名还是a.txt）
ln -s /opt/a.txt /opt/git/b :（快捷方式改名为b）（下面的一样可以改名）
ln -s /opt/mulu /opt/git/ :对目录创建软链接
```

## 6、文件权限

```text
chmod [-R] 777文件或目录 ：设置权限（chmod a+rwx a=chmod ugo +rwx a=chmod 777 a）
​注： r（read）对应4，w（write）对应2，x（execute）执行对应1；
-R：递归更改文件属组，就是在更改某个目录文件的属组时，如果加上-R的参数，那么该目录下的所有文件的属组都会更改）
chmod [{ugoa}{+-=}{rwx}][文件或目录] ：如chmod u-w,g+x,o=r test.txt为user（拥有者）去掉写权限，group(所属组)加上执行权限，other(其他人)权限等于只读；
ls -lh 显示权限
ls /tmp | pr -T5 -W$COLUMNS 将终端划分成5栏显示
chmod ugo+rwx directory1 设置目录的所有人(u)、群组(g)以及其他人(o)以读（r ）、写(w)和执行(x)的权限
chmod go-rwx directory1 删除群组(g)与其他人(o)对目录的读写执行权限
chown user1 file1 改变一个文件的所有人属性
chown -R user1 directory1 改变一个目录的所有人属性并同时改变改目录下所有文件的属性
chgrp group1 file1 改变文件的群组
chown user1:group1 file1 改变一个文件的所有人和群组属性
find / -perm -u+s 罗列一个系统中所有使用了SUID控制的文件
chmod u+s /bin/file1 设置一个二进制文件的 SUID 位 - 运行该文件的用户也被赋予和所有者同样的权限
chmod u-s /bin/file1 禁用一个二进制文件的 SUID位
chmod g+s /home/public 设置一个目录的SGID 位 - 类似SUID ，不过这是针对目录的
chmod g-s /home/public 禁用一个目录的 SGID 位
chmod o+t /home/public 设置一个文件的 STIKY 位 - 只允许合法所有人删除文件
chmod o-t /home/public 禁用一个目录的 STIKY 位
chmod +x 文件路径 为所有者、所属组和其他用户添加执行的权限
chmod -x 文件路径 为所有者、所属组和其他用户删除执行的权限
chmod u+x 文件路径 为所有者添加执行的权限
chmod g+x 文件路径 为所属组添加执行的权限
chmod o+x 文件路径 为其他用户添加执行的权限
chmod ug+x 文件路径 为所有者、所属组添加执行的权限
chmod =wx 文件路径 为所有者、所属组和其他用户添加写、执行的权限，取消读权限
chmod ug=wx 文件路径 为所有者、所属组添加写、执行的权限，取消读权限
```

## 7、文件查找

```text
locate a.txt ：在系统全局范围内查找文件名包含a.txt字样的文件（比find快）;
find /home -mtime -2 ：在/home下查最近2*24小时内改动过的文件
find . -size +100M ：在当前目录及子目录下查找大于100M的文件
find . -type f ：f表示文件类型为普通文件（b/d/c/p/l/f 分别为块设备、目录、字符设备、管道、符号链接、普通文件）
find / -name file1 从 '/' 开始进入根文件系统搜索文件和目录
find / -user user1 搜索属于用户 'user1' 的文件和目录
find /home/user1 -name \*.bin 在目录 '/ home/user1' 中搜索带有'.bin' 结尾的文件
find /usr/bin -type f -atime +100 搜索在过去100天内未被使用过的执行文件
find /usr/bin -type f -mtime -10 搜索在10天内被创建或者修改过的文件
find / -name \*.rpm -exec chmod 755 '{}' \; 搜索以 '.rpm' 结尾的文件并定义其权限
find / -xdev -name \*.rpm 搜索以 '.rpm' 结尾的文件，忽略光驱、捷盘等可移动设备
locate \*.ps 寻找以 '.ps' 结尾的文件 - 先运行 'updatedb' 命令
whereis halt 显示一个二进制文件、源码或man的位置
which halt 显示一个二进制文件或可执行文件的完整路径
```

## 8、查看文件

```text
cat -n ：文件名 :显示文件内容，连行号一起显示
less 文件名 ：一页一页的显示文件内容（搜索翻页同man命令）
head [-n] 文件名 ：显示文件头n行内容，n指定显示多少行
tail [-nf] 文件名:显示文件尾几行内容,n指定显示多少行,f用于实时追踪文件的所有更新，常用于查阅正在改变的日志文件（如tail -f -n 3 a.log 表示开始显示最后3行，并在文件更新时实时追加显示，没有-n默认10行）
sed -n '2,$p' ab ：显示第二行到最后一行；
sed -n '/搜索的关键词/p' a.txt ：显示包括关键词所在行
less a.txt |grep 搜索的关键词 ：显示包括关键词所在行
cat -n a.txt |grep 搜索的关键词 ：显示包括关键词所在行（连行号一起显示）
cat filename |grep abc -A10 ：查看filename中含有abc所在行后10行（A10）、前10行（B10）内容
less a.txt|grep git ：显示关键词所在行，管道符”|”它只能处理由前面一个指令传出的正确输出信息，对错误信息信息没有直接处理能力。然后传递给下一个命令，作为标准的输入；
cat /etc/passwd |awk -F ':' '{print $1}' ：显示第一列
```

## 9、用户&权限

```text
useradd 用户名 ：创建用户
userdel -r 用户名 :删除用户：（-r表示把用户的主目录一起删除）
usermod -g 组名 用户名 ：修改用户的组
usermod -aG 组名 用户名 ：将用户添加到组
groups test ：查看test用户所在的组
passwd [ludf] 用户名 ：用户改自己密码，不需要输入用户名，选项-d:指定空口令,-l:禁用某用户，-u解禁某用户，-f：强迫用户下次登录时修改口令
groupadd 组名 ：创建用户组
groupdel 用户组 ：删除组
groupmod -n 新组名 旧组名 ：修改用户组名字
su - 用户名：完整的切换到一个用户环境（相当于登录）（建议用这个）（退出用户：exit）
su 用户名 :切换到用户的身份（环境变量等没变，导致很多命令要加上绝对路径才能执行）
sudo 命令 ：以root的身份执行命令（输入用户自己的密码，而su为输入要切换用户的密码，普通用户需设置/etc/sudoers才可用sudo）
```

## 10、压缩&解压

```text
tar
解包：tar xvf FileName.tar
打包：tar cvf FileName.tar DirName
（注：tar是打包，不是压缩！）
———————————————
.gz
解压1：gunzip FileName.gz
解压2：gzip -d FileName.gz
压缩：gzip FileName
.tar.gz
解压：tar zxvf FileName.tar.gz
压缩：tar zcvf FileName.tar.gz DirName
———————————————
.bz2
解压1：bzip2 -d FileName.bz2
解压2：bunzip2 FileName.bz2
压缩： bzip2 -z FileName
.tar.bz2
解压：tar jxvf FileName.tar.bz2
压缩：tar jcvf FileName.tar.bz2 DirName
———————————————
.bz
解压1：bzip2 -d FileName.bz
解压2：bunzip2 FileName.bz

.tar.bz
解压：tar jxvf FileName.tar.bz
———————————————
.Z
解压：uncompress FileName.Z
压缩：compress FileName
.tar.Z
解压：tar Zxvf FileName.tar.Z
压缩：tar Zcvf FileName.tar.Z DirName
———————————————
.tgz
解压：tar zxvf FileName.tgz

.tar.tgz
解压：tar zxvf FileName.tar.tgz
压缩：tar zcvf FileName.tar.tgz FileName
———————————————
.zip
解压：unzip FileName.zip
压缩：zip FileName.zip DirName
———————————————
.rar
解压：rar a FileName.rar
压缩：rar e FileName.rar
———————————————
.lha
解压：lha -e FileName.lha
压缩：lha -a FileName.lha FileName

ZIP
zip可能是目前使用得最多的文档压缩格式。它最大的优点就是在不同的操作系统平台，比如Linux， Windows以及MacOS，上使用。缺点就是支持的压缩率不是很高，而tar.gz和tar.gz2在压缩率方面做得非常好。闲话少说，我们步入正题吧：
我们可以使用下列的命令压缩一个目录：
# zip -r archive_name.zip directory_to_compress

下面是如果解压一个zip文档：
# unzip archive_name.zip
```

## 11、apt软件安装

```text
APT 软件工具 (Debian, Ubuntu 以及类似系统) 
apt-get install package_name 安装/更新一个 deb 包 
apt-cdrom install package_name 从光盘安装/更新一个 deb 包 
apt-get update 升级列表中的软件包 
apt-get upgrade 升级所有已安装的软件 
apt-get remove package_name 从系统删除一个deb包 
apt-get check 确认依赖的软件仓库正确 
apt-get clean 从下载的软件包中清理缓存 
apt-cache search searched-package 返回包含所要搜索字符串的软件包名称 
```

## 12、YUM 软件包升级器 - （Fedora, RedHat及类似系统）

```text
yum install package_name 下载并安装一个rpm包 
yum localinstall package_name.rpm 将安装一个rpm包，使用你自己的软件仓库为你解决所有依赖关系 
yum update package_name.rpm 更新当前系统中所有安装的rpm包 
yum update package_name 更新一个rpm包 
yum remove package_name 删除一个rpm包 
yum list 列出当前系统中安装的所有包 
yum search package_name 在rpm仓库中搜寻软件包 
yum clean packages 清理rpm缓存删除下载的包 
yum clean headers 删除所有头文件 
yum clean all 删除所有缓存的包和头文件 
```

## 13、磁盘空间

```text
df -h 显示已经挂载的分区列表
ls -lSr |more 以尺寸大小排列文件和目录
du -sh dir1 估算目录 'dir1' 已经使用的磁盘空间'
du -sk * | sort -rn 以容量大小为依据依次显示文件和目录的大小
rpm -q -a --qf '%10{SIZE}t%{NAME}n' | sort -k1,1n 以大小为依据依次显示已安装的rpm包所使用的空间 (fedora, redhat类系统)
dpkg-query -W -f='${Installed-Size;10}t${Package}n' | sort -k1,1n 以大小为依据显示已安装的deb包所使用的空间 (ubuntu, debian类系统)
```

## 14、文本处理

```text
cat file1 file2 ... | command <> file1_in.txt_or_file1_out.txt general syntax for text manipulation using PIPE, STDIN and STDOUT
cat file1 | command( sed, grep, awk, grep, etc...) > result.txt 合并一个文件的详细说明文本，并将简介写入一个新文件中
cat file1 | command( sed, grep, awk, grep, etc...) >> result.txt 合并一个文件的详细说明文本，并将简介写入一个已有的文件中
grep Aug /var/log/messages 在文件 '/var/log/messages'中查找关键词"Aug"
grep ^Aug /var/log/messages 在文件 '/var/log/messages'中查找以"Aug"开始的词汇
grep [0-9] /var/log/messages 选择 '/var/log/messages' 文件中所有包含数字的行
grep Aug -R /var/log/* 在目录 '/var/log' 及随后的目录中搜索字符串"Aug"
sed 's/stringa1/stringa2/g' example.txt 将example.txt文件中的 "string1" 替换成 "string2"
sed '/^$/d' example.txt 从example.txt文件中删除所有空白行
sed '/ *#/d; /^$/d' example.txt 从example.txt文件中删除所有注释和空白行
echo 'esempio' | tr '[:lower:]' '[:upper:]' 合并上下单元格内容
sed -e '1d' result.txt 从文件example.txt 中排除第一行
sed -n '/stringa1/p' 查看只包含词汇 "string1"的行
sed -e 's/ *$//' example.txt 删除每一行最后的空白字符
sed -e 's/stringa1//g' example.txt 从文档中只删除词汇 "string1" 并保留剩余全部
sed -n '1,5p;5q' example.txt 查看从第一行到第5行内容
sed -n '5p;5q' example.txt 查看第5行
sed -e 's/00*/0/g' example.txt 用单个零替换多个零
cat -n file1 标示文件的行数
cat example.txt | awk 'NR%2==1' 删除example.txt文件中的所有偶数行
echo a b c | awk '{print $1}' 查看一行第一栏
echo a b c | awk '{print $1,$3}' 查看一行的第一和第三栏
paste file1 file2 合并两个文件或两栏的内容
paste -d '+' file1 file2 合并两个文件或两栏的内容，中间用"+"区分
sort file1 file2 排序两个文件的内容
sort file1 file2 | uniq 取出两个文件的并集(重复的行只保留一份)
sort file1 file2 | uniq -u 删除交集，留下其他的行
sort file1 file2 | uniq -d 取出两个文件的交集(只留下同时存在于两个文件中的文件)
comm -1 file1 file2 比较两个文件的内容只删除 'file1' 所包含的内容
comm -2 file1 file2 比较两个文件的内容只删除 'file2' 所包含的内容
comm -3 file1 file2 比较两个文件的内容只删除两个文件共有的部分
```

## 15、**[文件系统分析](https://zhida.zhihu.com/search?content_id=173829370&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E5%88%86%E6%9E%90&zhida_source=entity)**

```text
badblocks -v /dev/hda1 检查磁盘hda1上的坏磁块
fsck /dev/hda1 修复/检查hda1磁盘上linux文件系统的完整性
fsck.ext2 /dev/hda1 修复/检查hda1磁盘上ext2文件系统的完整性
e2fsck /dev/hda1 修复/检查hda1磁盘上ext2文件系统的完整性
e2fsck -j /dev/hda1 修复/检查hda1磁盘上ext3文件系统的完整性
fsck.ext3 /dev/hda1 修复/检查hda1磁盘上ext3文件系统的完整性
fsck.vfat /dev/hda1 修复/检查hda1磁盘上fat文件系统的完整性
fsck.msdos /dev/hda1 修复/检查hda1磁盘上dos文件系统的完整性
dosfsck /dev/hda1 修复/检查hda1磁盘上dos文件系统的完整性
```

## 16、**初始化一个文件系统**

```text
mkfs /dev/hda1 在hda1分区创建一个文件系统
mke2fs /dev/hda1 在hda1分区创建一个linux ext2的文件系统
mke2fs -j /dev/hda1 在hda1分区创建一个linux ext3(日志型)的文件系统
mkfs -t vfat 32 -F /dev/hda1 创建一个 FAT32 文件系统
fdformat -n /dev/fd0 格式化一个软盘
mkswap /dev/hda3 创建一个swap文件系统
```

## 17、**备份**

```text
dump -0aj -f /tmp/home0.bak /home 制作一个 '/home' 目录的完整备份
dump -1aj -f /tmp/home0.bak /home 制作一个 '/home' 目录的交互式备份
restore -if /tmp/home0.bak 还原一个交互式备份
rsync -rogpav --delete /home /tmp 同步两边的目录
rsync -rogpav -e ssh --delete /home ip_address:/tmp 通过SSH通道rsync
rsync -az -e ssh --delete ip_addr:/home/public /home/local 通过ssh和压缩将一个远程目录同步到本地目录
rsync -az -e ssh --delete /home/local ip_addr:/home/public 通过ssh和压缩将本地目录同步到远程目录
dd bs=1M if=/dev/hda | gzip | ssh user@ip_addr 'dd of=hda.gz' 通过ssh在远程主机上执行一次备份本地磁盘的操作
dd if=/dev/sda of=/tmp/file1 备份磁盘内容到一个文件
tar -Puf backup.tar /home/user 执行一次对 '/home/user' 目录的交互式备份操作
( cd /tmp/local/ && tar c . ) | ssh -C user@ip_addr 'cd /home/share/ && tar x -p' 通过ssh在远程目录中复制一个目录内容
( tar c /home ) | ssh -C user@ip_addr 'cd /home/backup-home && tar x -p' 通过ssh在远程目录中复制一个本地目录
tar cf - . | (cd /tmp/backup ; tar xf - ) 本地将一个目录复制到另一个地方，保留原有权限及链接
find /home/user1 -name '*.txt' | xargs cp -av --target-directory=/home/backup/ --parents 从一个目录查找并复制所有以 '.txt' 结尾的文件到另一个目录
find /var/log -name '*.log' | tar cv --files-from=- | bzip2 > log.tar.bz2 查找所有以 '.log' 结尾的文件并做成一个bzip包
dd if=/dev/hda of=/dev/fd0 bs=512 count=1 做一个将 MBR (Master Boot Record)内容复制到软盘的动作
dd if=/dev/fd0 of=/dev/hda bs=512 count=1 从已经保存到软盘的备份中恢复MBR内容
```

## 18、**VIM模式**

```text
im拥有三种模式：

（1）命令模式（常规模式）

vim启动后，默认进入命令模式，任何模式都可以通过esc键回到命令模式（可以多按几次），命令模式下可以键入不同的命令完成选择、复制、粘贴、撤销等操作。
命名模式常用命令如下：
i : 在光标前插入文本；
o:在当前行的下面插入新行；
dd:删除整行；
yy：将当前行的内容放入缓冲区（复制当前行）
n+yy :将n行的内容放入缓冲区（复制n行）
p:将缓冲区中的文本放入光标后（粘贴）
u：撤销上一个操作
r:替换当前字符
/ 查找关键字

（2）插入模式

在命令模式下按 " i "键，即可进入插入模式，在插入模式可以输入编辑文本内容，使用esc键可以返回命令模式。

（3）ex模式

在命令模式中按" : "键可以进入ex模式，光标会移动到底部，在这里可以保存修改或退出vim.
ext模式常用命令如下：
:w ：保存当前的修改
:q ：退出
:q! ：强制退出，保存修改
:x  :保存并退出，相当于:wq
:set number 显示行号
:! 系统命令  执行一个系统命令并显示结果
:sh ：切换到命令行，使用ctrl+d切换回vim
```

linux下 反引号里的内容会被当做系统命令执行 比如echo `ls`

## 19、tee命令
### 一、基本功能

`tee` 命令用于从**标准输入（stdin）** 读取数据，同时将数据输出到**标准输出（stdout，通常是终端）** 和**一个或多个文件**中。其核心作用是 “分流” 数据 —— 既展示内容，又保存内容，常用于管道操作中。

### 二、语法与常用选项

#### 基本语法

bash

```bash
tee [选项] 文件名1 [文件名2 ...]
```

#### 常用选项

- `-a`（append）：追加内容到文件，而非覆盖（默认是覆盖）。
- `-i`（ignore interrupts）：忽略中断信号（如 `Ctrl+C`），确保数据完整写入文件。

### 三、主要用途

1. 保存命令输出到文件，同时在终端查看；
2. 一次性将内容写入多个文件；
3. 追加内容到文件（替代 `>>` 但同时显示内容）；
4. 结合管道（`|`）处理中间结果，同时保存过程数据。

### 四、演示示例

#### 示例 1：基本用法（保存输出并显示）

将 `ls -l` 的输出同时显示在终端，并保存到 `file_list.txt` 中：

bash

```bash
ls -l | tee file_list.txt
```

- 终端会显示 `ls -l` 的结果；
- 同时 `file_list.txt` 中会写入相同内容（若文件不存在则创建，存在则覆盖）。

#### 示例 2：追加内容（`-a` 选项）

向 `notes.txt` 追加一行内容，同时在终端显示：

bash

```bash
echo "今天学习了tee命令" | tee -a notes.txt
```

- 终端显示：`今天学习了tee命令`；
- `notes.txt` 末尾会追加该内容（不会覆盖原有内容）。

#### 示例 3：输出到多个文件

将当前时间同时写入 `time1.log` 和 `time2.log`，并在终端显示：

bash

```bash
date | tee time1.log time2.log
```

- 终端显示当前时间（如 `Tue Nov 4 10:00:00 CST 2025`）；
- `time1.log` 和 `time2.log` 中均会写入该时间。

#### 示例 4：结合管道处理中间结果

查找 `document.txt` 中包含 “error” 的行，同时显示并保存到 `errors.log`：

bash

```bash
cat document.txt | grep "error" | tee errors.log
```

- 终端显示所有含 “error” 的行；
- 这些行同时被保存到 `errors.log` 中。

#### 示例 5：忽略中断（`-i` 选项）

执行 `ping` 命令时，即使按 `Ctrl+C` 中断，仍确保输出完整保存到 `ping.log`：

bash

```bash
ping example.com | tee -i ping.log
```

- 终端实时显示 `ping` 结果；
- 按 `Ctrl+C` 后，`ping.log` 会完整保存中断前的所有输出（若不加 `-i`，可能丢失最后部分数据）。

### 五、总结

`tee` 是管道操作中常用的 “分流工具”，核心价值是 “一边显示，一边保存”。通过 `-a` 追加、`-i` 抗中断等选项，可灵活应对不同场景（如日志记录、中间结果保存等）。