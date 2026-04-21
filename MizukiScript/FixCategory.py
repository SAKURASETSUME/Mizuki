import os
from datetime import datetime

OUTPUT = r"E:\Blog\Mizuki\src\content\posts\Linux笔记"
POSTS_ROOT = r"E:\Blog\Mizuki\src\content\posts"
AUTHOR = "Rin"

def read(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except:
        return ""

def fix_only():
    today = datetime.now().strftime("%Y-%m-%d")
    for root, _, files in os.walk(OUTPUT):
        for fn in files:
            if fn != "index.md": continue
            path = os.path.join(root, fn)
            try:
                with open(path, "r") as f:
                    if "---" in f.read(400): continue
            except: continue

            content = read(path)
            body = content.split("---", 2)[-1].strip() if "---" in content else content

            rel_path = os.path.relpath(root, POSTS_ROOT).replace("\\", "/")
            folders = rel_path.split("/")
            title = " - ".join(folders)
            category = "Linux笔记"

            fm = f"""---
title: "{title}"
category: "{category}"
date: {today}
published: {today}
author: "{AUTHOR}"
---

"""
            with open(path, "w", encoding="utf-8") as f:
                f.write(fm + body)

if __name__ == "__main__":
    fix_only()