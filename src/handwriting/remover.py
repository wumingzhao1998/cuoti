"""
去手写处理
"""

from typing import Optional
from pathlib import Path

# 尝试导入opencv，如果失败则使用Pillow作为替代
try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    from PIL import Image
    import io


class HandwritingRemover:
    """去手写处理类"""
    
    def __init__(self):
        """初始化去手写处理器"""
        if not HAS_OPENCV:
            import warnings
            warnings.warn(
                "opencv-python未安装，去手写功能将使用基础方法。"
                "建议安装opencv-python以获得更好的效果，或使用外部图像处理API。"
            )
    
    def remove_handwriting(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        去除图片中的手写内容
        
        注意：这是一个基础实现，实际效果可能需要更复杂的算法或AI模型
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径（可选）
            
        Returns:
            处理后的图片路径
        """
        if HAS_OPENCV:
            return self._remove_handwriting_opencv(image_path, output_path)
        else:
            # 使用Pillow的基础处理（效果有限）
            return self._remove_handwriting_pillow(image_path, output_path)
    
    def _remove_handwriting_opencv(self, image_path: str, output_path: Optional[str] = None) -> str:
        """使用OpenCV进行去手写处理"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 方法1：使用形态学操作去除细线（手写笔迹通常是细线）
        # 创建结构元素
        kernel = np.ones((3, 3), np.uint8)
        
        # 开运算：先腐蚀后膨胀，可以去除小的噪点
        opened = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # 将处理后的灰度图转换回BGR
        result = cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR)
        
        # 保存结果
        if output_path is None:
            output_path = str(Path(image_path).parent / f"cleaned_{Path(image_path).name}")
        
        cv2.imwrite(output_path, result)
        return output_path
    
    def _remove_handwriting_pillow(self, image_path: str, output_path: Optional[str] = None) -> str:
        """使用Pillow进行基础处理（Vercel部署时使用）"""
        # 基础处理：增强对比度，减少手写痕迹
        img = Image.open(image_path)
        
        # 转换为灰度图
        if img.mode != 'L':
            img = img.convert('L')
        
        # 增强对比度（简单方法）
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # 保存结果
        if output_path is None:
            output_path = str(Path(image_path).parent / f"cleaned_{Path(image_path).name}")
        
        img.save(output_path)
        return output_path
    
    def remove_handwriting_advanced(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        高级去手写方法（使用AI模型或更复杂的算法）
        
        这个方法可以集成：
        1. 深度学习模型（如PaddleOCR的去手写功能）
        2. 图像修复算法（如inpainting）
        3. 第三方API服务
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径（可选）
            
        Returns:
            处理后的图片路径
        """
        # TODO: 实现更高级的去手写算法
        # 可以调用AI模型或第三方服务
        
        # 临时使用基础方法
        return self.remove_handwriting(image_path, output_path)

