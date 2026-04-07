---
title: "网安笔记 - 代码审计 - php RCE 文件下载删除"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2022/webp/2476579/1647844675027-e63ddf0c-8481-4a12-b906-5874e16a3b16.webp?x-oss-process=image%2Fresize%2Cw_937%2Climit_0)

```
#漏洞关键字
SQL注入
select insert update mysql_query mysqli等

文件上传
$files,type='file'上传，move_upload_file()等

XSS跨站
print print_r echo sprintf die var_dup var_export等

文件包含
include include_once require require_once

代码执行
eval assert preg replace call user func call user func arry等

命令执行
system exec shell_exec `` passthru pcntl_exec popen proc_open

变量覆盖
extract() parse_str() importrequestvariables() $$等

反序列化:
destruct() serialize() unserialize() __Construct __destruct

其他漏洞:
unlink()file get contents()show source()file()fopen()等
```