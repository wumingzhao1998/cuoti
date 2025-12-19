# 配置修复说明

## 问题

在 `config.py` 中，`FEISHU_APP_TOKEN` 和 `FEISHU_TABLE_ID` 的值被错误地设置为相同。

## 正确的配置

### app_token（两个表共享）

`FEISHU_APP_TOKEN` 应该是多维表格的 app_token/base_id，从URL的 `base/` 后面获取。

例如，如果URL是：
```
https://xxx.feishu.cn/base/tblchSd315sqHTCt?table=NO9nbcpjraKeUCsSQkBcHL9gnhh
```

那么 `FEISHU_APP_TOKEN = "tblchSd315sqHTCt"`

### table_id（每个表不同）

- **错题本表**：`FEISHU_TABLE_ID` 从URL的 `table=` 后面获取
- **反馈题表**：`FEISHU_FEEDBACK_TABLE_ID` 从反馈题表的URL中获取

## 已修复

`config.py` 已更新为：

```python
FEISHU_APP_TOKEN = "tblchSd315sqHTCt"  # app_token，两个表共享
FEISHU_TABLE_ID = "NO9nbcpjraKeUCsSQkBcHL9gnhh"  # 错题本表的table_id
FEISHU_FEEDBACK_TABLE_ID = "your_feedback_table_id"  # 反馈题表的table_id（需要填入）
```

## 验证

确保：
- ✅ `FEISHU_APP_TOKEN` = 两个表共享的app_token/base_id
- ✅ `FEISHU_TABLE_ID` = 错题本表的table_id
- ✅ `FEISHU_FEEDBACK_TABLE_ID` = 反馈题表的table_id（需要填入）

三个值应该都不相同！

