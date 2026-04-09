---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - Script - 监控进程"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```bash
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

```