# 双表格配置说明

## 概述

根据PRD文档，应用需要两个飞书多维表格：
1. **主表：错题本** - 存储错题记录
2. **关联表：反馈题** - 存储基于母题生成的反馈题

两个表在同一个多维表格（base）中，共享同一个 `FEISHU_TABLE_ID`，但有不同的表格token。

## 配置步骤

### 1. 在飞书中创建两个表

#### 创建错题本表
1. 在飞书多维表格中创建第一个表
2. 命名为"错题本"或你喜欢的名称
3. 按照PRD文档创建所有字段（见 `TABLE_SETUP.md`）

#### 创建反馈题表
1. 在同一多维表格中，点击"+"添加新表
2. 命名为"反馈题"
3. 按照PRD文档创建所有字段（见 `TABLE_SETUP.md`）

### 2. 获取表格Token

#### 获取错题本表Token
1. 切换到"错题本"表
2. 查看浏览器URL，格式类似：
   ```
   https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=NO9nbcpjraKeUCsSQkBcHL9gnhh
   ```
3. `table=` 后面的部分就是错题本表的token
4. 复制这个token，填入 `FEISHU_TABLE_TOKEN`

#### 获取反馈题表Token
1. 切换到"反馈题"表
2. 查看浏览器URL，格式类似：
   ```
   https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=另一个token
   ```
3. `table=` 后面的部分就是反馈题表的token
4. 复制这个token，填入 `FEISHU_FEEDBACK_TABLE_TOKEN`

### 3. 配置config.py

```python
# 飞书多维表格配置
FEISHU_APP_ID = "your_app_id"
FEISHU_APP_SECRET = "your_app_secret"
FEISHU_TABLE_ID = "tblchSd315sqHTCt"  # 两个表共享的base_id

# 主表：错题本
FEISHU_TABLE_TOKEN = "NO9nbcpjraKeUCsSQkBcHL9gnhh"  # 错题本表的token

# 关联表：反馈题
FEISHU_FEEDBACK_TABLE_TOKEN = "your_feedback_table_token"  # 反馈题表的token
```

### 4. 设置关联字段

在反馈题表中：
1. 创建"母题ID"字段
2. 字段类型选择"关联"
3. 关联到"错题本"表
4. 选择关联方式（推荐"多对一"）

## 代码更新说明

### 已更新的文件

1. **config.py / config.example.py**
   - 添加了 `FEISHU_FEEDBACK_TABLE_TOKEN` 配置项

2. **src/feishu/client.py**
   - `__init__` 方法添加了 `feedback_table_token` 参数
   - 实现了 `create_feedback_question` 方法

3. **main.py**
   - 更新了 `FeishuClient` 初始化，传入反馈题表token
   - `generate_practice_questions` 方法现在会自动保存反馈题到飞书

## 使用说明

### 生成反馈题并保存

```python
from main import ErrorQuestionApp

app = ErrorQuestionApp()

# 处理错题
record_id = app.process_error_question("question.jpg", "不会")

# 生成反馈题（会自动保存到飞书反馈题表）
questions = app.generate_practice_questions(
    record_id, 
    count=5, 
    question_text="题目文本"
)
```

### 单独创建反馈题记录

```python
from src.feishu.models import FeedbackQuestion
from datetime import datetime

feedback = FeedbackQuestion(
    master_question_id="record_id_from_error_table",
    question_content="反馈题题目",
    difficulty="基础",
    standard_answer="标准答案",
    student_answer=None,
    is_correct=None,
    created_at=datetime.now()
)

feedback_id = app.feishu_client.create_feedback_question(feedback)
```

## 注意事项

1. **两个表必须在同一个base中**
   - 它们共享同一个 `FEISHU_TABLE_ID`
   - 但有不同的表格token

2. **关联字段设置**
   - 确保反馈题表中的"母题ID"字段正确关联到错题本表
   - 关联字段的值应该是错题本表的记录ID

3. **可选配置**
   - 如果暂时不需要反馈题功能，可以不配置 `FEISHU_FEEDBACK_TABLE_TOKEN`
   - 但在调用 `create_feedback_question` 时会提示需要配置

## 验证配置

运行测试脚本：

```bash
python test_basic.py
```

如果配置正确，应该能够：
- ✅ 创建错题记录到错题本表
- ✅ 创建反馈题记录到反馈题表（如果配置了反馈题表token）

