"""
飞书多维表格API客户端
"""

import os
import time
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

from .models import ErrorRecord, FeedbackQuestion


class FeishuClient:
    """飞书多维表格API客户端"""
    
    def __init__(self, app_id: str, app_secret: str, app_token: str, 
                 table_id: Optional[str] = None, feedback_table_id: Optional[str] = None):
        """
        初始化飞书客户端
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            app_token: 多维表格的app_token/base_id（两个表共享，从URL中获取，base/后面的部分）
            table_id: 错题本表的table_id/table_token（从URL中获取，table=后面的部分）
            feedback_table_id: 反馈题表的table_id/table_token（可选，如果配置了反馈题表）
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_token = app_token  # app_token/base_id，两个表共享
        self.table_id = table_id or "tblXXXXXXXX"  # 错题本表的table_id
        self.feedback_table_id = feedback_table_id  # 反馈题表的table_id
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0
        
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        # 如果token未过期，直接返回
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        # 获取新token
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取token失败: {result.get('msg')}")
        
        self.access_token = result["tenant_access_token"]
        # token有效期通常是2小时，提前5分钟刷新
        self.token_expires_at = time.time() + result.get("expire", 7200) - 300
        
        return self.access_token
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self._get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def _upload_file(self, file_path: str) -> str:
        """
        上传文件到飞书
        
        Args:
            file_path: 本地文件路径
            
        Returns:
            文件token，用于插入到表格中
        """
        url = f"{self.base_url}/im/v1/files"
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}"
        }
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'file_type': 'image', 'file_name': os.path.basename(file_path)}
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"上传文件失败: {result.get('msg')}")
            
            return result["data"]["file_token"]
    
    def create_error_record(self, record: ErrorRecord) -> str:
        """
        创建错题记录
        
        Args:
            record: 错题记录对象
            
        Returns:
            创建的记录ID
        """
        url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        
        # 构建字段数据
        fields = {}
        
        # 上传附件（错题原题和去手写）
        if record.original_image:
            if os.path.exists(record.original_image):
                file_token = self._upload_file(record.original_image)
                fields["错题原题"] = [{"file_token": file_token}]
        
        if record.cleaned_image:
            if os.path.exists(record.cleaned_image):
                file_token = self._upload_file(record.cleaned_image)
                fields["去手写"] = [{"file_token": file_token}]
        
        # 注意：根据PRD，不再保存"题目文本"字段到飞书表格
        # question_text 仅用于内部处理和AI分析
        
        # 学科（替代了原来的科目和年级）
        if record.subject:
            fields["学科"] = record.subject
        
        # 知识点
        if record.knowledge_points:
            fields["知识点"] = record.knowledge_points
        
        # 不会/做错（单选）
        if record.error_type:
            fields["不会/做错"] = record.error_type
        
        # 不会/做错的原因（文本）
        if record.error_reason:
            fields["不会/做错的原因"] = record.error_reason
        if record.guide_questions:
            fields["引导问题"] = record.guide_questions
        if record.thinking_process:
            fields["思考过程"] = record.thinking_process
        if record.solution_approach:
            fields["解题思路"] = record.solution_approach
        if record.solution_checklist:
            fields["解题清单"] = record.solution_checklist
        if record.memory_formula:
            fields["记忆口诀"] = record.memory_formula
        
        # 是否母题（单选：是/否）- 从bool改为单选
        if record.is_master_question:
            # 如果已经是字符串（是/否），直接使用
            if isinstance(record.is_master_question, str):
                fields["是否母题"] = record.is_master_question
            # 如果是bool类型，转换为字符串
            elif isinstance(record.is_master_question, bool):
                fields["是否母题"] = "是" if record.is_master_question else "否"
        
        # 掌握程度
        if record.mastery_level:
            fields["掌握程度"] = record.mastery_level
        
        # 日期时间
        if record.created_at:
            fields["创建时间"] = int(record.created_at.timestamp() * 1000)
        if record.last_review_time:
            fields["最后复习时间"] = int(record.last_review_time.timestamp() * 1000)
        
        # 复习次数（PRD中有，根据实际情况决定是否保存）
        if record.review_count is not None:
            fields["复习次数"] = record.review_count
        
        # 复习次数（PRD中有但可能不需要，根据实际情况决定）
        if hasattr(record, 'review_count') and record.review_count is not None:
            fields["复习次数"] = record.review_count
        
        # 发送请求
        headers = self._get_headers()
        data = {"fields": fields}
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"创建记录失败: {result.get('msg')}")
        
        return result["data"]["record"]["record_id"]
    
    def update_error_record(self, record_id: str, record: ErrorRecord) -> bool:
        """
        更新错题记录
        
        Args:
            record_id: 记录ID
            record: 更新的错题记录对象
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/bitable/v1/apps/{self.table_id}/tables/{self.table_token}/records/{record_id}"
        
        # 构建字段数据（只包含需要更新的字段）
        fields = {}
        
        # 类似create_error_record的逻辑，但只包含需要更新的字段
        # ...（省略具体实现，与create类似）
        
        headers = self._get_headers()
        data = {"fields": fields}
        
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"更新记录失败: {result.get('msg')}")
        
        return True
    
    def get_error_records(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        获取错题记录列表
        
        Args:
            limit: 每页数量
            offset: 偏移量
            
        Returns:
            记录列表
        """
        url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        params = {
            "page_size": limit,
            "page_token": str(offset) if offset > 0 else None
        }
        
        headers = self._get_headers()
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取记录失败: {result.get('msg')}")
        
        return result.get("data", {}).get("items", [])
    
    def create_feedback_question(self, question: FeedbackQuestion) -> str:
        """
        创建反馈题记录
        
        Args:
            question: 反馈题对象
            
        Returns:
            创建的记录ID
        """
        if not self.feedback_table_id:
            raise ValueError("反馈题表格ID未配置，请在config.py中设置FEISHU_FEEDBACK_TABLE_ID")
        
        url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.feedback_table_id}/records"
        
        # 构建字段数据
        fields = {}
        
        # 关联字段：母题ID（关联字段需要传入记录ID数组）
        if question.master_question_id:
            # 关联字段格式：["record_id1", "record_id2"]
            fields["母题ID"] = [question.master_question_id]
        
        # 文本字段
        if question.question_content:
            fields["题目内容"] = question.question_content
        if question.difficulty:
            fields["难度"] = question.difficulty
        if question.standard_answer:
            fields["答案"] = question.standard_answer
        if question.student_answer:
            fields["学生答案"] = question.student_answer
        if question.is_correct:
            fields["是否正确"] = question.is_correct
        
        # 日期时间
        if question.created_at:
            fields["创建时间"] = int(question.created_at.timestamp() * 1000)
        
        # 发送请求
        headers = self._get_headers()
        data = {"fields": fields}
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"创建反馈题记录失败: {result.get('msg')}")
        
        return result["data"]["record"]["record_id"]

