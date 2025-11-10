#!/usr/bin/env python3
"""
简单的验证脚本，测试Matplotlib中文显示功能
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试基础模块导入
        from utils import (
            setup_chinese_font,
            get_font_config_info,
            list_available_chinese_fonts,
            complete_chinese_font_setup,
            quick_fix_chinese_display,
            diagnose_chinese_display
        )
        print("✓ 基础模块导入成功")
        
        # 测试扩展模块导入
        try:
            from utils import FontInstaller, MatplotlibCacheCleaner
            print("✓ 扩展模块导入成功")
        except ImportError as e:
            print(f"⚠ 扩展模块导入失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基础功能"""
    print("\n🔧 测试基础功能...")
    
    try:
        from utils import list_available_chinese_fonts, get_font_config_info
        
        # 测试字体列表
        fonts = list_available_chinese_fonts()
        print(f"✓ 字体列表获取成功，找到 {len(fonts)} 个中文字体")
        
        # 测试配置信息
        config = get_font_config_info()
        print("✓ 配置信息获取成功")
        print(f"  当前字体: {config.get('current_font', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"✗ 基础功能测试失败: {e}")
        return False

def test_font_setup():
    """测试字体设置"""
    print("\n🎨 测试字体设置...")
    
    try:
        from utils import setup_chinese_font
        
        # 测试基础设置
        font_name = setup_chinese_font()
        print(f"✓ 基础字体设置成功，使用字体: {font_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ 字体设置测试失败: {e}")
        return False

def test_matplotlib_rendering():
    """测试matplotlib渲染"""
    print("\n📊 测试matplotlib渲染...")
    
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # 创建简单图表
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # 测试中文文本
        ax.text(0.5, 0.5, "中文测试", fontsize=16, ha='center', va='center')
        ax.set_title("中文标题")
        ax.set_xlabel("X轴")
        ax.set_ylabel("Y轴")
        
        # 保存到临时文件
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "verification_test.png"
        
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✓ matplotlib渲染测试成功，图片保存至: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ matplotlib渲染测试失败: {e}")
        return False

def main():
    """主函数"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 20 + "Matplotlib中文显示验证" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ("模块导入", test_imports),
        ("基础功能", test_basic_functionality),
        ("字体设置", test_font_setup),
        ("matplotlib渲染", test_matplotlib_rendering),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name}测试出现异常: {e}")
            results.append((test_name, False))
    
    # 输出总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Matplotlib中文显示功能正常。")
        return 0
    elif passed >= total * 0.75:
        print("⚠ 大部分测试通过，但仍有问题需要解决。")
        return 1
    else:
        print("❌ 多项测试失败，需要进一步检查配置。")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)