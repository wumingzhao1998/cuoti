# Vercel部署指南

## 环境变量配置

在Vercel项目设置中，需要配置以下环境变量：

### 飞书配置

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `FEISHU_APP_ID` | 飞书应用ID | `cli_a9c84f993638dceb` |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | `vEa2dJyfpd0D0fDwEsBW6eoPTn3nKj3i` |
| `FEISHU_APP_TOKEN` | 多维表格的app_token（两个表共享） | `NO9nbcpjraKeUCsSQkBcHL9gnhh` |
| `FEISHU_TABLE_ID` | 错题本表的table_id | `tblchSd315sqHTCt` |
| `FEISHU_FEEDBACK_TABLE_ID` | 反馈题表的table_id | `tblz8joW4LNvzS6a` |

### API配置

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `DOUBAO_API_KEY` | 豆包API密钥（图片识别） | `3fe04017-64a1-466a-abca-ff90d02422b4` |
| `DOUBAO_API_URL` | 豆包API地址（可选） | `https://ark.cn-beijing.volces.com/api/v3/chat/completions` |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（AI引导） | `sk-90e4c69ff32a4ef1ac397e3ef02cc2b9` |
| `DEEPSEEK_API_URL` | DeepSeek API地址（可选） | `https://api.deepseek.com/v1` |

## 在Vercel中配置环境变量

### 方法1：通过Vercel Dashboard

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的项目
3. 进入 **Settings** → **Environment Variables**
4. 点击 **Add New**
5. 依次添加上述所有环境变量
6. 选择环境（Production, Preview, Development）
7. 点击 **Save**

### 方法2：通过Vercel CLI

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录
vercel login

# 添加环境变量
vercel env add FEISHU_APP_ID
vercel env add FEISHU_APP_SECRET
vercel env add FEISHU_APP_TOKEN
vercel env add FEISHU_TABLE_ID
vercel env add FEISHU_FEEDBACK_TABLE_ID
vercel env add DOUBAO_API_KEY
vercel env add DEEPSEEK_API_KEY

# 推送到生产环境
vercel env pull .env.production
```

## 更新代码以支持环境变量

需要更新 `config.py` 和 `main.py` 以从环境变量读取配置。

## 部署步骤

1. 确保所有环境变量已配置
2. 推送代码到GitHub
3. Vercel会自动检测并部署
4. 或使用 `vercel deploy` 手动部署

## 注意事项

1. **环境变量安全性**：不要在代码中硬编码API密钥
2. **文件上传**：Vercel Serverless Functions有文件大小限制（通常50MB）
3. **执行时间**：Serverless Functions有执行时间限制（通常10秒，Pro版60秒）
4. **存储**：上传的文件需要存储到外部服务（如OSS、S3等），不能存储在Vercel文件系统中

## 推荐架构调整

对于Vercel部署，建议：
1. 使用外部存储服务存储图片（如阿里云OSS、AWS S3）
2. 将图片处理改为异步任务
3. 使用API路由处理请求

