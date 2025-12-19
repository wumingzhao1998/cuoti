# Vercel环境变量批量导入指南

## 快速开始

### 方法A：使用自动化脚本（推荐）

#### Windows用户

1. **打开PowerShell**，进入项目目录
2. **运行脚本**：
   ```powershell
   .\vercel-env-import.ps1
   ```
3. 脚本会自动：
   - 检查Vercel CLI是否安装
   - 检查是否已登录
   - 从 `.env.vercel` 文件读取所有环境变量
   - 批量导入到Vercel（Production、Preview、Development三个环境）

#### Linux/Mac用户

1. **打开终端**，进入项目目录
2. **添加执行权限**：
   ```bash
   chmod +x vercel-env-import.sh
   ```
3. **运行脚本**：
   ```bash
   ./vercel-env-import.sh
   ```

### 方法B：使用Vercel CLI手动导入

#### 前提条件

1. **安装Vercel CLI**：
   ```bash
   npm i -g vercel
   ```

2. **登录Vercel**：
   ```bash
   vercel login
   ```

3. **进入项目目录**（确保在项目根目录）

#### Windows PowerShell命令

```powershell
# 读取.env.vercel文件并逐个导入
Get-Content .env.vercel | Where-Object { 
    $_ -notmatch "^#" -and $_ -notmatch "^$" 
} | ForEach-Object {
    $parts = $_ -split "=", 2
    $key = $parts[0].Trim()
    $value = $parts[1].Trim()
    Write-Host "导入: $key" -ForegroundColor Cyan
    $value | vercel env add "$key" production preview development
}
```

#### Linux/Mac Bash命令

```bash
# 读取.env.vercel文件并逐个导入
cat .env.vercel | grep -v "^#" | grep -v "^$" | while IFS='=' read -r key value; do
    echo "导入: $key"
    echo "$value" | vercel env add "$key" production preview development
done
```

### 方法C：使用Vercel Dashboard手动添加（最安全）

如果脚本不可用，可以：

1. 打开 `.env.vercel` 文件
2. 复制每一行的内容
3. 在Vercel Dashboard中手动添加：
   - 访问 https://vercel.com/dashboard
   - 选择项目 → Settings → Environment Variables
   - 点击 Add New
   - 粘贴 Key 和 Value
   - 选择环境（Production, Preview, Development）
   - 保存

## 环境变量文件说明

`.env.vercel` 文件包含以下环境变量：

```
FEISHU_APP_ID=cli_a9c84f993638dceb
FEISHU_APP_SECRET=vEa2dJyfpd0D0fDwEsBW6eoPTn3nKj3i
FEISHU_APP_TOKEN=NO9nbcpjraKeUCsSQkBcHL9gnhh
FEISHU_TABLE_ID=tblchSd315sqHTCt
FEISHU_FEEDBACK_TABLE_ID=tblz8joW4LNvzS6a
DOUBAO_API_KEY=3fe04017-64a1-466a-abca-ff90d02422b4
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
DEEPSEEK_API_KEY=sk-90e4c69ff32a4ef1ac397e3ef02cc2b9
DEEPSEEK_API_URL=https://api.deepseek.com/v1
```

## 验证导入结果

导入完成后，验证步骤：

1. **在Vercel Dashboard中检查**：
   - 访问 https://vercel.com/dashboard
   - 选择项目 → Settings → Environment Variables
   - 确认所有9个变量都已添加

2. **使用CLI检查**（可选）：
   ```bash
   vercel env ls
   ```

3. **重新部署项目**：
   - 在Vercel Dashboard中点击 **Redeploy**
   - 或推送代码触发自动部署

## 常见问题

### Q: 脚本提示"未安装Vercel CLI"
A: 运行 `npm i -g vercel` 安装CLI

### Q: 脚本提示"未登录"
A: 运行 `vercel login` 登录Vercel账号

### Q: 导入时提示"项目未关联"
A: 确保在项目根目录运行，或先运行 `vercel link` 关联项目

### Q: 某些变量导入失败
A: 检查变量值是否包含特殊字符，可能需要转义。也可以手动在Dashboard中添加。

### Q: 如何只导入到特定环境？
A: 修改脚本中的 `production preview development` 为单个环境，如 `production`

## 安全提示

- ✅ `.env.vercel` 文件已在 `.gitignore` 中，不会被提交到Git
- ✅ 环境变量在Vercel中是加密存储的
- ⚠️ 不要将包含真实密钥的文件提交到公开仓库
- ⚠️ 如果修改了 `.env.vercel`，记得更新Vercel中的环境变量

