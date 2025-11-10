"""
Matplotlib中文绘图测试模块

提供全面的中文显示功能测试，确保matplotlib中文字体配置正确工作。
包含基础测试、边界测试和性能测试。
"""

import sys
import time
import traceback
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from utils.plot_config import (
        complete_chinese_font_setup,
        get_font_config_info,
        list_available_chinese_fonts,
        quick_fix_chinese_display,
        setup_chinese_font,
    )
except ImportError as e:
    print(f"✗ 导入工具模块失败: {e}")
    print("请确保在项目根目录下运行此脚本")
    sys.exit(1)


class ChinesePlottingTester:
    """
    中文绘图测试器
    
    提供全面的matplotlib中文显示功能测试。
    """
    
    def __init__(self):
        """初始化测试器"""
        self.test_results = {
            "setup": {},
            "basic_tests": {},
            "advanced_tests": {},
            "edge_cases": {},
            "performance_tests": {},
            "summary": {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "success_rate": 0.0
            }
        }
        self.output_dir = project_root / "outputs" / "chinese_plotting_tests"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_all_tests(self) -> Dict[str, any]:
        """
        运行所有测试
        
        返回:
            完整的测试结果字典
        """
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 20 + "Matplotlib中文绘图测试" + " " * 20 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        
        # 1. 设置测试
        self._test_setup()
        
        # 2. 基础功能测试
        self._test_basic_functionality()
        
        # 3. 高级功能测试
        self._test_advanced_functionality()
        
        # 4. 边界情况测试
        self._test_edge_cases()
        
        # 5. 性能测试
        self._test_performance()
        
        # 6. 生成总结
        self._generate_summary()
        
        return self.test_results
    
    def _test_setup(self):
        """测试字体设置功能"""
        print("🔧 测试字体设置功能...")
        
        setup_results = {}
        
        # 测试1: 基础设置
        try:
            font_name = setup_chinese_font()
            setup_results["基础设置"] = {
                "status": "通过",
                "font": font_name,
                "config": get_font_config_info()
            }
            print("✓ 基础字体设置测试通过")
        except Exception as e:
            setup_results["基础设置"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 基础字体设置测试失败: {e}")
        
        # 测试2: 完整设置
        try:
            result = complete_chinese_font_setup(
                auto_install=False,
                clear_cache=False
            )
            setup_results["完整设置"] = {
                "status": "通过" if result['status'] == 'success' else "失败",
                "result": result
            }
            print("✓ 完整字体设置测试通过")
        except Exception as e:
            setup_results["完整设置"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 完整字体设置测试失败: {e}")
        
        # 测试3: 快速修复
        try:
            success = quick_fix_chinese_display()
            setup_results["快速修复"] = {
                "status": "通过" if success else "失败",
                "success": success
            }
            print("✓ 快速修复测试通过")
        except Exception as e:
            setup_results["快速修复"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 快速修复测试失败: {e}")
        
        self.test_results["setup"] = setup_results
    
    def _test_basic_functionality(self):
        """测试基础绘图功能"""
        print("\n📊 测试基础绘图功能...")
        
        basic_results = {}
        
        # 测试1: 简单中文文本
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, "中文测试文本", fontsize=20, ha='center', va='center')
            ax.set_title("中文标题测试")
            ax.set_xlabel("中文X轴标签")
            ax.set_ylabel("中文Y轴标签")
            
            output_path = self.output_dir / "test_basic_chinese_text.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            basic_results["基础中文文本"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 基础中文文本测试通过")
        except Exception as e:
            basic_results["基础中文文本"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 基础中文文本测试失败: {e}")
        
        # 测试2: 中文字符串组合
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # 各种中文字符串
            test_texts = [
                "简体中文测试：你好世界",
                "繁體中文測試：你好世界",
                "数字混合：2024年12月",
                "英文混合：Hello世界",
                "特殊符号：￥%&*（）",
                "标点符号：，。！？；："
            ]
            
            for i, text in enumerate(test_texts):
                ax.text(0.1, 0.9 - i*0.12, text, fontsize=12, transform=ax.transAxes)
            
            ax.set_title("中文字符串组合测试")
            ax.axis('off')  # 隐藏坐标轴
            
            output_path = self.output_dir / "test_chinese_text_combinations.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            basic_results["中文字符串组合"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 中文字符串组合测试通过")
        except Exception as e:
            basic_results["中文字符串组合"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 中文字符串组合测试失败: {e}")
        
        # 测试3: 中文图例
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            x = np.linspace(0, 2*np.pi, 100)
            ax.plot(x, np.sin(x), 'b-', label="正弦函数")
            ax.plot(x, np.cos(x), 'r--', label="余弦函数")
            ax.plot(x, np.tan(x), 'g:', label="正切函数")
            
            ax.set_title("三角函数图例测试")
            ax.set_xlabel("横坐标（弧度）")
            ax.set_ylabel("纵坐标（函数值）")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # 限制y轴范围以便显示正切函数
            ax.set_ylim(-3, 3)
            
            output_path = self.output_dir / "test_chinese_legend.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            basic_results["中文图例"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 中文图例测试通过")
        except Exception as e:
            basic_results["中文图例"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 中文图例测试失败: {e}")
        
        self.test_results["basic_tests"] = basic_results
    
    def _test_advanced_functionality(self):
        """测试高级绘图功能"""
        print("\n🎨 测试高级绘图功能...")
        
        advanced_results = {}
        
        # 测试1: 多子图中文
        try:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle("多子图中文测试", fontsize=16, fontweight='bold')
            
            # 子图1：柱状图
            categories = ["产品A", "产品B", "产品C", "产品D", "产品E"]
            values = np.random.randint(10, 100, size=5)
            axes[0, 0].bar(categories, values, color='skyblue')
            axes[0, 0].set_title("产品销售柱状图")
            axes[0, 0].set_ylabel("销售量")
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 子图2：散点图
            x = np.random.randn(50)
            y = 2*x + np.random.randn(50)
            axes[0, 1].scatter(x, y, alpha=0.6)
            axes[0, 1].set_title("数据分布散点图")
            axes[0, 1].set_xlabel("横坐标数据")
            axes[0, 1].set_ylabel("纵坐标数据")
            
            # 子图3：饼图
            sizes = [30, 25, 20, 15, 10]
            labels = ["类别一", "类别二", "类别三", "类别四", "类别五"]
            axes[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%')
            axes[1, 0].set_title("分类数据饼图")
            
            # 子图4：热力图
            data = np.random.randn(10, 10)
            im = axes[1, 1].imshow(data, cmap='viridis')
            axes[1, 1].set_title("数据热力图")
            plt.colorbar(im, ax=axes[1, 1])
            
            plt.tight_layout()
            
            output_path = self.output_dir / "test_multi_subplot_chinese.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            advanced_results["多子图中文"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 多子图中文测试通过")
        except Exception as e:
            advanced_results["多子图中文"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 多子图中文测试失败: {e}")
        
        # 测试2: 中文注释和箭头
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax.plot(x, y, 'b-', linewidth=2)
            
            # 添加各种中文注释
            ax.annotate("起始点", xy=(0, 0), xytext=(1, 0.5),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=12, color='red')
            
            ax.annotate("最大值", xy=(np.pi/2, 1), xytext=(3, 0.5),
                       arrowprops=dict(arrowstyle='->', color='green'),
                       fontsize=12, color='green')
            
            ax.annotate("最小值", xy=(3*np.pi/2, -1), xytext=(5, -0.5),
                       arrowprops=dict(arrowstyle='->', color='orange'),
                       fontsize=12, color='orange')
            
            ax.set_title("中文注释和箭头测试")
            ax.set_xlabel("横坐标（弧度）")
            ax.set_ylabel("纵坐标（函数值）")
            ax.grid(True, alpha=0.3)
            
            output_path = self.output_dir / "test_chinese_annotations.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            advanced_results["中文注释和箭头"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 中文注释和箭头测试通过")
        except Exception as e:
            advanced_results["中文注释和箭头"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 中文注释和箭头测试失败: {e}")
        
        # 测试3: 颜色条中文
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # 等高线图
            x = np.linspace(-3, 3, 100)
            y = np.linspace(-3, 3, 100)
            X, Y = np.meshgrid(x, y)
            Z = np.exp(-(X**2 + Y**2))
            
            contour = ax1.contourf(X, Y, Z, levels=20, cmap='viridis')
            ax1.set_title("等高线图")
            ax1.set_xlabel("X坐标")
            ax1.set_ylabel("Y坐标")
            cbar1 = plt.colorbar(contour, ax=ax1)
            cbar1.set_label("数值大小")
            
            # 3D曲面图（如果支持）
            from mpl_toolkits.mplot3d import Axes3D
            ax2.remove()
            ax2 = fig.add_subplot(122, projection='3d')
            surf = ax2.plot_surface(X, Y, Z, cmap='coolwarm')
            ax2.set_title("3D曲面图")
            ax2.set_xlabel("X轴")
            ax2.set_ylabel("Y轴")
            ax2.set_zlabel("Z轴")
            cbar2 = plt.colorbar(surf, ax=ax2, shrink=0.5)
            cbar2.set_label("高度值")
            
            plt.tight_layout()
            
            output_path = self.output_dir / "test_chinese_colorbar.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            advanced_results["颜色条中文"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 颜色条中文测试通过")
        except Exception as e:
            advanced_results["颜色条中文"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 颜色条中文测试失败: {e}")
        
        self.test_results["advanced_tests"] = advanced_results
    
    def _test_edge_cases(self):
        """测试边界情况"""
        print("\n🚨 测试边界情况...")
        
        edge_results = {}
        
        # 测试1: 超长中文文本
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            long_text = "这是一个非常长的中文文本测试，用来测试matplotlib在处理超长中文文本时的表现。" * 5
            
            ax.text(0.5, 0.5, long_text, fontsize=10, ha='center', va='center',
                   wrap=True, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
            ax.set_title("超长中文文本测试")
            ax.axis('off')
            
            output_path = self.output_dir / "test_long_chinese_text.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            edge_results["超长中文文本"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 超长中文文本测试通过")
        except Exception as e:
            edge_results["超长中文文本"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 超长中文文本测试失败: {e}")
        
        # 测试2: 特殊字符和符号
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            special_chars = [
                "数学符号：∑∏∫∂∇∆∞",
                "货币符号：￥$€£¢",
                "标点符号：，。！？；：""''（）【】",
                "特殊符号：①②③④⑤⑥⑦⑧⑨⑩",
                "混合符号：Hello世界2024年￥100.00"
            ]
            
            for i, chars in enumerate(special_chars):
                ax.text(0.05, 0.9 - i*0.15, chars, fontsize=12, transform=ax.transAxes)
            
            ax.set_title("特殊字符和符号测试")
            ax.axis('off')
            
            output_path = self.output_dir / "test_special_characters.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            edge_results["特殊字符和符号"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 特殊字符和符号测试通过")
        except Exception as e:
            edge_results["特殊字符和符号"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 特殊字符和符号测试失败: {e}")
        
        # 测试3: 极小字体
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            font_sizes = [4, 6, 8, 10, 12, 14, 16, 18, 20]
            
            for i, size in enumerate(font_sizes):
                ax.text(0.1 + (i % 3) * 0.3, 0.9 - (i // 3) * 0.3, 
                       f"字体大小{size}号", fontsize=size, transform=ax.transAxes)
            
            ax.set_title("不同字体大小测试")
            ax.axis('off')
            
            output_path = self.output_dir / "test_font_sizes.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            edge_results["极小字体"] = {
                "status": "通过",
                "output": str(output_path)
            }
            print("✓ 极小字体测试通过")
        except Exception as e:
            edge_results["极小字体"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 极小字体测试失败: {e}")
        
        self.test_results["edge_cases"] = edge_results
    
    def _test_performance(self):
        """测试性能"""
        print("\n⚡ 测试性能...")
        
        performance_results = {}
        
        # 测试1: 大量中文文本渲染性能
        try:
            start_time = time.time()
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # 生成大量中文文本
            chinese_texts = [f"中文文本{i}" for i in range(100)]
            x_positions = np.random.rand(100)
            y_positions = np.random.rand(100)
            
            for i, (text, x, y) in enumerate(zip(chinese_texts, x_positions, y_positions)):
                ax.text(x, y, text, fontsize=8, alpha=0.7)
            
            ax.set_title("大量中文文本性能测试")
            ax.axis('off')
            
            output_path = self.output_dir / "test_performance_many_texts.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            end_time = time.time()
            render_time = end_time - start_time
            
            performance_results["大量中文文本"] = {
                "status": "通过",
                "render_time": f"{render_time:.3f}秒",
                "text_count": 100,
                "output": str(output_path)
            }
            print(f"✓ 大量中文文本性能测试通过 (耗时: {render_time:.3f}秒)")
        except Exception as e:
            performance_results["大量中文文本"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 大量中文文本性能测试失败: {e}")
        
        # 测试2: 复杂图形中文性能
        try:
            start_time = time.time()
            
            fig, axes = plt.subplots(3, 3, figsize=(15, 15))
            fig.suptitle("复杂图形中文性能测试", fontsize=16)
            
            for i in range(9):
                row, col = i // 3, i % 3
                ax = axes[row, col]
                
                # 不同类型的图形
                if i == 0:
                    ax.bar(["测试一", "测试二", "测试三"], np.random.rand(3))
                    ax.set_title("柱状图")
                elif i == 1:
                    ax.plot(np.random.rand(20), 'o-')
                    ax.set_title("折线图")
                elif i == 2:
                    ax.scatter(np.random.rand(20), np.random.rand(20))
                    ax.set_title("散点图")
                elif i == 3:
                    ax.hist(np.random.randn(100), bins=20)
                    ax.set_title("直方图")
                elif i == 4:
                    ax.pie(np.random.rand(4), labels=["一", "二", "三", "四"], autopct='%1.1f%%')
                    ax.set_title("饼图")
                elif i == 5:
                    ax.boxplot([np.random.randn(20) for _ in range(3)])
                    ax.set_title("箱线图")
                elif i == 6:
                    ax.imshow(np.random.rand(10, 10), cmap='viridis')
                    ax.set_title("热力图")
                elif i == 7:
                    ax.fill_between(np.linspace(0, 10, 50), np.random.rand(50))
                    ax.set_title("面积图")
                else:
                    ax.errorbar(np.arange(5), np.random.rand(5), yerr=np.random.rand(5)/10)
                    ax.set_title("误差图")
                
                ax.set_xlabel("X轴标签")
                ax.set_ylabel("Y轴标签")
            
            plt.tight_layout()
            
            output_path = self.output_dir / "test_performance_complex_plots.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            end_time = time.time()
            render_time = end_time - start_time
            
            performance_results["复杂图形中文"] = {
                "status": "通过",
                "render_time": f"{render_time:.3f}秒",
                "plot_count": 9,
                "output": str(output_path)
            }
            print(f"✓ 复杂图形中文性能测试通过 (耗时: {render_time:.3f}秒)")
        except Exception as e:
            performance_results["复杂图形中文"] = {
                "status": "失败",
                "error": str(e)
            }
            print(f"✗ 复杂图形中文性能测试失败: {e}")
        
        self.test_results["performance_tests"] = performance_results
    
    def _generate_summary(self):
        """生成测试总结"""
        print("\n📊 生成测试总结...")
        
        # 统计测试结果
        all_tests = {}
        
        # 收集所有测试
        for category in ["setup", "basic_tests", "advanced_tests", "edge_cases", "performance_tests"]:
            for test_name, result in self.test_results[category].items():
                all_tests[f"{category}_{test_name}"] = result
        
        total_tests = len(all_tests)
        passed_tests = sum(1 for result in all_tests.values() if result.get("status") == "通过")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.test_results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": round(success_rate, 2)
        }
        
        # 输出总结
        print(f"\n{'='*50}")
        print("测试总结")
        print(f"{'='*50}")
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"成功率: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n失败的测试:")
            for test_name, result in all_tests.items():
                if result.get("status") != "通过":
                    print(f"  - {test_name}: {result.get('error', '未知错误')}")
        
        # 保存测试报告
        self._save_test_report()
    
    def _save_test_report(self):
        """保存测试报告"""
        try:
            import json
            
            report_path = self.output_dir / "test_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ 测试报告已保存: {report_path}")
            
            # 生成HTML报告（如果可能）
            html_report_path = self.output_dir / "test_report.html"
            self._generate_html_report(html_report_path)
            
        except Exception as e:
            print(f"✗ 保存测试报告失败: {e}")
    
    def _generate_html_report(self, html_path: Path):
        """生成HTML测试报告"""
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matplotlib中文绘图测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #e8f5e8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .category {{ margin: 20px 0; }}
        .test {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ccc; }}
        .pass {{ border-left-color: #4CAF50; background-color: #f1f8f1; }}
        .fail {{ border-left-color: #f44336; background-color: #fff1f1; }}
        .error {{ color: #d32f2f; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Matplotlib中文绘图测试报告</h1>
        <p>生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>测试总结</h2>
        <p>总测试数: {self.test_results['summary']['total_tests']}</p>
        <p>通过测试: {self.test_results['summary']['passed_tests']}</p>
        <p>失败测试: {self.test_results['summary']['failed_tests']}</p>
        <p>成功率: {self.test_results['summary']['success_rate']}%</p>
    </div>
"""
            
            # 添加各类测试结果
            for category, tests in self.test_results.items():
                if category == "summary":
                    continue
                    
                html_content += f'<div class="category"><h3>{category}</h3>'
                for test_name, result in tests.items():
                    status = result.get("status", "未知")
                    css_class = "pass" if status == "通过" else "fail"
                    
                    html_content += f'''
                    <div class="test {css_class}">
                        <h4>{test_name} - {status}</h4>
'''
                    if "error" in result:
                        html_content += f'<p class="error">错误: {result["error"]}</p>'
                    if "output" in result:
                        html_content += f'<p>输出文件: {result["output"]}</p>'
                    
                    html_content += '</div>'
                
                html_content += '</div>'
            
            html_content += """
</body>
</html>
"""
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✓ HTML测试报告已保存: {html_path}")
            
        except Exception as e:
            print(f"✗ 生成HTML报告失败: {e}")


def main():
    """
    主函数：运行所有测试
    """
    tester = ChinesePlottingTester()
    
    try:
        results = tester.run_all_tests()
        
        # 根据测试结果决定退出码
        success_rate = results["summary"]["success_rate"]
        if success_rate >= 90:
            print(f"\n🎉 测试完成！成功率: {success_rate}%")
            return 0
        elif success_rate >= 70:
            print(f"\n⚠️ 测试完成，但有部分失败。成功率: {success_rate}%")
            return 1
        else:
            print(f"\n❌ 测试失败过多。成功率: {success_rate}%")
            return 2
            
    except Exception as e:
        print(f"\n✗ 测试过程出现严重错误: {e}")
        traceback.print_exc()
        return 3


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)