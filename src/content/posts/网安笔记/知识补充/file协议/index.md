---
title: "网安笔记 - 知识补充 - file协议"
category: "网安笔记"
date: 2025-10-31
published: 2025-10-31
author: "Rin"
---

## **一、URI标准结构：协议与路径的分界**

URI的通用格式遵循 **`scheme:[//authority][/path]`**的规则：

- **`scheme`**：协议类型（如`http`、`ftp`、`file`）。
- **`authority`**：通常指域名、主机地址或用户认证信息（如`user:pass@example.com:8080`）。
- **`path`**：资源的具体路径。

**示例**：

- HTTP协议：`http://example.com/path`（`//`后接域名）。
- FTP协议：`ftp://user:pass@ftp.example.com/file`（`//`后接认证和主机）。

## **二、`file:///`的三斜杠逻辑**

### **1. 本地文件的特殊性**

对于本地文件系统，`file`协议的`authority`（主机部分）通常为空，但为了保持URI格式的完整性，需保留协议后的双斜杠（`//`）。

- **问题**：若直接写为 `file://C:/path`，可能被误解析为访问名为 `C`的网络主机。
- **解决**：通过三斜杠（`///`）明确表示**无主机名**，直接指向本地根目录。

## **三、协议设计的底层逻辑**

### **1. RFC规范要求**

根据RFC 8089（File URI规范）：

> 文件URI格式为 `file://<host>/<path>`，若`host`为空（指向本地），则需保留双斜杠并直接接路径，即 `file:///path`。

### **2. 避免歧义**

- **错误写法**：`file://C:/path`可能被解析为：
    - 协议：`file`
    - 主机：`C`（网络主机名）
    - 路径：`/path`
- **正确写法**：`file:///C:/path`明确表示本地路径。

常用来读取的文件

> windows：  
> C:\boot.ini   //查看系统版本  
> C:\Windows\System32\inetsrv\MetaBase.xml    //IIS配置文件  
> C:\Windows\repair\sam      //存储系统初次安装的密码  
> C:\Program Files\mysql\my.ini   //Mysql配置  
> C:\Program Files\mysql\data\mysql\user.MYD   //Mysql root  
> C:\Windows\php.ini   //php配置信息  
> C:\Windows\my.ini   //Mysql配置信息  
> C:\Windows\win.ini   //Windows系统的一个基本系统配置文件

> linux：  
> root/.ssh/authorized_keys如需登录到远程主机，需要到.ssh目录下，新建authorized_keys文件，并将id_rsa.pub内容复制进去  
> /root/.ssh/id_rsa       //ssh私钥,ssh公钥是id_rsa.pub  
> /root/.ssh/id_ras.keystore    //记录每个访问计算机用户的公钥  
> /root/.ssh/known_hosts      //记录每个访问计算机用户的公钥  
> /etc/passwd  
> /etc/shadow   //账户密码文件  
> /etc/my.cnf   //mysql配置文件  
> /etc/httpd/conf/httpd.conf   //apache配置文件  
> /root/.bash_history      //用户历史命令记录文件  
> /root/.mysql_history     //mysql历史命令记录文件  
> /proc/mounts         //记录系统挂载设备  
> /porc/config.gz       //内核配置文件  
> /var/lib/mlocate/mlocate.db   //全文件路径  
> /porc/self/cmdline        //当前进程的cmdline参数