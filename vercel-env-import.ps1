# Vercel环境变量批量导入脚本 (PowerShell版本)

# 检查是否安装了Vercel CLI
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装Vercel CLI" -ForegroundColor Red
    Write-Host "请先安装: npm i -g vercel" -ForegroundColor Yellow
    exit 1
}

# 检查是否已登录
try {
    vercel whoami | Out-Null
} catch {
    Write-Host "请先登录Vercel:" -ForegroundColor Yellow
    vercel login
}

# 读取.env.vercel文件并导入环境变量
Write-Host "开始导入环境变量..." -ForegroundColor Green

$envFile = ".env.vercel"
if (-not (Test-Path $envFile)) {
    Write-Host "错误: 找不到 $envFile 文件" -ForegroundColor Red
    exit 1
}

Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    
    # 跳过空行和注释
    if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) {
        return
    }
    
    # 解析键值对
    if ($line -match "^([^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        if ($key -and $value) {
            Write-Host "导入: $key" -ForegroundColor Cyan
            $value | vercel env add "$key" production preview development
        }
    }
}

Write-Host "`n环境变量导入完成！" -ForegroundColor Green
Write-Host "请在Vercel Dashboard中验证所有变量是否已正确添加" -ForegroundColor Yellow

