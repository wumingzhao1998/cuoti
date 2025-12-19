# Vercel Environment Variables Batch Import Script (PowerShell)

# Check if Vercel CLI is installed
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Vercel CLI not installed" -ForegroundColor Red
    Write-Host "Please install: npm i -g vercel" -ForegroundColor Yellow
    exit 1
}

# Check if logged in
try {
    vercel whoami | Out-Null
} catch {
    Write-Host "Please login to Vercel:" -ForegroundColor Yellow
    vercel login
}

# Read .env.vercel file and import environment variables
Write-Host "Starting environment variables import..." -ForegroundColor Green

$envFile = ".env.vercel"
if (-not (Test-Path $envFile)) {
    Write-Host "Error: Cannot find $envFile file" -ForegroundColor Red
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
            Write-Host "Importing: $key" -ForegroundColor Cyan
            $value | vercel env add "$key" production preview development
        }
    }
}

Write-Host "`nEnvironment variables import completed!" -ForegroundColor Green
Write-Host "Please verify all variables in Vercel Dashboard" -ForegroundColor Yellow

