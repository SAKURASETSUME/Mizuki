**AutoInputMizuki : 需要自己配置一下路径 是导入笔记的脚本**

**FixCategory : 是增加笔记分类的脚本**

**MarkdownToMizuki : 是把Markdown文件转换成Mizuki模板的脚本**

**上线.bat : 是一键上线的脚本 但是要提前配好git环境 功能-> 自动构建npm git自动推送至github仓库(由于环境问题 已经移动到Mizuki文件夹中)**

**手动推送流程**

```bash
pnpm build #手动构建
git add .
git commit -m ""
git status
git push
```



**ps:脚本更新了 建议日常只使用AutoInputNewFile 这个脚本的作用是只增加新文件 已经存在的文件不进行修改**
