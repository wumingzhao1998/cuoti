"""
配置文件示例
复制此文件为 config.py 并填入实际的配置信息
"""

# 飞书多维表格配置
FEISHU_APP_ID = "your_feishu_app_id"
FEISHU_APP_SECRET = "your_feishu_app_secret"
FEISHU_APP_TOKEN = "your_app_token"  # 多维表格的app_token/base_id（两个表共享，从URL中获取，base/后面的部分）

# 主表：错题本
FEISHU_TABLE_ID = "tblXXXXXXXX"  # 错题本表的table_id（从URL中获取，table=后面的部分）

# 关联表：反馈题
FEISHU_FEEDBACK_TABLE_ID = "tblYYYYYYYY"  # 反馈题表的table_id（从URL中获取，table=后面的部分）

# 豆包API配置（用于图片识别）
DOUBAO_API_KEY = "your_doubao_api_key"
DOUBAO_API_URL = "https://ark.cn-beijing.volces.com/api/v3"  # 根据实际情况调整

# DeepSeek API配置（用于AI引导和生成，根据PRD推荐使用）
DEEPSEEK_API_KEY = "your_deepseek_api_key"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"  # DeepSeek API地址

# OpenAI配置（可选，备用方案）
OPENAI_API_KEY = "your_openai_api_key"  # 可选
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 可选

# 应用配置
APP_NAME = "错题思维"
APP_VERSION = "1.0.0"
DEBUG = True

# 文件存储配置
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

