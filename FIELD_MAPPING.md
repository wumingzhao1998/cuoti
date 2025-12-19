# 飞书多维表格字段映射说明

## 主表：错题本

根据PRD文档，字段映射如下：

| PRD字段名 | 代码字段名 | 字段类型 | 说明 |
|----------|-----------|---------|------|
| 创建时间 | created_at | 日期时间 | 自动记录 |
| 学科 | subject | 单选 | 数学/语文/英语 |
| 错题原题 | original_image | 附件 | 原始错题照片 |
| 去手写 | cleaned_image | 附件 | 去除手写后的题目图片 |
| 知识点 | knowledge_points | 多选 | 关联知识点标签 |
| 不会/做错 | error_type | 单选 | 不会/做错 |
| 不会/做错的原因 | error_reason | 文本 | 不会/做错的原因 |
| 引导问题 | guide_questions | 文本 | AI生成的引导问题 |
| 思考过程 | thinking_process | 文本 | 学生思考过程记录 |
| 解题思路 | solution_approach | 文本 | 最终形成的解题思路 |
| 解题清单 | solution_checklist | 文本 | 标准化的解题步骤 |
| 记忆口诀 | memory_formula | 文本 | 记忆口诀 |
| 是否母题 | is_master_question | 单选 | 是/否 |
| 掌握程度 | mastery_level | 单选 | 未掌握/掌握中/已掌握 |
| 最后复习时间 | last_review_time | 日期时间 | 最后复习时间 |
| 复习次数 | review_count | 数字 | 复习次数统计 |

## 关联表：反馈题

| PRD字段名 | 代码字段名 | 字段类型 | 说明 |
|----------|-----------|---------|------|
| 创建时间 | created_at | 日期时间 | 自动记录 |
| 母题ID | master_question_id | 关联 | 关联到错题本 |
| 题目内容 | question_content | 文本 | 反馈题题目 |
| 难度 | difficulty | 单选 | 基础/进阶/挑战 |
| 答案 | standard_answer | 文本 | 标准答案 |
| 学生答案 | student_answer | 文本 | 学生作答答案 |
| 是否正确 | is_correct | 单选 | 正确/错误 |

## 重要注意事项

### 1. 字段名说明
- "不会/做错"：单选类型，值为"不会"或"做错"
- "不会/做错的原因"：文本类型，记录具体原因

### 2. 记忆口诀字段
字段名为"记忆口诀"（PRD中之前显示为"c"是手误，已更正）。

### 3. 是否母题字段
从复选框改为单选（是/否），代码中已相应调整。

### 4. 学科字段
替代了原来的"科目"和"年级"两个字段，合并为一个"学科"字段。

### 5. 创建时间
替代了原来的"录入时间"字段。

## 代码更新

已更新的文件：
- `src/feishu/models.py` - 数据模型
- `src/feishu/client.py` - 字段映射
- `main.py` - 记录创建逻辑

## 如果字段名不匹配

如果飞书表格中的实际字段名与PRD不同，需要修改 `src/feishu/client.py` 中的字段映射。

例如，如果实际字段名是"科目"而不是"学科"，需要修改：
```python
fields["学科"] = record.subject  # 改为
fields["科目"] = record.subject
```

