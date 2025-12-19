"""
使用示例
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    import config
except ImportError:
    print("错误：请先复制 config.example.py 为 config.py 并配置相关参数")
    sys.exit(1)

from main import ErrorQuestionApp


def example_basic_usage():
    """基础使用示例"""
    print("=" * 50)
    print("基础使用示例")
    print("=" * 50)
    
    app = ErrorQuestionApp()
    
    # 假设有一张错题图片
    image_path = "uploads/example_question.jpg"
    
    # 检查文件是否存在
    if not Path(image_path).exists():
        print(f"示例图片不存在: {image_path}")
        print("请先准备一张错题图片")
        return
    
    try:
        # 1. 处理错题
        print("\n1. 处理错题...")
        record_id = app.process_error_question(image_path, "不会做")
        print(f"✅ 记录ID: {record_id}")
        
        # 2. 生成引导问题
        print("\n2. 生成引导问题...")
        result = app.start_guide_learning(record_id)
        print(f"✅ 生成了 {len(result['questions'])} 个引导问题")
        for i, q in enumerate(result['questions'], 1):
            print(f"   {i}. {q}")
        
        # 3. 生成反馈题
        print("\n3. 生成反馈题...")
        questions = app.generate_practice_questions(record_id, count=3)
        print(f"✅ 生成了 {len(questions)} 道反馈题")
        for i, q in enumerate(questions, 1):
            print(f"\n   题目{i} ({q.get('difficulty', '未知')}):")
            print(f"   {q.get('question', '')}")
            print(f"   答案: {q.get('answer', '')}")
            print(f"   解析: {q.get('explanation', '')}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def example_interactive_guide():
    """交互式引导学习示例"""
    print("=" * 50)
    print("交互式引导学习示例")
    print("=" * 50)
    
    app = ErrorQuestionApp()
    
    # 假设已有记录ID
    record_id = input("请输入记录ID: ").strip()
    
    if not record_id:
        print("记录ID不能为空")
        return
    
    try:
        # 获取错题信息
        records = app.feishu_client.get_error_records()
        record = next((r for r in records if r.get("record_id") == record_id), None)
        
        if not record:
            print(f"未找到记录: {record_id}")
            return
        
        fields = record.get("fields", {})
        question_text = fields.get("题目文本", "")
        
        print(f"\n题目: {question_text}\n")
        
        # 生成引导问题
        guide_questions = app.guide.generate_guide_questions(
            question_text,
            fields.get("科目", ""),
            fields.get("不会/做错", "")
        )
        
        # 开始对话
        conversation_history = []
        for i, question in enumerate(guide_questions):
            print(f"\n问题 {i+1}: {question}")
            answer = input("你的回答: ").strip()
            
            if not answer:
                continue
            
            conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            # 继续对话
            if i < len(guide_questions) - 1:
                response = app.guide.continue_dialogue(
                    question_text,
                    question,
                    answer,
                    conversation_history
                )
                
                if response["type"] == "summary":
                    print(f"\n总结: {response['content']}")
                    break
        
        # 生成解题清单
        print("\n正在生成解题清单...")
        solution_approach = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" 
                                      for h in conversation_history])
        
        checklist_result = app.guide.generate_solution_checklist(
            question_text,
            solution_approach,
            fields.get("科目", "")
        )
        
        print("\n解题清单:")
        for i, step in enumerate(checklist_result.get("checklist", []), 1):
            print(f"  {i}. {step}")
        
        if checklist_result.get("formula"):
            print(f"\n记忆口诀: {checklist_result['formula']}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def example_batch_process():
    """批量处理示例"""
    print("=" * 50)
    print("批量处理示例")
    print("=" * 50)
    
    app = ErrorQuestionApp()
    
    # 获取所有图片文件
    image_dir = Path("uploads")
    image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
    
    if not image_files:
        print("未找到图片文件")
        return
    
    print(f"找到 {len(image_files)} 张图片")
    
    results = []
    for image_file in image_files:
        print(f"\n处理: {image_file.name}")
        try:
            record_id = app.process_error_question(str(image_file), "不会做")
            results.append({
                "file": image_file.name,
                "record_id": record_id,
                "status": "success"
            })
            print(f"✅ 成功: {record_id}")
        except Exception as e:
            results.append({
                "file": image_file.name,
                "record_id": None,
                "status": "error",
                "error": str(e)
            })
            print(f"❌ 失败: {e}")
    
    # 输出汇总
    print("\n" + "=" * 50)
    print("处理汇总")
    print("=" * 50)
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"成功: {success_count}/{len(results)}")
    print(f"失败: {len(results) - success_count}/{len(results)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "basic":
            example_basic_usage()
        elif mode == "interactive":
            example_interactive_guide()
        elif mode == "batch":
            example_batch_process()
        else:
            print("未知模式，使用: basic, interactive, batch")
    else:
        print("使用示例:")
        print("  python example.py basic        # 基础使用")
        print("  python example.py interactive  # 交互式引导")
        print("  python example.py batch        # 批量处理")

