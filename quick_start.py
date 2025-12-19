"""
快速开始脚本
交互式引导用户完成首次配置和测试
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))


def check_config():
    """检查配置文件是否存在"""
    config_file = Path("config.py")
    if not config_file.exists():
        print("[ERROR] 配置文件 config.py 不存在")
        print("\n请先创建配置文件：")
        print("  1. 复制 config.example.py 为 config.py")
        print("  2. 编辑 config.py，填入你的API密钥")
        return False
    return True


def check_dependencies():
    """检查依赖是否安装"""
    print("检查Python依赖...")
    missing = []
    
    # 检查各个依赖
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import pydantic
    except ImportError:
        missing.append("pydantic")
    
    if missing:
        print(f"[ERROR] 缺少以下依赖: {', '.join(missing)}")
        print("\n请运行: pip install " + " ".join(missing))
        return False
    else:
        print("[OK] 依赖检查通过")
        return True


def interactive_config():
    """交互式配置引导"""
    print("\n" + "="*50)
    print("配置向导")
    print("="*50)
    
    config_file = Path("config.py")
    if config_file.exists():
        print("\n[WARNING] config.py 已存在")
        choice = input("是否重新配置？(y/n): ").strip().lower()
        if choice != 'y':
            return
    
    # 读取示例配置
    example_file = Path("config.example.py")
    if not example_file.exists():
        print("[ERROR] config.example.py 不存在")
        return
    
    print("\n请依次输入以下配置信息（直接回车跳过）：")
    
    config_values = {}
    
    # 飞书配置
    print("\n【飞书配置】")
    config_values['FEISHU_APP_ID'] = input("飞书 App ID: ").strip()
    config_values['FEISHU_APP_SECRET'] = input("飞书 App Secret: ").strip()
    config_values['FEISHU_TABLE_ID'] = input("飞书表格 base_id: ").strip()
    config_values['FEISHU_TABLE_TOKEN'] = input("飞书表格 token (tbl...): ").strip()
    
    # API配置
    print("\n【API配置】")
    config_values['DOUBAO_API_KEY'] = input("豆包 API Key: ").strip()
    config_values['DEEPSEEK_API_KEY'] = input("DeepSeek API Key (可选): ").strip()
    
    # 读取示例文件
    with open(example_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换配置值
    for key, value in config_values.items():
        if value:
            # 替换配置值
            import re
            pattern = rf'{key}\s*=\s*"[^"]*"'
            replacement = f'{key} = "{value}"'
            content = re.sub(pattern, replacement, content)
    
    # 保存配置文件
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[OK] 配置已保存到 {config_file}")
    print("\n提示：你可以随时手动编辑 config.py 来修改配置")


def show_next_steps():
    """显示下一步操作"""
    print("\n" + "="*50)
    print("下一步操作")
    print("="*50)
    print("\n1. 运行基础功能测试：")
    print("   python test_basic.py")
    print("\n2. 处理第一张错题：")
    print("   python main.py path/to/question.jpg 不会")
    print("\n3. 查看详细文档：")
    print("   - NEXT_STEPS.md - 详细配置指南")
    print("   - USAGE.md - 使用说明")
    print("   - PRD.md - 产品需求文档")


def main():
    """主函数"""
    print("="*50)
    print("错题思维应用 - 快速开始")
    print("="*50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查配置
    if not check_config():
        print("\n开始配置向导...")
        try:
            interactive_config()
        except EOFError:
            print("\n[INFO] 非交互式环境，跳过配置向导")
            print("请手动编辑 config.py 文件，填入你的API密钥")
    else:
        print("[OK] 配置文件已存在")
        try:
            choice = input("\n是否运行配置向导？(y/n): ").strip().lower()
            if choice == 'y':
                interactive_config()
        except EOFError:
            print("\n[INFO] 非交互式环境，跳过配置向导")
            print("如需修改配置，请手动编辑 config.py 文件")
    
    # 显示下一步
    show_next_steps()


if __name__ == "__main__":
    main()

