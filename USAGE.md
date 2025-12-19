# 使用指南

## 快速开始

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置

复制配置文件并填入你的API密钥：

```bash
cp config.example.py config.py
```

编辑 `config.py`，填入以下信息：

- **飞书配置**：
  - `FEISHU_APP_ID`: 飞书应用ID
  - `FEISHU_APP_SECRET`: 飞书应用密钥
  - `FEISHU_TABLE_ID`: 飞书多维表格ID（需要先创建表格）

- **豆包API配置**（用于图片识别）：
  - `DOUBAO_API_KEY`: 豆包API密钥
  
- **DeepSeek API配置**（用于AI引导和生成，根据PRD推荐）：
  - `DEEPSEEK_API_KEY`: DeepSeek API密钥
  - `DEEPSEEK_API_URL`: DeepSeek API地址（默认：https://api.deepseek.com/v1）

### 3. 创建飞书多维表格

在飞书中创建一个名为"吴涵的错题本"的多维表格，包含以下字段：

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 错题原题 | 附件 | 原始错题照片 |
| 去手写 | 附件 | 去除手写后的题目图片 |
| 科目 | 单选 | 数学/语文/英语 |
| 年级 | 单选 | 一年级到高三 |
| 知识点 | 多选 | 知识点标签 |
| 不会/做错 | 单选 | 不会/做错 |
| 引导问题 | 文本 | AI生成的引导问题 |
| 思考过程 | 文本 | 学生思考过程记录 |
| 解题思路 | 文本 | 最终形成的解题思路 |
| 解题清单 | 文本 | 标准化的解题步骤 |
| 记忆口诀 | 文本 | 记忆口诀 |
| 是否母题 | 复选框 | 是否作为母题 |
| 掌握程度 | 单选 | 未掌握/掌握中/已掌握 |
| 录入时间 | 日期时间 | 自动记录 |
| 最后复习时间 | 日期时间 | 最后复习时间 |
| 复习次数 | 数字 | 复习次数统计 |

**注意**：在 `src/feishu/client.py` 中，需要将 `tblXXXXXXXX` 替换为实际的表ID。

### 4. 运行应用

#### 基本使用

```bash
# 处理一张错题图片
python main.py path/to/question.jpg 不会
```

参数说明：
- 第一个参数：错题图片路径
- 第二个参数（可选）：错误类型（"不会" 或 "做错"），默认为"不会"

#### 完整流程示例

```python
from main import ErrorQuestionApp

# 初始化应用
app = ErrorQuestionApp()

# 1. 处理错题（拍照识别、去手写、保存到飞书）
record_id = app.process_error_question("question.jpg", "不会")

# 2. 生成引导问题
result = app.start_guide_learning(record_id)
questions = result["questions"]
for q in questions:
    print(q)

# 3. 生成反馈题
practice_questions = app.generate_practice_questions(record_id, count=5)
for q in practice_questions:
    print(f"题目: {q['question']}")
    print(f"答案: {q['answer']}")
```

## 功能说明

### 1. 错题录入

**功能**：自动识别题目、去除手写、保存到飞书

**流程**：
1. 拍照或选择图片
2. 使用豆包API识别题目内容
3. 分析题目（科目、年级、知识点等）
4. 去除手写痕迹
5. 保存到飞书多维表格

**使用**：
```python
record_id = app.process_error_question("question.jpg", "不会做")
```

### 2. 苏格拉底式引导

**功能**：AI生成引导问题，帮助学生思考

**流程**：
1. 分析题目和错误类型
2. 生成3-5个递进式引导问题
3. 学生回答后继续提问或总结思路
4. 生成解题清单和记忆口诀

**使用**：
```python
# 生成引导问题
result = app.start_guide_learning(record_id)

# 继续对话（需要手动实现交互）
guide = app.guide
response = guide.continue_dialogue(
    question_text="题目内容",
    current_question="第一个问题",
    student_answer="学生回答",
    conversation_history=[]
)
```

### 3. 反馈题生成

**功能**：基于母题生成针对性练习题

**流程**：
1. 分析母题的知识点和难度
2. 根据错误类型生成不同难度的题目
3. 生成标准答案和解析

**使用**：
```python
questions = app.generate_practice_questions(record_id, count=5)
```

## API说明

### 飞书API配置

1. 登录[飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 在应用权限中开启"多维表格"相关权限
5. 获取表格的 Table ID

### 豆包API配置

1. 访问[豆包开放平台](https://www.volcengine.com/product/doubao)
2. 创建应用并获取API Key
3. 配置API地址（根据实际使用的模型调整）

## 常见问题

### Q: 图片识别不准确怎么办？

A: 
- 确保图片清晰，光线充足
- 尽量拍摄单题，避免多题混杂
- 可以手动调整识别区域（需要扩展功能）

### Q: 去手写效果不好？

A: 
- 当前使用的是基础算法，效果有限
- 可以集成更专业的去手写服务（如PaddleOCR）
- 或使用AI图像修复模型

### Q: 飞书表格字段不匹配？

A: 
- 检查表格字段名称是否与代码中的一致
- 确保字段类型正确（图片、文本、单选等）
- 在 `src/feishu/client.py` 中调整字段映射

### Q: API调用失败？

A: 
- 检查API密钥是否正确
- 确认网络连接正常
- 查看API调用限制和配额
- 检查错误日志获取详细信息

## 扩展开发

### 添加新的OCR服务

在 `src/ocr/` 目录下创建新的OCR类，实现 `recognize_question` 方法。

### 改进去手写算法

在 `src/handwriting/remover.py` 中实现 `remove_handwriting_advanced` 方法，可以集成：
- PaddleOCR的去手写功能
- 图像修复模型（如inpainting）
- 第三方API服务

### 添加Web界面

可以基于Flask或FastAPI创建Web界面，提供更友好的用户体验。

## 技术支持

如有问题，请查看：
- PRD.md - 产品需求文档
- README.md - 项目说明
- 代码注释 - 详细的实现说明

