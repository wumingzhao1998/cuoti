"""
工具函数
"""

import os
from datetime import datetime
from pathlib import Path
from PIL import Image


def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def validate_image(image_path: str, max_size_mb: int = 10) -> tuple:
    """
    验证图片文件
    
    Args:
        image_path: 图片路径
        max_size_mb: 最大文件大小（MB）
        
    Returns:
        (是否有效, 错误信息)
    """
    if not os.path.exists(image_path):
        return False, "文件不存在"
    
    # 检查文件大小
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
    if file_size > max_size_mb:
        return False, f"文件大小超过{max_size_mb}MB"
    
    # 检查是否为有效图片
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True, ""
    except Exception as e:
        return False, f"无效的图片文件: {str(e)}"


def create_upload_dir(base_dir: str = "uploads") -> str:
    """
    创建上传目录
    
    Args:
        base_dir: 基础目录名
        
    Returns:
        创建的目录路径
    """
    upload_dir = Path(base_dir)
    upload_dir.mkdir(exist_ok=True)
    
    # 按日期创建子目录
    today = datetime.now().strftime("%Y-%m-%d")
    date_dir = upload_dir / today
    date_dir.mkdir(exist_ok=True)
    
    return str(date_dir)

