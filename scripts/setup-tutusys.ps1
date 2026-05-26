# 一键初始化 tutusys：建表 + 灌库 + 图片上传 OSS + 更新 RDS 路径
$ErrorActionPreference = "Stop"
$BackendRoot = $PSScriptRoot | Split-Path -Parent
Set-Location $BackendRoot

Write-Host "=== 臭臭的家 tutusys 初始化 ===" -ForegroundColor Cyan
Write-Host "请确认 backend/.env 中 PG_DATABASE=tutusys" -ForegroundColor Yellow

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "未找到 python，请先激活 conda/venv"
}

python -m pip install -q -r requirements.txt
python scripts/setup_tutusys.py
exit $LASTEXITCODE
