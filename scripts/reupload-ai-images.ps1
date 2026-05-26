# 用 dist-old-2 的 AI 原图覆盖 OSS（不重置数据库）
$ErrorActionPreference = "Stop"
$Root = (Split-Path -Parent $PSScriptRoot) | Split-Path -Parent
Set-Location (Join-Path $Root "backend")

Write-Host "1. 同步 AI 图到 app/public/assets ..." -ForegroundColor Cyan
python (Join-Path $Root "scripts\sync_ai_assets.py")

Write-Host "2. 上传到 OSS rabbit/assets/ ..." -ForegroundColor Cyan
python -c "from scripts.oss_assets import upload_all_seed_assets; upload_all_seed_assets()"

Write-Host "完成。请 Ctrl+Shift+R 强制刷新浏览器。" -ForegroundColor Green
