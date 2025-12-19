# 下一步行动指南

## 🎯 立即开始（必须完成）

### 1. 环境配置（5分钟）

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 创建配置文件
cp config.example.py config.py

# 3. 编辑 config.py，填入你的API密钥
```

**需要获取的API密钥：**
- ✅ **豆包API密钥**（必须）- 用于图片识别
  - 访问：https://www.volcengine.com/product/doubao
  - 创建应用并获取API Key
  
- ✅ **DeepSeek API密钥**（推荐）- 用于AI引导和生成
  - 访问：https://platform.deepseek.com/
  - 注册并获取API Key

### 2. 飞书配置（15-20分钟）

#### 步骤1：创建飞书应用
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录你的飞书账号
3. 创建企业自建应用
4. 获取 **App ID** 和 **App Secret**
5. 在应用权限中开启：
   - ✅ 查看、编辑、评论多维表格
   - ✅ 上传文件到云文档

#### 步骤2：创建多维表格
1. 在飞书中创建新的多维表格
2. 命名为"**吴涵的错题本**"
3. 按照PRD创建以下字段：

| 字段名 | 字段类型 | 选项/说明 |
|--------|---------|----------|
| 错题原题 | 附件 | - |
| 去手写 | 附件 | - |
| 科目 | 单选 | 数学/语文/英语 |
| 年级 | 单选 | 一年级/二年级/.../高三 |
| 知识点 | 多选 | 可自定义标签 |
| 不会/做错 | 单选 | 不会/做错 |
| 引导问题 | 文本 | - |
| 思考过程 | 文本 | - |
| 解题思路 | 文本 | - |
| 解题清单 | 文本 | - |
| 记忆口诀 | 文本 | - |
| 是否母题 | 复选框 | - |
| 掌握程度 | 单选 | 未掌握/掌握中/已掌握 |
| 录入时间 | 日期时间 | - |
| 最后复习时间 | 日期时间 | - |
| 复习次数 | 数字 | - |

#### 步骤3：获取表格ID
1. 打开多维表格
2. 在浏览器地址栏可以看到类似：`https://xxx.feishu.cn/base/xxxxxxxxxxxxx?table=tblXXXXXXXX`
3. 复制 `tblXXXXXXXX` 部分（这就是表ID）

#### 步骤4：更新代码
编辑 `src/feishu/client.py`，找到：
```python
url = f"{self.base_url}/bitable/v1/apps/{self.table_id}/tables/tblXXXXXXXX/records"
```
将 `tblXXXXXXXX` 替换为你的实际表ID。

同时，`FEISHU_TABLE_ID` 应该是表格的 base_id（从URL中获取，`base/` 后面的部分）。

### 3. 更新配置文件

编辑 `config.py`，填入所有配置：

```python
# 飞书配置
FEISHU_APP_ID = "你的App ID"
FEISHU_APP_SECRET = "你的App Secret"
FEISHU_TABLE_ID = "你的表格base_id"

# 豆包API（图片识别）
DOUBAO_API_KEY = "你的豆包API Key"
DOUBAO_API_URL = "https://ark.cn-beijing.volces.com/api/v3"

# DeepSeek API（AI引导和生成）
DEEPSEEK_API_KEY = "你的DeepSeek API Key"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
```

## 🧪 测试运行（10分钟）

### 测试1：基础功能测试

```bash
# 1. 准备一张错题图片（数学题、语文题都可以）
# 2. 将图片放到项目目录或uploads文件夹

# 3. 运行测试
python main.py path/to/your/question.jpg 不会
```

**预期结果：**
- ✅ 图片识别成功
- ✅ 去手写处理完成
- ✅ 数据保存到飞书表格

### 测试2：AI引导功能

```python
# 在Python交互环境中测试
from main import ErrorQuestionApp

app = ErrorQuestionApp()
# 先处理一张错题获取record_id
record_id = app.process_error_question("question.jpg", "不会")

# 测试引导学习（需要提供题目文本）
question_text = "你的题目文本"  # 从识别结果中获取
result = app.start_guide_learning(record_id, question_text)
print(result)
```

### 测试3：反馈题生成

```python
# 继续使用上面的record_id
questions = app.generate_practice_questions(record_id, count=3, question_text=question_text)
for q in questions:
    print(q)
```

## 🔧 问题排查

### 常见问题1：API调用失败
- ✅ 检查API密钥是否正确
- ✅ 检查网络连接
- ✅ 查看API配额是否用完
- ✅ 查看错误日志

### 常见问题2：飞书同步失败
- ✅ 检查App ID和Secret是否正确
- ✅ 检查应用权限是否开启
- ✅ 检查表格ID是否正确
- ✅ 检查字段名称是否完全一致（包括中文字符）

### 常见问题3：图片识别不准确
- ✅ 确保图片清晰
- ✅ 尽量拍摄单题
- ✅ 光线充足
- ✅ 可以尝试调整OCR提示词

## 📋 检查清单

完成以下检查项：

- [ ] Python环境已配置（Python 3.8+）
- [ ] 依赖已安装（`pip install -r requirements.txt`）
- [ ] `config.py` 已创建并配置
- [ ] 豆包API密钥已配置
- [ ] DeepSeek API密钥已配置（可选但推荐）
- [ ] 飞书应用已创建
- [ ] 飞书应用权限已开启
- [ ] 多维表格已创建
- [ ] 表格字段已按PRD创建
- [ ] 表格ID已更新到代码
- [ ] 测试图片已准备
- [ ] 基础功能测试通过
- [ ] 飞书数据同步成功

## 🚀 完成测试后的下一步

### 短期优化（1-2天）
1. **完善错误处理**
   - 添加更详细的错误提示
   - 添加重试机制
   - 添加日志记录

2. **优化用户体验**
   - 添加进度提示
   - 优化输出信息
   - 添加结果预览

3. **修复发现的问题**
   - 根据测试结果修复bug
   - 优化API调用
   - 改进去手写效果

### 中期开发（1-2周）
1. **创建Web界面**（可选）
   - 使用Flask或FastAPI
   - 提供图片上传界面
   - 显示错题列表

2. **改进去手写算法**
   - 集成更专业的服务
   - 或使用AI模型

3. **添加数据统计**
   - 错题统计图表
   - 学习进度分析

## 💡 提示

1. **先测试核心功能**：确保图片识别和飞书同步正常工作
2. **逐步完善**：不要一次性做太多，先让基础流程跑通
3. **保存测试数据**：测试时使用真实的错题图片，验证实际效果
4. **记录问题**：遇到问题及时记录，方便后续优化

## 📞 需要帮助？

如果遇到问题：
1. 查看 `USAGE.md` 详细使用指南
2. 查看 `PRD.md` 了解功能需求
3. 查看代码注释
4. 检查错误日志

---

**现在就开始：先完成环境配置和飞书设置，然后进行第一次测试！** 🎉

