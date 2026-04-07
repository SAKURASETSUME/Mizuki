---
title: "系统权限划分"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/面试题/系统权限划分/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```txt
如果你是系统管理员，在进行Linux系统权限划分时，应考虑哪些因素
```

```txt
首先阐述Linux权限的主要对象
可以阐述一下文件权限的含义 -> 文件的rwx权限和文件夹的rwx权限
权限修改 -R 权限递归项

根据自己的实际经验谈考虑因素
注意权限分离，比如：工作中，Linux系统权限和数据库权限不要在同一个部门
权限最小原则（即：在满足使用的情况下最少优先）
减少使用root用户，尽量用普通用户+sudo提权进行日常操作。
重要的系统文件，比如/etc/passwd，/etc/shadowetc/fstab，/etc/sudoers等，日常建议使用chattr锁定，需要操作时再打开。【演示比如：锁定/ect/password让任何用户都不能随意useradd除非解除锁定】
使用SUID，SGID，Sticky设置特殊权限。
可以利用工具，比如chkrootkit/rootkit hunter检测rootkit脚本（rootkit是入侵者使用工具，在不察觉的建立了入侵系统途径）【演示使用                           wget ftp://ftp.pangeia.com.br/pub/seg/pac/chkrootkit.tar.gz】
利用工具Tripwire 检测文件系统完整性
```

```bash
chattr -i /etc/passwd #锁定文件

#为了防止黑客使用 把chattr移动一个位置
#首先查看chattr在哪
which chattr
#移动
mv /usr/bin/chattr /opt
#但是find可以找到
find / -name chattr

#解决方法：移动之后改个名
mv /opt/chattr /opt/aaa

#解锁
#就是上面的逆向流程
#把名字改回去
mv /opt/aaa /opt/chattr
#放到原来的位置
mv /opt/chattr /usr/bin/
#解锁
chattr -i /etc/passwd
```