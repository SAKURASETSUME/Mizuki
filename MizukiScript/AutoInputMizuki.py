import os
from datetime import datetime

# ================= 配置区 =================
INPUT       = r"E:\Obsidian管理\Linux笔记"
OUTPUT      = r"E:\Blog\Mizuki\src\content\posts\Linux笔记"
POSTS_ROOT  = r"E:\Blog\Mizuki\src\content\posts"
AUTHOR      = "Rin"
# =========================================

def read_file(path):
    """读取文件内容"""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    except:
        return ""

def run():
    # 1. 遍历源文件
    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            
            src_path = os.path.join(root, fn)
            # 计算相对路径 (去掉 INPUT 前缀)
            rel_path = os.path.relpath(root, INPUT).replace("\\", "/")
            # 目标目录 = OUTPUT + 相对路径 + 文件名(无后缀)
            target_dir = os.path.join(OUTPUT, rel_path, os.path.splitext(fn)[0])
            target_file = os.path.join(target_dir, "index.md")

            # 如果已存在，跳过
            if os.path.exists(target_file):
                continue

            # 创建目录
            os.makedirs(target_dir, exist_ok=True)
            
            # 读取源内容
            content = read_file(src_path)
            
            # ================= 核心：生成 YAML 头 =================
            # 获取源文件修改时间
            mtime = os.path.getmtime(src_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            
            # 计算标题和分类 (从 posts 根目录开始算)
            abs_target_dir = os.path.dirname(target_file)
            url_path = os.path.relpath(abs_target_dir, POSTS_ROOT).replace("\\", "/")
            folders = url_path.split("/")
            title = " - ".join(folders)
            category = folders[0] if folders[0] != "." else "未分类"
            # ======================================================

            # 写入完整内容
            fm = f"""---
title: "{title}"
category: "{category}"
date: {date_str}
published: {date_str}
author: "{AUTHOR}"
---

"""
            with open(target_file, "w", encoding="utf-8", newline="") as f:
                f.write(fm + content)

if __name__ == "__main__":
    run()