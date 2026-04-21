import os
from datetime import datetime

POSTS_ROOT  = r"E:\Blog\Mizuki\src\content\posts"
AUTHOR      = "Rin"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    except:
        return ""

def run():
    for root, _, files in os.walk(POSTS_ROOT):
        for fn in files:
            if fn != "index.md": continue
            path = os.path.join(root, fn)
            
            content = read_file(path)
            body = content.split("---", 2)[-1].strip() if "---" in content else content

            # 计算日期 (用文件修改时间)
            mtime = os.path.getmtime(path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

            rel_path = os.path.relpath(root, POSTS_ROOT).replace("\\", "/")
            folders = rel_path.split("/")
            title = " - ".join(folders)
            category = folders[0] if folders[0] != "." else "未分类"

            fm = f"""---
title: "{title}"
category: "{category}"
date: {date_str}
published: {date_str}
author: "{AUTHOR}"
---

"""
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(fm + body)

if __name__ == "__main__":
    run()