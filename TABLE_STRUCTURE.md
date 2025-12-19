# 飞书多维表格结构说明

## 表格关系

根据你的说明，两个表的结构如下：

```
多维表格（Base）
├── base_id (app_token): tblchSd315sqHTCt  ← 两个表共享
├── 错题本表
│   └── table_token: NO9nbcpjraKeUCsSQkBcHL9gnhh
└── 反馈题表
    └── table_token: (需要填入)
```

## 配置说明

### 共享配置（两个表相同）

```python
FEISHU_TABLE_ID = "tblchSd315sqHTCt"  # base_id，两个表共享
```

### 独立配置（每个表不同）

```python
# 错题本表的token
FEISHU_TABLE_TOKEN = "NO9nbcpjraKeUCsSQkBcHL9gnhh"

# 反馈题表的token
FEISHU_FEEDBACK_TABLE_TOKEN = "反馈题表的实际token"
```

## API调用方式

### 错题本表操作

```python
# URL格式
url = f"/bitable/v1/apps/{base_id}/tables/{错题本table_token}/records"

# 实际示例
url = "/bitable/v1/apps/tblchSd315sqHTCt/tables/NO9nbcpjraKeUCsSQkBcHL9gnhh/records"
```

### 反馈题表操作

```python
# URL格式
url = f"/bitable/v1/apps/{base_id}/tables/{反馈题table_token}/records"

# 实际示例（需要填入反馈题表的token）
url = "/bitable/v1/apps/tblchSd315sqHTCt/tables/反馈题table_token/records"
```

## 代码实现

代码已经正确实现了这个结构：

```python
class FeishuClient:
    def __init__(self, app_id, app_secret, table_id, 
                 table_token=None, feedback_table_token=None):
        self.table_id = table_id  # base_id，两个表共享
        self.table_token = table_token  # 错题本表的token
        self.feedback_table_token = feedback_table_token  # 反馈题表的token
    
    def create_error_record(self, record):
        # 使用错题本表的token
        url = f".../apps/{self.table_id}/tables/{self.table_token}/records"
    
    def create_feedback_question(self, question):
        # 使用反馈题表的token
        url = f".../apps/{self.table_id}/tables/{self.feedback_table_token}/records"
```

## 验证配置

### 检查清单

- [x] `FEISHU_TABLE_ID` 已配置（base_id，两个表共享）
- [x] `FEISHU_TABLE_TOKEN` 已配置（错题本表的token）
- [ ] `FEISHU_FEEDBACK_TABLE_TOKEN` 需要填入（反馈题表的token）

### 如何获取反馈题表的token

1. 在飞书中打开多维表格
2. 切换到"反馈题"表
3. 查看浏览器URL：
   ```
   https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=反馈题的token
   ```
4. 复制 `table=` 后面的部分
5. 填入 `config.py` 中的 `FEISHU_FEEDBACK_TABLE_TOKEN`

## 当前配置状态

根据你的 `config.py`：

```python
FEISHU_TABLE_ID = "tblchSd315sqHTCt"  # ✅ 已配置（两个表共享）
FEISHU_TABLE_TOKEN = "NO9nbcpjraKeUCsSQkBcHL9gnhh"  # ✅ 已配置（错题本表）
FEISHU_FEEDBACK_TABLE_TOKEN = "your_feedback_table_token"  # ⚠️ 需要填入实际值
```

## 下一步

只需要在 `config.py` 中填入反馈题表的实际token即可！

