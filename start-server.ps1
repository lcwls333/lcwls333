$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$port = 8080
Write-Host ""
Write-Host "明理 ClearLogic · PWA 本地服务器" -ForegroundColor Cyan
Write-Host "打开: http://localhost:$port" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止" -ForegroundColor DarkGray
Write-Host ""

if (Get-Command python -ErrorAction SilentlyContinue) {
  python -m http.server $port
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  py -m http.server $port
} else {
  Write-Host "未找到 Python。请安装 Python，或用任意静态文件服务器指向本目录。" -ForegroundColor Red
  Write-Host "例如: npx serve ." -ForegroundColor DarkGray
  exit 1
}
