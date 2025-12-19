"""
反馈题生成器
"""

import requests
from typing import List, Dict, Optional
import json


class QuestionGenerator:
    """反馈题生成器"""
    
    def __init__(self, api_key: str, api_url: Optional[str] = None, 
                 model: str = "deepseek-chat", use_deepseek: bool = True):
        """
        初始化生成器
        
        Args:
            api_key: API密钥（DeepSeek或其他大模型）
            api_url: API地址
            model: 使用的模型名称（DeepSeek默认：deepseek-chat）
            use_deepseek: 是否使用DeepSeek（根据PRD推荐）
        """
        self.api_key = api_key
        if use_deepseek:
            self.api_url = api_url or "https://api.deepseek.com/v1"
            self.model = model or "deepseek-chat"
        else:
            self.api_url = api_url or "https://ark.cn-beijing.volces.com/api/v3"
            self.model = model or "doubao-pro-4k"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_feedback_questions(self, master_question: str, subject: str, 
                                    knowledge_points: List[str], error_type: str,
                                    count: int = 5) -> List[Dict]:
        """
        基于母题生成反馈题
        
        Args:
            master_question: 母题内容
            subject: 科目
            knowledge_points: 知识点列表
            error_type: 错误类型（不会/做错）
            count: 生成题目数量
            
        Returns:
            反馈题列表，每个包含题目、答案、难度等信息
        """
        url = f"{self.api_url}/chat/completions"
        
        # 根据错误类型调整生成策略
        if error_type == "不会":
            difficulty_distribution = "基础题3道，进阶题2道"
            strategy = "生成更多基础题，帮助学生巩固基本概念和解题方法"
        else:  # 做错
            difficulty_distribution = "基础题2道，进阶题2道，挑战题1道"
            strategy = "生成相似题和易错点题，帮助学生避免类似错误"
        
        prompt = f"""请基于以下母题，生成{count}道有针对性的练习题。

母题：{master_question}
科目：{subject}
知识点：{', '.join(knowledge_points)}
学生情况：{error_type}
生成策略：{strategy}
难度分布：{difficulty_distribution}

要求：
1. 保持相同的知识点和解题思路
2. 改变数值、场景或表达方式
3. 每道题都要有标准答案和简要解析
4. 难度要循序渐进

请以JSON格式返回，格式如下：
{{
    "questions": [
        {{
            "question": "题目内容",
            "answer": "标准答案",
            "explanation": "简要解析",
            "difficulty": "基础/进阶/挑战"
        }},
        ...
    ]
}}"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.8,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                data = json.loads(content)
                return data.get("questions", [])
            else:
                return []
                
        except Exception as e:
            print(f"生成反馈题失败: {e}")
            return []
    
    def generate_similar_question(self, master_question: str, subject: str) -> Dict:
        """
        生成一道相似题（快速生成）
        
        Args:
            master_question: 母题内容
            subject: 科目
            
        Returns:
            包含题目、答案、解析的字典
        """
        questions = self.generate_feedback_questions(
            master_question, subject, [], "做错", count=1
        )
        return questions[0] if questions else {}

