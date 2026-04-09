---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - keepalived - 实操 - keepalived感知nginx"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 关于keepalived对nginx状态未知的问题
**如果不进行进一步的配置 keepalived只能监听服务器是否存活 不能监听服务器里的某一个服务是否正在正常运行**

## 解决方法

**产生这个问题的原因是keepalived监控的是网卡接口的IP状态 无法监控服务状态**
**所以我们要写脚本来解决这个问题 一旦某个服务停止了 那么就杀死keepalived进程就可以了**

```bash
vim /etc/keepalived/ck_ng.sh

#写入
#!/bin/bash
LOG_FILE="/var/log/nginx_monitor.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> ${LOG_FILE}
}

# 检查nginx进程数量
counter=$(ps -C nginx --no-heading | wc -l)

# 如果nginx进程不存在
if [ ${counter} -eq 0 ]; then
    log "检测到nginx进程不存在，尝试启动nginx..."
    systemctl start nginx
    sleep 5

    # 再次检测
    counter=$(ps -C nginx --no-heading | wc -l)
    if [ ${counter} -eq 0 ]; then
        log "nginx启动失败，停止keepalived触发主备切换！"
        systemctl stop keepalived
        log "keepalived已停止，主备切换完成"
    else
        log "nginx启动成功，当前进程数：${counter}"
    fi
fi



#每个服务器都要写上面的脚本

chmod +x /etc/keepalived/ck_ng.sh

#定期执行
crontab -e

*/1 * * * * sh /etc/keepalived/ck_ng.sh

#启动监控脚本 把前面keepalived的监控注释清了就行
#重启keepalived和nginx

```