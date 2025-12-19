# 配置文件总结

## 当前配置状态

### ✅ 已配置的项

1. **飞书应用配置**
   - ✅ FEISHU_APP_ID
   - ✅ FEISHU_APP_SECRET
   - ✅ FEISHU_TABLE_ID (base_id)

2. **错题本表配置**
   - ✅ FEISHU_TABLE_TOKEN (错题本表的token)

3. **API配置**
   - ✅ DOUBAO_API_KEY (豆包API)
   - ✅ DEEPSEEK_API_KEY (DeepSeek API)

### ⚠️ 需要配置的项

1. **反馈题表配置**
   - ⚠️ FEISHU_FEEDBACK_TABLE_TOKEN
   - 当前值：`"your_feedback_table_token"`
   - **需要填入实际的反馈题表token**

## 如何获取反馈题表Token

### 步骤1：在飞书中创建反馈题表

1. 打开你的飞书多维表格
2. 点击"+"按钮添加新表
3. 命名为"反馈题"
4. 按照PRD文档创建字段（见 `TABLE_SETUP.md`）

### 步骤2：获取表格Token

1. 切换到"反馈题"表
2. 查看浏览器地址栏，URL格式类似：
   ```
   https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=反馈题的token
   ```
3. 复制 `table=` 后面的部分
4. 这就是反馈题表的token

### 步骤3：更新config.py

将 `FEISHU_FEEDBACK_TABLE_TOKEN` 的值替换为实际的token：

```python
FEISHU_FEEDBACK_TABLE_TOKEN = "实际的反馈题表token"
```

## 配置验证

配置完成后，可以运行测试：

```bash
python test_basic.py
```

如果反馈题表token配置正确，生成反馈题时会自动保存到飞书表格。

## 注意事项

1. **两个表必须在同一个base中**
   - 它们共享 `FEISHU_TABLE_ID`
   - 但有不同的表格token

2. **关联字段设置**
   - 在反馈题表中，确保"母题ID"字段正确关联到错题本表

3. **可选配置**
   - 如果暂时不需要反馈题功能，可以不配置
   - 但在生成反馈题时会提示需要配置

## 完整配置示例

```python
# 飞书多维表格配置
FEISHU_APP_ID = "cli_a9c84f993638dceb"
FEISHU_APP_SECRET = "vEa2dJyfpd0D0fDwEsBW6eoPTn3nKj3i"
FEISHU_TABLE_ID = "tblchSd315sqHTCt"  # 两个表共享的base_id

# 主表：错题本
FEISHU_TABLE_TOKEN = "NO9nbcpjraKeUCsSQkBcHL9gnhh"  # 错题本表的token

# 关联表：反馈题
FEISHU_FEEDBACK_TABLE_TOKEN = "实际的反馈题表token"  # 需要填入
```

