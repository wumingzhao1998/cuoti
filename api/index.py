"""
Vercel Serverless Function入口
"""

import os
import sys
import json
import traceback
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

# 在导入main之前，先创建config模块（避免main.py导入config时失败）
if 'config' not in sys.modules:
    import types
    config = types.ModuleType('config')
    config.FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', '')
    config.FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', '')
    config.FEISHU_APP_TOKEN = os.getenv('FEISHU_APP_TOKEN', '')
    config.FEISHU_TABLE_ID = os.getenv('FEISHU_TABLE_ID', '')
    config.FEISHU_FEEDBACK_TABLE_ID = os.getenv('FEISHU_FEEDBACK_TABLE_ID', '')
    config.DOUBAO_API_KEY = os.getenv('DOUBAO_API_KEY', '')
    config.DOUBAO_API_URL = os.getenv('DOUBAO_API_URL', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions')
    config.DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    config.DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
    config.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    config.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    config.APP_NAME = os.getenv('APP_NAME', '错题思维')
    config.APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    config.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    config.UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/tmp')
    config.MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', str(10 * 1024 * 1024)))
    sys.modules['config'] = config

# 延迟导入，避免初始化时出错
app = None

def get_app():
    """延迟加载应用实例"""
    global app
    if app is None:
        try:
            # 确保config模块存在
            if 'config' not in sys.modules:
                import types
                config = types.ModuleType('config')
                config.FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', '')
                config.FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', '')
                config.FEISHU_APP_TOKEN = os.getenv('FEISHU_APP_TOKEN', '')
                config.FEISHU_TABLE_ID = os.getenv('FEISHU_TABLE_ID', '')
                config.FEISHU_FEEDBACK_TABLE_ID = os.getenv('FEISHU_FEEDBACK_TABLE_ID', '')
                config.DOUBAO_API_KEY = os.getenv('DOUBAO_API_KEY', '')
                config.DOUBAO_API_URL = os.getenv('DOUBAO_API_URL', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions')
                config.DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
                config.DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
                config.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
                config.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
                config.APP_NAME = os.getenv('APP_NAME', '错题思维')
                config.APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
                config.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
                config.UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/tmp')
                config.MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', str(10 * 1024 * 1024)))
                sys.modules['config'] = config
            
            # 导入main（此时config应该已经存在）
            from main import ErrorQuestionApp
            app = ErrorQuestionApp(enable_logging=False)
        except Exception as e:
            print(f"Error initializing app: {e}")
            print(traceback.format_exc())
            raise
    return app

def handler(request):
    """
    Vercel Serverless Function处理函数
    
    Vercel Python函数格式：
    - request: dict，包含 'method', 'path', 'headers', 'body' 等
    - 返回: dict，包含 'statusCode', 'headers', 'body'
    """
    try:
        # 获取请求信息
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        query = request.get('query', {})
        
        # 处理根路径
        if path == '/' or path == '':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8'
                },
                'body': json.dumps({
                    'message': '错题思维应用已部署',
                    'version': '1.0.0',
                    'status': 'running'
                }, ensure_ascii=False)
            }
        
        # 处理健康检查
        if path == '/health':
            try:
                get_app()  # 测试应用是否可以初始化
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json; charset=utf-8'
                    },
                    'body': json.dumps({
                        'status': 'healthy',
                        'app_initialized': True
                    }, ensure_ascii=False)
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json; charset=utf-8'
                    },
                    'body': json.dumps({
                        'status': 'unhealthy',
                        'error': str(e),
                        'app_initialized': False
                    }, ensure_ascii=False)
                }
        
        # 其他路径返回404
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8'
            },
            'body': json.dumps({
                'error': 'Not Found',
                'path': path
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        # 捕获所有异常并返回错误信息
        error_info = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc() if os.getenv('DEBUG', 'false').lower() == 'true' else None
        }
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8'
            },
            'body': json.dumps(error_info, ensure_ascii=False)
        }

