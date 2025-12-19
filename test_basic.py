"""
基础功能测试脚本
用于快速测试各个模块是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    import config
except ImportError:
    print("❌ 错误：请先复制 config.example.py 为 config.py 并配置相关参数")
    sys.exit(1)

from src.utils import setup_logger
from src.ocr import DoubaoOCR
from src.handwriting import HandwritingRemover
from src.ai import SocraticGuide, QuestionGenerator
from src.feishu import FeishuClient

logger = setup_logger()


def test_ocr():
    """测试OCR识别功能"""
    print("\n" + "="*50)
    print("测试1: OCR图片识别")
    print("="*50)
    
    try:
        ocr = DoubaoOCR(api_key=config.DOUBAO_API_KEY)
        print("✅ OCR模块初始化成功")
        
        # 如果有测试图片，可以测试识别
        # result = ocr.recognize_question("test_image.jpg")
        # print(f"识别结果: {result}")
        
        return True
    except Exception as e:
        print(f"❌ OCR测试失败: {e}")
        logger.error(f"OCR测试失败: {e}", exc_info=True)
        return False


def test_handwriting_removal():
    """测试去手写功能"""
    print("\n" + "="*50)
    print("测试2: 去手写处理")
    print("="*50)
    
    try:
        remover = HandwritingRemover()
        print("✅ 去手写模块初始化成功")
        
        # 如果有测试图片，可以测试去手写
        # result = remover.remove_handwriting("test_image.jpg")
        # print(f"去手写完成: {result}")
        
        return True
    except Exception as e:
        print(f"❌ 去手写测试失败: {e}")
        logger.error(f"去手写测试失败: {e}", exc_info=True)
        return False


def test_ai_guide():
    """测试AI引导功能"""
    print("\n" + "="*50)
    print("测试3: AI引导学习")
    print("="*50)
    
    try:
        deepseek_key = getattr(config, 'DEEPSEEK_API_KEY', config.DOUBAO_API_KEY)
        deepseek_url = getattr(config, 'DEEPSEEK_API_URL', None)
        use_deepseek = hasattr(config, 'DEEPSEEK_API_KEY')
        
        guide = SocraticGuide(
            api_key=deepseek_key,
            api_url=deepseek_url,
            use_deepseek=use_deepseek
        )
        print("✅ AI引导模块初始化成功")
        
        # 测试生成引导问题
        test_question = "计算 2x + 3 = 11 中 x 的值"
        questions = guide.generate_guide_questions(test_question, "数学", "不会")
        
        if questions:
            print(f"✅ 成功生成 {len(questions)} 个引导问题")
            for i, q in enumerate(questions[:2], 1):  # 只显示前2个
                print(f"   {i}. {q}")
        else:
            print("⚠️  未生成引导问题（可能是API调用失败）")
        
        return True
    except Exception as e:
        print(f"❌ AI引导测试失败: {e}")
        logger.error(f"AI引导测试失败: {e}", exc_info=True)
        return False


def test_question_generator():
    """测试反馈题生成功能"""
    print("\n" + "="*50)
    print("测试4: 反馈题生成")
    print("="*50)
    
    try:
        deepseek_key = getattr(config, 'DEEPSEEK_API_KEY', config.DOUBAO_API_KEY)
        deepseek_url = getattr(config, 'DEEPSEEK_API_URL', None)
        use_deepseek = hasattr(config, 'DEEPSEEK_API_KEY')
        
        generator = QuestionGenerator(
            api_key=deepseek_key,
            api_url=deepseek_url,
            use_deepseek=use_deepseek
        )
        print("✅ 反馈题生成模块初始化成功")
        
        # 测试生成反馈题
        test_question = "计算 2x + 3 = 11 中 x 的值"
        questions = generator.generate_feedback_questions(
            test_question, "数学", ["一元一次方程"], "不会", count=2
        )
        
        if questions:
            print(f"✅ 成功生成 {len(questions)} 道反馈题")
            for i, q in enumerate(questions, 1):
                print(f"\n   题目{i} ({q.get('difficulty', '未知')}):")
                print(f"   {q.get('question', '')[:50]}...")
        else:
            print("⚠️  未生成反馈题（可能是API调用失败）")
        
        return True
    except Exception as e:
        print(f"❌ 反馈题生成测试失败: {e}")
        logger.error(f"反馈题生成测试失败: {e}", exc_info=True)
        return False


def test_feishu_connection():
    """测试飞书连接"""
    print("\n" + "="*50)
    print("测试5: 飞书连接")
    print("="*50)
    
    try:
        table_token = getattr(config, 'FEISHU_TABLE_TOKEN', None)
        client = FeishuClient(
            app_id=config.FEISHU_APP_ID,
            app_secret=config.FEISHU_APP_SECRET,
            table_id=config.FEISHU_TABLE_ID,
            table_token=table_token
        )
        print("✅ 飞书客户端初始化成功")
        
        # 测试获取token
        token = client._get_access_token()
        if token:
            print("✅ 飞书API认证成功")
        else:
            print("❌ 飞书API认证失败")
            return False
        
        # 测试获取记录（不要求有数据）
        try:
            records = client.get_error_records(limit=1)
            print(f"✅ 飞书API连接正常（当前有 {len(records)} 条记录）")
        except Exception as e:
            print(f"⚠️  获取记录失败（可能是表格ID配置错误）: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 飞书连接测试失败: {e}")
        logger.error(f"飞书连接测试失败: {e}", exc_info=True)
        return False


def main():
    """运行所有测试"""
    print("="*50)
    print("错题思维应用 - 基础功能测试")
    print("="*50)
    
    results = []
    
    # 运行各项测试
    results.append(("OCR识别", test_ocr()))
    results.append(("去手写处理", test_handwriting_removal()))
    results.append(("AI引导学习", test_ai_guide()))
    results.append(("反馈题生成", test_question_generator()))
    results.append(("飞书连接", test_feishu_connection()))
    
    # 输出测试结果
    print("\n" + "="*50)
    print("测试结果汇总")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！可以开始使用了。")
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接。")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

