"""
豆包API图片识别集成
"""

import requests
import base64
from typing import Optional, Dict, Any
from pathlib import Path


class DoubaoOCR:
    """豆包OCR识别类"""
    
    def __init__(self, api_key: str, api_url: Optional[str] = None):
        """
        初始化豆包OCR
        
        Args:
            api_key: 豆包API密钥
            api_url: API地址（可选）
        """
        self.api_key = api_key
        self.api_url = api_url or "https://ark.cn-beijing.volces.com/api/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _encode_image(self, image_path: str) -> str:
        """
        将图片编码为base64
        
        Args:
            image_path: 图片路径
            
        Returns:
            base64编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def recognize_question(self, image_path: str, model: str = "doubao-vision-128k") -> Dict[str, Any]:
        """
        识别题目内容
        
        Args:
            image_path: 图片路径
            model: 使用的模型名称
            
        Returns:
            识别结果，包含题目文本等信息
        """
        # 编码图片
        image_base64 = self._encode_image(image_path)
        
        # 构建请求
        url = f"{self.api_url}/chat/completions"
        
        # 使用视觉模型识别题目
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "请识别这张图片中的题目内容，提取出完整的题目文本。如果是数学题，请保留所有数学符号和公式。"
                    }
                ]
            }
        ]
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # 提取识别结果
            if "choices" in result and len(result["choices"]) > 0:
                question_text = result["choices"][0]["message"]["content"]
                
                return {
                    "success": True,
                    "question_text": question_text,
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": "未获取到识别结果",
                    "raw_response": result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_response": None
            }
    
    def analyze_question(self, image_path: str, question_text: Optional[str] = None) -> Dict[str, Any]:
        """
        分析题目，提取科目、知识点等信息
        
        Args:
            image_path: 图片路径
            question_text: 题目文本（如果已识别）
            
        Returns:
            分析结果，包含科目、知识点、难度等
        """
        if not question_text:
            # 先识别题目
            recognize_result = self.recognize_question(image_path)
            if not recognize_result["success"]:
                return recognize_result
            question_text = recognize_result["question_text"]
        
        # 分析题目
        url = f"{self.api_url}/chat/completions"
        
        messages = [
            {
                "role": "user",
                "content": f"""请分析以下题目，提取以下信息：
1. 科目（数学/语文/英语/物理/化学/生物/历史/地理/政治）
2. 年级（一年级/二年级/.../高三）
3. 主要知识点（列出2-5个）
4. 题目类型（选择题/填空题/解答题等）
5. 难度等级（简单/中等/困难）

题目内容：
{question_text}

请以JSON格式返回，格式如下：
{{
    "subject": "科目",
    "grade": "年级",
    "knowledge_points": ["知识点1", "知识点2"],
    "question_type": "题目类型",
    "difficulty": "难度等级"
}}"""
            }
        ]
        
        data = {
            "model": "doubao-pro-4k",
            "messages": messages,
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                analysis_text = result["choices"][0]["message"]["content"]
                import json
                analysis = json.loads(analysis_text)
                
                return {
                    "success": True,
                    "analysis": analysis,
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": "未获取到分析结果",
                    "raw_response": result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_response": None
            }

