@echo off
chcp 65001 >nul
echo ==============================================
echo          Mizuki 博客 一键上线
echo ==============================================
echo.

echo.
echo [1/3] 构建项目...
pnpm build

echo.
echo [2/3] 提交更新...
git add .
git commit -m "feat: 自动更新笔记"

echo.
echo [3/3] 推送到 GitHub...
git push

echo.
echo ==============================================
echo          🎉 上线完成！Vercel 自动部署
echo ==============================================
pause