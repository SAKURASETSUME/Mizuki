import os
from datetime import datetime

INPUT       = r"E:\Obsidian管理\Linux笔记"
OUTPUT      = r"E:\Blog\src\content\posts\Linux笔记"
POSTS_ROOT  = r"E:\Blog\src\content\posts"
AUTHOR      = "Rin"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    except:
        return ""

def run():
    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.endswith(".md"):
                continue

            src_path = os.path.join(root, fn)
            rel_path = os.path.relpath(root, INPUT).replace("\\", "/")
            target_dir = os.path.join(OUTPUT, rel_path, os.path.splitext(fn)[0])
            target_file = os.path.join(target_dir, "index.md")

            if os.path.exists(target_file):
                continue

            os.makedirs(target_dir, exist_ok=True)
            content = read_file(src_path)

            # 取源文件修改时间
            mtime = os.path.getmtime(src_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

            # 标题与分类
            abs_target_dir = os.path.dirname(target_file)
            url_path = os.path.relpath(abs_target_dir, POSTS_ROOT).replace("\\", "/")
            folders = url_path.split("/")
            title = " - ".join(folders)
            category = folders[0] if folders else "Linux笔记"

            # YAML头
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
