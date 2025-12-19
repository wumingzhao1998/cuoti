"""
Vercel Serverless Function入口
"""

import os
import sys
import json
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
    """
    Vercel Serverless Function处理函数
    
    Args:
        request: Vercel请求对象
        
    Returns:
        HTTP响应
    """
    # 获取请求方法和路径
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    
    # 处理根路径
    if path == '/' or path == '':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': '错题思维应用已部署',
                'version': '1.0.0',
                'status': 'running'
            }, ensure_ascii=False)
        }
    
    # 处理健康检查
    if path == '/health':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'status': 'healthy'
            }, ensure_ascii=False)
        }
    
    # 其他路径返回404
    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'error': 'Not Found',
            'path': path
        }, ensure_ascii=False)
    }

