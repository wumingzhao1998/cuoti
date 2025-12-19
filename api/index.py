"""
Vercel Serverless Function入口
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 设置环境变量（从Vercel环境变量读取）
os.environ.setdefault('FEISHU_APP_ID', os.getenv('FEISHU_APP_ID', ''))
os.environ.setdefault('FEISHU_APP_SECRET', os.getenv('FEISHU_APP_SECRET', ''))
os.environ.setdefault('FEISHU_APP_TOKEN', os.getenv('FEISHU_APP_TOKEN', ''))
os.environ.setdefault('FEISHU_TABLE_ID', os.getenv('FEISHU_TABLE_ID', ''))
os.environ.setdefault('FEISHU_FEEDBACK_TABLE_ID', os.getenv('FEISHU_FEEDBACK_TABLE_ID', ''))
os.environ.setdefault('DOUBAO_API_KEY', os.getenv('DOUBAO_API_KEY', ''))
os.environ.setdefault('DEEPSEEK_API_KEY', os.getenv('DEEPSEEK_API_KEY', ''))

# 导入主应用
from main import ErrorQuestionApp

app = ErrorQuestionApp()

def handler(request):
    """Vercel Serverless Function处理函数"""
    # 这里可以根据需要实现HTTP接口
    # 目前返回简单的响应
    return {
        'statusCode': 200,
        'body': {
            'message': '错题思维应用已部署',
            'version': '1.0.0'
        }
    }

