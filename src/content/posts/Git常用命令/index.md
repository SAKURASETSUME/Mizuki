---
title: "Git常用命令"
category: "Git常用命令"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

### 仓库操作

bash

```bash
# 初始化新仓库
git init

# 克隆远程仓库
git clone <url>

# 查看仓库状态
git status

# 查看提交历史
git log
git log --oneline
```

### 文件操作

bash

```bash
# 添加文件到暂存区
git add <file>        # 添加特定文件
git add .             # 添加所有文件

# 提交更改
git commit -m "消息"
git commit -am "消息" # 添加并提交所有已跟踪文件的更改

# 撤销更改
git restore <file>        # 撤销工作区修改
git restore --staged <file> # 取消暂存
```

### 分支管理

bash

```bash
# 查看分支
git branch            # 本地分支
git branch -r         # 远程分支
git branch -a         # 所有分支

# 创建/切换分支
git branch <name>     # 创建分支
git checkout <name>   # 切换分支
git checkout -b <name> # 创建并切换

# 合并分支
git merge <branch>
git rebase <branch>

# 删除分支
git branch -d <name>  # 安全删除
git branch -D <name>  # 强制删除
```

### 远程操作

bash

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <url>

# 推送代码
git push origin main
git push -u origin main # 首次推送设置上游

# 拉取代码
git pull origin main
git fetch origin       # 只下载不合并
```

### 查看信息

bash

```bash
# 查看差异
git diff              # 工作区 vs 暂存区
git diff --staged     # 暂存区 vs 最后一次提交

# 查看提交详情
git show <commit>

# 查看文件历史
git blame <file>
```

### 标签管理

bash

```bash
# 创建标签
git tag v1.0.0
git tag -a v1.0.0 -m "版本说明"

# 推送标签
git push origin --tags
```

### 撤销操作

bash

```bash
# 撤销提交
git reset --soft HEAD~1 # 保留更改
git reset --hard HEAD~1 # 丢弃更改

# 修改最后一次提交
git commit --amend
```

### 暂存更改

bash

```bash
git stash            # 暂存当前更改
git stash pop        # 恢复暂存
git stash list       # 查看暂存列表
```

### 常用组合命令

bash

```bash
# 日常开发流程
git status
git add .
git commit -m "fix: 修复问题"
git push origin main

# 同步最新代码
git pull origin main

# 创建功能分支
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```