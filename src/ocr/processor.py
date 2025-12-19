"""
图片处理工具
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
from pathlib import Path


class ImageProcessor:
    """图片处理类"""
    
    @staticmethod
    def preprocess_image(image_path: str, output_path: Optional[str] = None) -> str:
        """
        预处理图片（调整大小、增强对比度等）
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径（可选）
            
        Returns:
            处理后的图片路径
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # 降噪
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        # 保存
        if output_path is None:
            output_path = str(Path(image_path).parent / f"processed_{Path(image_path).name}")
        
        cv2.imwrite(output_path, denoised)
        return output_path
    
    @staticmethod
    def detect_text_regions(image_path: str) -> list:
        """
        检测图片中的文本区域
        
        Args:
            image_path: 图片路径
            
        Returns:
            文本区域列表 [(x, y, w, h), ...]
        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 使用边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤出可能是文本的矩形区域
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 过滤太小的区域
            if w > 50 and h > 20:
                text_regions.append((x, y, w, h))
        
        return text_regions
    
    @staticmethod
    def crop_question_region(image_path: str, region: Tuple[int, int, int, int], 
                            output_path: Optional[str] = None) -> str:
        """
        裁剪题目区域
        
        Args:
            image_path: 输入图片路径
            region: 区域 (x, y, w, h)
            output_path: 输出图片路径（可选）
            
        Returns:
            裁剪后的图片路径
        """
        img = cv2.imread(image_path)
        x, y, w, h = region
        
        cropped = img[y:y+h, x:x+w]
        
        if output_path is None:
            output_path = str(Path(image_path).parent / f"cropped_{Path(image_path).name}")
        
        cv2.imwrite(output_path, cropped)
        return output_path

