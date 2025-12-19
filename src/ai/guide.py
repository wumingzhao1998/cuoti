"""
苏格拉底式提问引导
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime


class SocraticGuide:
    """苏格拉底式引导类"""
    
    def __init__(self, api_key: str, api_url: Optional[str] = None, 
                 model: str = "deepseek-chat", use_deepseek: bool = True):
        """
        初始化引导器
        
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
    
    def generate_guide_questions(self, question_text: str, subject: str, 
                                error_type: str) -> List[str]:
        """
        生成引导问题列表
        
        Args:
            question_text: 题目文本
            subject: 科目
            error_type: 错误类型（不会/做错）
            
        Returns:
            引导问题列表
        """
        url = f"{self.api_url}/chat/completions"
        
        system_prompt = """你是一位优秀的老师，擅长使用苏格拉底式教学法引导学生思考。
你的任务是针对学生的错题，提出一系列引导性问题，帮助学生自己找到解题思路。
不要直接给出答案，而是通过提问引导学生思考。"""
        
        user_prompt = f"""题目：{question_text}
科目：{subject}
学生情况：{error_type}

请生成3-5个递进式的引导问题，帮助学生思考解题思路。
问题应该：
1. 从简单到复杂，逐步深入
2. 引导学生思考关键概念和步骤
3. 适合学生的认知水平
4. 每个问题之间要有逻辑关联

请以列表形式返回问题，每个问题一行。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                # 解析问题列表
                questions = [q.strip() for q in content.split('\n') if q.strip() and q.strip().startswith(('1', '2', '3', '4', '5', 'Q', '问'))]
                # 清理问题编号
                questions = [q.split('.', 1)[-1].strip() if '.' in q else q for q in questions]
                return questions
            else:
                return []
                
        except Exception as e:
            print(f"生成引导问题失败: {e}")
            return []
    
    def continue_dialogue(self, question_text: str, current_question: str, 
                         student_answer: str, conversation_history: List[Dict]) -> Dict:
        """
        继续对话，根据学生回答生成下一个问题或总结
        
        Args:
            question_text: 原始题目
            current_question: 当前问题
            student_answer: 学生回答
            conversation_history: 对话历史
            
        Returns:
            包含下一个问题或总结的字典
        """
        url = f"{self.api_url}/chat/completions"
        
        # 构建对话历史
        messages = [
            {
                "role": "system",
                "content": "你是一位优秀的老师，使用苏格拉底式教学法。根据学生的回答，继续提问引导，或总结解题思路。"
            }
        ]
        
        # 添加历史对话
        for item in conversation_history:
            if "question" in item:
                messages.append({"role": "user", "content": item["question"]})
            if "answer" in item:
                messages.append({"role": "assistant", "content": item["answer"]})
        
        # 添加当前对话
        messages.append({"role": "user", "content": f"题目：{question_text}\n问题：{current_question}"})
        messages.append({"role": "assistant", "content": "请回答这个问题。"})
        messages.append({"role": "user", "content": student_answer})
        messages.append({
            "role": "assistant",
            "content": "请根据学生的回答，继续提问引导（如果还需要更多引导），或总结解题思路（如果已经引导到位）。"
        })
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # 判断是继续提问还是总结
                if "?" in content or "？" in content or "接下来" in content or "那么" in content:
                    return {
                        "type": "question",
                        "content": content,
                        "is_finished": False
                    }
                else:
                    return {
                        "type": "summary",
                        "content": content,
                        "is_finished": True
                    }
            else:
                return {
                    "type": "error",
                    "content": "生成回复失败",
                    "is_finished": False
                }
                
        except Exception as e:
            return {
                "type": "error",
                "content": f"对话失败: {e}",
                "is_finished": False
            }
    
    def generate_solution_checklist(self, question_text: str, solution_approach: str, 
                                   subject: str) -> Dict[str, str]:
        """
        生成解题清单和记忆口诀
        
        Args:
            question_text: 题目文本
            solution_approach: 解题思路
            subject: 科目
            
        Returns:
            包含解题清单和记忆口诀的字典
        """
        url = f"{self.api_url}/chat/completions"
        
        prompt = f"""题目：{question_text}
科目：{subject}
解题思路：{solution_approach}

请完成以下任务：
1. 将解题思路整理成标准化的解题步骤清单（3-7步）
2. 如果适合，生成一个朗朗上口的记忆口诀（不超过20字）

请以JSON格式返回：
{{
    "checklist": ["步骤1", "步骤2", ...],
    "formula": "记忆口诀（如果没有合适的口诀，可以为空）"
}}"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                import json
                return json.loads(content)
            else:
                return {
                    "checklist": [],
                    "formula": ""
                }
                
        except Exception as e:
            print(f"生成解题清单失败: {e}")
            return {
                "checklist": [],
                "formula": ""
            }

