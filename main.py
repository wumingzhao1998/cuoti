"""
错题思维应用主程序
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    import config
except ImportError:
    print("错误：请先复制 config.example.py 为 config.py 并配置相关参数")
    sys.exit(1)

from src.feishu import FeishuClient
from src.feishu.models import ErrorRecord
from src.ocr import DoubaoOCR
from src.handwriting import HandwritingRemover
from src.ai import SocraticGuide, QuestionGenerator
from src.utils import validate_image, create_upload_dir, setup_logger


class ErrorQuestionApp:
    """错题应用主类"""
    
    def __init__(self, enable_logging: bool = True):
        """
        初始化应用
        
        Args:
            enable_logging: 是否启用日志
        """
        # 设置日志
        if enable_logging:
            self.logger = setup_logger()
        else:
            import logging
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.WARNING)
        # 初始化飞书客户端
        app_token = getattr(config, 'FEISHU_APP_TOKEN', None) or getattr(config, 'FEISHU_TABLE_ID', None)  # 兼容旧配置
        table_id = getattr(config, 'FEISHU_TABLE_ID', None) or getattr(config, 'FEISHU_TABLE_TOKEN', None)  # 兼容旧配置
        feedback_table_id = getattr(config, 'FEISHU_FEEDBACK_TABLE_ID', None) or getattr(config, 'FEISHU_FEEDBACK_TABLE_TOKEN', None)  # 兼容旧配置
        
        self.feishu_client = FeishuClient(
            app_id=config.FEISHU_APP_ID,
            app_secret=config.FEISHU_APP_SECRET,
            app_token=app_token,
            table_id=table_id,
            feedback_table_id=feedback_table_id
        )
        
        # 初始化OCR
        self.ocr = DoubaoOCR(api_key=config.DOUBAO_API_KEY)
        
        # 初始化去手写
        self.handwriting_remover = HandwritingRemover()
        
        # 初始化AI引导（使用DeepSeek，根据PRD推荐）
        deepseek_key = getattr(config, 'DEEPSEEK_API_KEY', config.DOUBAO_API_KEY)
        deepseek_url = getattr(config, 'DEEPSEEK_API_URL', None)
        use_deepseek = hasattr(config, 'DEEPSEEK_API_KEY')
        self.guide = SocraticGuide(
            api_key=deepseek_key,
            api_url=deepseek_url,
            use_deepseek=use_deepseek
        )
        
        # 初始化题目生成器（使用DeepSeek）
        self.generator = QuestionGenerator(
            api_key=deepseek_key,
            api_url=deepseek_url,
            use_deepseek=use_deepseek
        )
        
        # 创建上传目录
        self.upload_dir = create_upload_dir()
    
    def process_error_question(self, image_path: str, error_type: str = "不会") -> str:
        """
        处理错题的完整流程
        
        Args:
            image_path: 错题图片路径
            error_type: 错误类型（不会做/做错了）
            
        Returns:
            创建的记录ID
        """
        self.logger.info(f"开始处理错题: {image_path}")
        print(f"开始处理错题: {image_path}")
        
        # 1. 验证图片
        is_valid, error_msg = validate_image(image_path)
        if not is_valid:
            error = f"图片验证失败: {error_msg}"
            self.logger.error(error)
            raise ValueError(error)
        
        # 2. 识别题目
        print("正在识别题目...")
        self.logger.info("开始识别题目")
        try:
            recognize_result = self.ocr.recognize_question(image_path)
            if not recognize_result["success"]:
                error = f"识别失败: {recognize_result.get('error')}"
                self.logger.error(error)
                raise Exception(error)
            
            question_text = recognize_result["question_text"]
            print(f"识别结果: {question_text[:50]}...")
            self.logger.info(f"识别成功，题目长度: {len(question_text)}")
        except Exception as e:
            self.logger.error(f"识别过程出错: {e}", exc_info=True)
            raise
        
        # 3. 分析题目
        print("正在分析题目...")
        self.logger.info("开始分析题目")
        try:
            analysis_result = self.ocr.analyze_question(image_path, question_text)
            if not analysis_result["success"]:
                print(f"分析失败: {analysis_result.get('error')}")
                self.logger.warning(f"题目分析失败: {analysis_result.get('error')}")
                analysis = {}
            else:
                analysis = analysis_result["analysis"]
                self.logger.info(f"分析成功: 科目={analysis.get('subject')}, 年级={analysis.get('grade')}")
        except Exception as e:
            self.logger.warning(f"分析过程出错: {e}")
            analysis = {}
        
        # 4. 去手写处理
        print("正在去除手写...")
        self.logger.info("开始去手写处理")
        try:
            cleaned_image_path = self.handwriting_remover.remove_handwriting(
                image_path,
                output_path=os.path.join(self.upload_dir, f"cleaned_{Path(image_path).name}")
            )
            print(f"去手写完成: {cleaned_image_path}")
            self.logger.info(f"去手写完成: {cleaned_image_path}")
        except Exception as e:
            self.logger.error(f"去手写处理失败: {e}", exc_info=True)
            # 去手写失败不影响主流程，继续执行
            cleaned_image_path = image_path
        
        # 5. 创建错题记录
        # 注意：question_text 不保存到飞书表格，仅用于内部处理
        # 根据PRD，学科字段替代了原来的科目和年级
        subject = analysis.get("subject", "")
        # 如果分析结果中有年级信息，可以合并到学科中，或单独处理
        # 这里暂时只使用subject
        
        record = ErrorRecord(
            original_image=image_path,
            cleaned_image=cleaned_image_path,
            question_text=question_text,  # 内部使用，不保存到飞书
            subject=subject,  # 学科：数学/语文/英语
            knowledge_points=analysis.get("knowledge_points", []),
            error_type=error_type,  # 应该是"不会"或"做错"
            error_reason=None,  # 可以后续补充
            is_master_question="是",  # 默认标记为母题（单选：是/否）
            mastery_level="未掌握",
            created_at=datetime.now()
        )
        
        # 6. 保存到飞书
        print("正在保存到飞书多维表格...")
        self.logger.info("开始保存到飞书")
        try:
            record_id = self.feishu_client.create_error_record(record)
            print(f"保存成功，记录ID: {record_id}")
            self.logger.info(f"保存成功，记录ID: {record_id}")
            return record_id
        except Exception as e:
            error = f"保存到飞书失败: {e}"
            self.logger.error(error, exc_info=True)
            raise Exception(error)
    
    def start_guide_learning(self, record_id: str, question_text: Optional[str] = None) -> dict:
        """
        开始引导学习
        
        Args:
            record_id: 记录ID
            question_text: 题目文本（可选，如果不提供则从飞书记录中获取或重新识别）
            
        Returns:
            引导结果
        """
        # 获取错题记录
        records = self.feishu_client.get_error_records()
        record = next((r for r in records if r.get("record_id") == record_id), None)
        
        if not record:
            raise ValueError(f"未找到记录: {record_id}")
        
        fields = record.get("fields", {})
        
        # 获取题目文本：优先使用传入的参数，否则尝试从引导问题字段获取，最后重新识别
        if not question_text:
            # 尝试从引导问题字段的开头获取（如果之前保存过）
            guide_questions = fields.get("引导问题", "")
            if guide_questions and "题目：" in guide_questions:
                # 简单提取，实际可能需要更复杂的解析
                question_text = ""
            else:
                # 如果都没有，需要重新识别图片
                # 这里需要从错题原题附件中获取图片并重新识别
                # 暂时提示用户需要提供题目文本
                raise ValueError("需要提供题目文本，或从错题原图重新识别")
        
        subject = fields.get("学科", "")  # 更新为"学科"
        error_type = fields.get("不会/做错", "")
        
        # 生成引导问题
        print("正在生成引导问题...")
        guide_questions = self.guide.generate_guide_questions(
            question_text, subject, error_type
        )
        
        print(f"生成了{len(guide_questions)}个引导问题")
        for i, q in enumerate(guide_questions, 1):
            print(f"{i}. {q}")
        
        return {
            "questions": guide_questions,
            "record_id": record_id
        }
    
    def generate_practice_questions(self, record_id: str, count: int = 5, 
                                   question_text: Optional[str] = None) -> list:
        """
        生成反馈题
        
        Args:
            record_id: 母题记录ID
            count: 生成题目数量
            question_text: 题目文本（可选，如果不提供则需要从其他地方获取）
            
        Returns:
            反馈题列表
        """
        # 获取错题记录
        records = self.feishu_client.get_error_records()
        record = next((r for r in records if r.get("record_id") == record_id), None)
        
        if not record:
            raise ValueError(f"未找到记录: {record_id}")
        
        fields = record.get("fields", {})
        
        # 获取题目文本：优先使用传入的参数，否则需要重新识别
        if not question_text:
            # 需要从错题原图重新识别，或提示用户提供
            raise ValueError("需要提供题目文本，或从错题原图重新识别")
        
        subject = fields.get("学科", "")  # 更新为"学科"
        knowledge_points = fields.get("知识点", [])
        error_type = fields.get("不会/做错", "")
        
        # 生成反馈题
        print(f"正在生成{count}道反馈题...")
        questions = self.generator.generate_feedback_questions(
            question_text, subject, knowledge_points, error_type, count
        )
        
        print(f"生成了{len(questions)}道反馈题")
        
        # 保存反馈题到飞书表格
        saved_question_ids = []
        for i, q in enumerate(questions, 1):
            print(f"\n题目{i} ({q.get('difficulty', '未知难度')}):")
            print(f"  {q.get('question', '')}")
            print(f"  答案: {q.get('answer', '')}")
            
            # 创建反馈题记录并保存到飞书
            try:
                from src.feishu.models import FeedbackQuestion
                from datetime import datetime
                
                feedback_record = FeedbackQuestion(
                    master_question_id=record_id,
                    question_content=q.get('question', ''),
                    difficulty=q.get('difficulty', '基础'),
                    standard_answer=q.get('answer', ''),
                    student_answer=None,
                    is_correct=None,
                    created_at=datetime.now()
                )
                
                feedback_id = self.feishu_client.create_feedback_question(feedback_record)
                saved_question_ids.append(feedback_id)
                print(f"  [已保存到飞书，记录ID: {feedback_id}]")
            except Exception as e:
                print(f"  [保存失败: {e}]")
                self.logger.warning(f"保存反馈题失败: {e}")
        
        if saved_question_ids:
            print(f"\n✅ 成功保存 {len(saved_question_ids)} 道反馈题到飞书表格")
        
        return questions


def main():
    """主函数"""
    print("=" * 50)
    print("错题思维应用")
    print("=" * 50)
    
    app = ErrorQuestionApp()
    
    # 示例：处理错题
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        error_type = sys.argv[2] if len(sys.argv) > 2 else "不会"
        
        try:
            record_id = app.process_error_question(image_path, error_type)
            print(f"\n✅ 错题处理完成！记录ID: {record_id}")
            
            # 询问是否开始引导学习
            choice = input("\n是否开始引导学习？(y/n): ")
            if choice.lower() == 'y':
                result = app.start_guide_learning(record_id)
                print("\n✅ 引导问题已生成")
            
            # 询问是否生成反馈题
            choice = input("\n是否生成反馈题？(y/n): ")
            if choice.lower() == 'y':
                questions = app.generate_practice_questions(record_id)
                print("\n✅ 反馈题已生成")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
    else:
        print("\n使用方法:")
        print("  python main.py <图片路径> [错误类型]")
        print("\n错误类型:")
        print("  - 不会")
        print("  - 做错")
        print("\n示例:")
        print("  python main.py uploads/question.jpg 不会")


if __name__ == "__main__":
    main()

