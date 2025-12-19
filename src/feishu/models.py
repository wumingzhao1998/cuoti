"""
飞书多维表格数据模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ErrorRecord(BaseModel):
    """错题记录模型"""
    
    # 基础信息
    original_image: Optional[str] = Field(None, description="错题原图URL或路径")
    cleaned_image: Optional[str] = Field(None, description="去手写后的图片URL或路径")
    question_text: Optional[str] = Field(None, description="题目文本")
    
    # 分类信息
    subject: Optional[str] = Field(None, description="学科：数学/语文/英语")
    knowledge_points: Optional[List[str]] = Field(None, description="知识点列表")
    error_type: Optional[str] = Field(None, description="不会/做错：不会/做错（单选）")
    error_reason: Optional[str] = Field(None, description="不会/做错的原因（文本）")
    
    # 学习引导
    guide_questions: Optional[str] = Field(None, description="引导问题（多行文本）")
    thinking_process: Optional[str] = Field(None, description="思考过程（多行文本）")
    solution_approach: Optional[str] = Field(None, description="解题思路（多行文本）")
    solution_checklist: Optional[str] = Field(None, description="解题清单（文本）")
    memory_formula: Optional[str] = Field(None, description="记忆口诀（文本）")
    
    # 状态信息
    is_master_question: Optional[str] = Field(None, description="是否母题：是/否（单选）")
    mastery_level: Optional[str] = Field(None, description="掌握程度：未掌握/掌握中/已掌握")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    last_review_time: Optional[datetime] = Field(None, description="最后复习时间")
    review_count: Optional[int] = Field(None, description="复习次数统计（可选）")
    
    # 飞书记录ID（用于更新）
    record_id: Optional[str] = Field(None, description="飞书记录ID")


class FeedbackQuestion(BaseModel):
    """反馈题模型"""
    
    master_question_id: str = Field(..., description="母题ID（关联字段）")
    question_content: str = Field(..., description="题目内容")
    difficulty: str = Field(..., description="难度：基础/进阶/挑战")
    standard_answer: str = Field(..., description="标准答案")
    student_answer: Optional[str] = Field(None, description="学生答案")
    is_correct: Optional[str] = Field(None, description="是否正确：正确/错误（单选）")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    
    # 飞书记录ID
    record_id: Optional[str] = Field(None, description="飞书记录ID")

