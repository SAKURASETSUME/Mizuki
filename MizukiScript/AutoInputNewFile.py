import os
from datetime import datetime

# ================= 配置区 =================
INPUT = r"E:\Obsidian管理\Linux笔记"
POSTS_ROOT = r"E:\Mizuki\Blog\src\content\posts"
BLOG_ROOT = os.path.join(POSTS_ROOT, "Linux笔记")   # 只同步到这里
AUTHOR = "Rin"
ROOT_NAME = "Linux笔记"
# =========================================


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    except:
        return ""


def build_target_path(src_file):
    """
    源文件:
    E:\Obsidian管理\Linux笔记\数据库\基础\事务\test.md

    输出:
    E:\Blog\src\content\posts\Linux笔记\数据库\基础\事务\test\index.md
    """
    rel_file = os.path.relpath(src_file, INPUT)
    rel_no_ext = os.path.splitext(rel_file)[0]

    target_dir = os.path.join(BLOG_ROOT, rel_no_ext)
    target_file = os.path.join(target_dir, "index.md")

    return target_dir, target_file


def build_title(target_dir):
    rel_dir = os.path.relpath(target_dir, POSTS_ROOT)
    parts = rel_dir.replace("\\", "/").split("/")
    return " - ".join(parts)
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
    except Exception as e:
        print("读取失败:", path, e)
        return ""


def run():
    print("开始扫描...")
    print("源目录:", INPUT)
    print("目标目录:", OUTPUT)

    if not os.path.exists(INPUT):
        print("源目录不存在！")
        return

    os.makedirs(OUTPUT, exist_ok=True)

    total = 0
    created = 0
    skipped = 0

    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue

            total += 1

            src_path = os.path.join(root, fn)
            rel_path = os.path.relpath(root, INPUT)

            target_dir = os.path.join(
                OUTPUT,
                rel_path,
                os.path.splitext(fn)[0]
            )

            target_file = os.path.join(target_dir, "index.md")

            # 已存在则跳过
            if os.path.exists(target_file):
                skipped += 1
                print("跳过:", target_file)
                continue

            os.makedirs(target_dir, exist_ok=True)

            content = read_file(src_path)

            mtime = os.path.getmtime(src_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

            url_path = os.path.relpath(target_dir, POSTS_ROOT).replace("\\", "/")
            folders = url_path.split("/")
            title = " - ".join(folders)

            fm = f"""---
title: "{title}"
category: "Linux笔记"
date: {date_str}
published: {date_str}
author: "{AUTHOR}"
---

"""

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(fm + content)

            created += 1
            print("已生成:", target_file)

    print()
    print("扫描完成")
    print("Markdown文件总数:", total)
    print("新增文件:", created)
    print("跳过文件:", skipped)


if __name__ == "__main__":
    run()
def get_date_str(path):
    mtime = os.path.getmtime(path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def run():
    # 保证 Linux笔记 根目录存在
    os.makedirs(BLOG_ROOT, exist_ok=True)

    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue

            src_path = os.path.join(root, fn)
            target_dir, target_file = build_target_path(src_path)

            # 只判断 Linux笔记 对应位置是否存在
            if os.path.exists(target_file):
                continue

            os.makedirs(target_dir, exist_ok=True)

            content = read_file(src_path)
            date_str = get_date_str(src_path)
            title = build_title(target_dir)

            front_matter = f"""---
title: "{title}"
category: "{ROOT_NAME}"
date: {date_str}
published: {date_str}
author: "{AUTHOR}"
---

"""

            with open(target_file, "w", encoding="utf-8", newline="") as f:
                f.write(front_matter + content)

            print("已生成:", target_file)


if __name__ == "__main__":
    run()