# Vercel环境变量配置清单

## 快速配置

在Vercel Dashboard的 **Settings** → **Environment Variables** 中添加以下环境变量：

## 必需的环境变量

### 1. 飞书配置（5个）

```
FEISHU_APP_ID=cli_a9c84f993638dceb
FEISHU_APP_SECRET=vEa2dJyfpd0D0fDwEsBW6eoPTn3nKj3i
FEISHU_APP_TOKEN=NO9nbcpjraKeUCsSQkBcHL9gnhh
FEISHU_TABLE_ID=tblchSd315sqHTCt
FEISHU_FEEDBACK_TABLE_ID=tblz8joW4LNvzS6a
```

### 2. API配置（2个必需，2个可选）

```
DOUBAO_API_KEY=3fe04017-64a1-466a-abca-ff90d02422b4
DEEPSEEK_API_KEY=sk-90e4c69ff32a4ef1ac397e3ef02cc2b9
```

可选：
```
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
DEEPSEEK_API_URL=https://api.deepseek.com/v1
```

## 配置步骤

### 方法1：Vercel Dashboard（推荐）

1. 访问 https://vercel.com/dashboard
2. 选择你的项目
3. 点击 **Settings** → **Environment Variables**
4. 点击 **Add New** 按钮
5. 依次添加每个变量：
   - **Key**: 变量名（如 `FEISHU_APP_ID`）
   - **Value**: 变量值（从你的config.py中复制）
   - **Environment**: 选择 Production, Preview, Development（或全部）
6. 点击 **Save**
7. 重复步骤4-6，添加所有变量

### 方法2：批量导入（如果支持）

可以创建一个 `.env` 文件格式的文本，然后批量导入。

## 环境变量说明

| 变量名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `FEISHU_APP_ID` | 字符串 | ✅ | 飞书应用ID |
| `FEISHU_APP_SECRET` | 字符串 | ✅ | 飞书应用密钥 |
| `FEISHU_APP_TOKEN` | 字符串 | ✅ | 多维表格app_token（两个表共享） |
| `FEISHU_TABLE_ID` | 字符串 | ✅ | 错题本表的table_id |
| `FEISHU_FEEDBACK_TABLE_ID` | 字符串 | ✅ | 反馈题表的table_id |
| `DOUBAO_API_KEY` | 字符串 | ✅ | 豆包API密钥 |
| `DEEPSEEK_API_KEY` | 字符串 | ✅ | DeepSeek API密钥 |
| `DOUBAO_API_URL` | 字符串 | ⚪ | 豆包API地址（可选） |
| `DEEPSEEK_API_URL` | 字符串 | ⚪ | DeepSeek API地址（可选） |

## 验证配置

配置完成后：

1. 重新部署项目（Vercel会自动使用新的环境变量）
2. 或在Vercel Dashboard中点击 **Redeploy**

## 安全提示

- ✅ 环境变量在Vercel中是加密存储的
- ✅ 不会出现在代码仓库中
- ✅ 每个环境（Production/Preview/Development）可以有不同的值
- ⚠️ 不要将环境变量值提交到Git仓库

## 当前配置值

根据你的 `config.py`，需要配置的值：

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

## 部署后检查

部署完成后，检查：
1. 环境变量是否正确加载
2. API调用是否正常
3. 飞书连接是否成功

