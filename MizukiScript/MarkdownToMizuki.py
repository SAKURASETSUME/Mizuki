import os

INPUT       = r"E:\Obsidian管理\运维笔记"
OUTPUT      = r"E:\Blog\Mizuki\src\content\posts\Linux笔记"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except:
        return ""

def run():
    for root, _, files in os.walk(INPUT):
        for fn in files:
            if not fn.endswith(".md"): continue
            src_path = os.path.join(root, fn)
            rel_path = os.path.relpath(root, INPUT).replace("\\", "/")
            target_dir = os.path.join(OUTPUT, rel_path, os.path.splitext(fn)[0])
            target_file = os.path.join(target_dir, "index.md")
            if os.path.exists(target_file): continue
            os.makedirs(target_dir, exist_ok=True)
            content = read_file(src_path)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    run()