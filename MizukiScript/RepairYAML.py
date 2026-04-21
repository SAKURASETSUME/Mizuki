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
    file_map = {}
    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            name = os.path.splitext(fn)[0]
            rel = root[len(INPUT):].lstrip("\\")
            target_file = os.path.join(OUTPUT, rel, name, "index.md")
            src_file = os.path.join(root, fn)
            if os.path.exists(target_file):
                file_map[target_file] = src_file

    for target_file, source_file in file_map.items():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                if "---" in f.read(10):
                    continue
        except:
            continue

        content = read_file(target_file)
        body = content.split("---", 2)[-1].strip() if "---" in content else content

        mtime = os.path.getmtime(source_file)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

        root_dir = os.path.dirname(target_file)
        rel_path = os.path.relpath(root_dir, POSTS_ROOT).replace("\\", "/")
        folders = rel_path.split("/")
        title = " - ".join(folders)
        category = folders[0] if folders else "Linux笔记"

        fm = f"""---
title: "{title}"
category: "{category}"
date: {date_str}
published: {date_str}
author: "{AUTHOR}"
---

"""
        with open(target_file, "w", encoding="utf-8", newline="") as f:
            f.write(fm + body)

if __name__ == "__main__":
    run()