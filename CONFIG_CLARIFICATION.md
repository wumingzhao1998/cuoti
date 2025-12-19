# 配置说明澄清

## 飞书多维表格结构

根据你的说明，正确的结构是：

```
多维表格应用（App）
├── app_token/base_id: tblchSd315sqHTCt  ← 两个表共享
├── 错题本表
│   └── table_id: NO9nbcpjraKeUCsSQkBcHL9gnhh
└── 反馈题表
    └── table_id: (需要填入)
```

## 配置变量说明

### 共享配置（两个表相同）

```python
FEISHU_APP_TOKEN = "tblchSd315sqHTCt"  # app_token/base_id，两个表共享
```

### 独立配置（每个表不同）

```python
# 错题本表的table_id
FEISHU_TABLE_ID = "NO9nbcpjraKeUCsSQkBcHL9gnhh"

# 反馈题表的table_id
FEISHU_FEEDBACK_TABLE_ID = "反馈题表的实际table_id"
```

## API调用格式

### 错题本表

```
/bitable/v1/apps/{app_token}/tables/{错题本table_id}/records
```

实际示例：
```
/bitable/v1/apps/tblchSd315sqHTCt/tables/NO9nbcpjraKeUCsSQkBcHL9gnhh/records
```

### 反馈题表

```
/bitable/v1/apps/{app_token}/tables/{反馈题table_id}/records
```

实际示例（需要填入反馈题表的table_id）：
```
/bitable/v1/apps/tblchSd315sqHTCt/tables/{反馈题table_id}/records
```

## 配置更新

### 已更新的变量名

为了更清晰地表达含义，已更新配置变量名：

| 旧变量名 | 新变量名 | 说明 |
|---------|---------|------|
| `FEISHU_TABLE_ID` | `FEISHU_APP_TOKEN` | app_token/base_id（两个表共享） |
| `FEISHU_TABLE_TOKEN` | `FEISHU_TABLE_ID` | 错题本表的table_id |
| `FEISHU_FEEDBACK_TABLE_TOKEN` | `FEISHU_FEEDBACK_TABLE_ID` | 反馈题表的table_id |

### 兼容性

代码中已添加兼容逻辑，旧的变量名仍然可以使用，但建议使用新的变量名。

## 当前配置

根据你的 `config.py`，需要更新为：

```python
# 飞书多维表格配置
FEISHU_APP_ID = "cli_a9c84f993638dceb"
FEISHU_APP_SECRET = "vEa2dJyfpd0D0fDwEsBW6eoPTn3nKj3i"
FEISHU_APP_TOKEN = "tblchSd315sqHTCt"  # app_token，两个表共享

# 主表：错题本
FEISHU_TABLE_ID = "NO9nbcpjraKeUCsSQkBcHL9gnhh"  # 错题本表的table_id

# 关联表：反馈题
FEISHU_FEEDBACK_TABLE_ID = "反馈题表的实际table_id"  # 需要填入
```

## 如何获取table_id

1. 在飞书中打开多维表格
2. 切换到对应的表（错题本或反馈题）
3. 查看浏览器URL：
   ```
   https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=NO9nbcpjraKeUCsSQkBcHL9gnhh
   ```
4. `table=` 后面的部分就是该表的table_id

## 验证

配置完成后，代码会：
- 使用 `FEISHU_APP_TOKEN` 作为app_token（两个表共享）
- 使用 `FEISHU_TABLE_ID` 作为错题本表的table_id
- 使用 `FEISHU_FEEDBACK_TABLE_ID` 作为反馈题表的table_id

