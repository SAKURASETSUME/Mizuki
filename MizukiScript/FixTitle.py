import os
from datetime import datetime

# ================= 配置区 =================
INPUT       = r"E:\Obsidian管理\Linux笔记"
OUTPUT      = r"E:\Blog\Mizuki\src\content\posts\Linux笔记"
POSTS_ROOT  = r"E:\Blog\Mizuki\src\content\posts"
AUTHOR      = "Rin"
# =========================================

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    except:
        return ""

def run():
    # 先建立源文件到目标文件的映射
    file_map = {}
    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.endswith(".md"): continue
            name = os.path.splitext(fn)[0]
            rel = root[len(INPUT):].lstrip("\\")
            target_file = os.path.join(OUTPUT, rel, name, "index.md")
            src_file = os.path.join(root, fn)
            if os.path.exists(target_file):
                file_map[target_file] = src_file

    # 遍历目标文件进行修复
    for target_file, source_file in file_map.items():
        try:
            # 检查是否已有 frontmatter
            with open(target_file, "r", encoding="utf-8") as f:
                head = f.read(10)
            if "---" in head:
                continue # 已有头，跳过
        except:
            continue

        # 读取内容 (去掉旧的头，如果有)
        content = read_file(target_file)
        body = content.split("---", 2)[-1].strip() if "---" in content else content

        # 生成新头
        mtime = os.path.getmtime(source_file)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        
        root_dir = os.path.dirname(target_file)
        rel_path = os.path.relpath(root_dir, POSTS_ROOT).replace("\\", "/")
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
        with open(target_file, "w", encoding="utf-8", newline="") as f:
            f.write(fm + body)

if __name__ == "__main__":
    run()