# 错题思维应用

一款面向家长和学生的智能错题管理应用，通过AI技术帮助学生系统化地收集、分析、学习和巩固错题。

## ✨ 功能特性

- 📸 **智能拍照识别**：使用豆包API自动识别题目内容
- ✏️ **去手写处理**：自动去除照片中的手写痕迹
- 📊 **飞书集成**：自动同步到飞书多维表格
- 🤔 **苏格拉底式引导**：使用DeepSeek AI逐步提问，引导孩子思考
- 📝 **解题清单生成**：将解题思路固化为可复用的清单和口诀
- 🎯 **刻意练习**：基于母题生成针对性反馈题

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

```bash
# 复制配置文件
cp config.example.py config.py

# 编辑 config.py，填入你的API密钥
```

或使用交互式配置向导：

```bash
python quick_start.py
```

### 3. 运行测试

```bash
# 运行基础功能测试
python test_basic.py
```

### 4. 使用

```bash
# 处理一张错题图片
python main.py path/to/question.jpg 不会
```

## 📖 详细文档

- **[NEXT_STEPS.md](NEXT_STEPS.md)** - 详细的配置和开始指南 ⭐ **推荐先看这个**
- **[USAGE.md](USAGE.md)** - 使用说明和API文档
- **[PRD.md](PRD.md)** - 产品需求文档
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - 项目开发状态

## 🏗️ 项目结构

```
错题思维/
├── README.md              # 项目说明
├── PRD.md                 # 产品需求文档
├── NEXT_STEPS.md          # 下一步行动指南
├── requirements.txt       # Python依赖
├── config.example.py      # 配置文件示例
├── main.py               # 主程序入口
├── test_basic.py         # 基础功能测试
├── quick_start.py        # 快速开始向导
├── src/
│   ├── feishu/           # 飞书多维表格集成
│   ├── ocr/              # 图片识别模块
│   ├── handwriting/      # 去手写模块
│   ├── ai/               # AI引导学习模块
│   └── utils/            # 工具函数
└── tests/                # 测试文件
```

## 🔧 配置说明

### 必需的API密钥

1. **豆包API** - 用于图片识别
   - 访问：https://www.volcengine.com/product/doubao

2. **DeepSeek API** - 用于AI引导和生成（推荐）
   - 访问：https://platform.deepseek.com/

3. **飞书应用** - 用于数据存储
   - 访问：https://open.feishu.cn/
   - 需要创建应用并获取 App ID 和 App Secret

详细配置步骤请查看 [NEXT_STEPS.md](NEXT_STEPS.md)

## 📝 使用示例

### 基础使用

```python
from main import ErrorQuestionApp

# 初始化应用
app = ErrorQuestionApp()

# 处理错题
record_id = app.process_error_question("question.jpg", "不会")

# 生成引导问题（需要提供题目文本）
result = app.start_guide_learning(record_id, question_text="题目内容")

# 生成反馈题
questions = app.generate_practice_questions(record_id, count=5, question_text="题目内容")
```

### 完整流程示例

查看 [example.py](example.py) 了解更多示例。

## 🐛 问题排查

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 检查网络连接
   - 查看日志文件 `logs/错题思维_YYYY-MM-DD.log`

2. **飞书同步失败**
   - 检查App ID和Secret
   - 检查应用权限
   - 检查表格ID和字段名称

3. **图片识别不准确**
   - 确保图片清晰
   - 尽量拍摄单题
   - 光线充足

更多问题排查请查看 [NEXT_STEPS.md](NEXT_STEPS.md)

## 📊 开发状态

当前版本：**MVP (最小可行产品)**

已完成功能：
- ✅ 图片识别和去手写
- ✅ 飞书多维表格集成
- ✅ AI引导学习
- ✅ 反馈题生成

待开发功能：
- ⏳ 数据统计和分析
- ⏳ 复习提醒系统
- ⏳ Web界面
- ⏳ 多孩子支持

详细状态请查看 [PROJECT_STATUS.md](PROJECT_STATUS.md)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请：
1. 查看文档（NEXT_STEPS.md, USAGE.md）
2. 运行测试脚本检查配置
3. 查看日志文件

---

**开始使用：运行 `python quick_start.py` 开始配置！** 🎉
