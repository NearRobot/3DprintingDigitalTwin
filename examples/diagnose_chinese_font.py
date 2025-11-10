"""
Matplotlib中文显示诊断脚本

全面诊断系统中文字体安装和matplotlib配置状态，
提供详细的诊断报告和故障排除建议。
"""

import sys
import traceback
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入工具模块
try:
    from utils.clear_matplotlib_cache import MatplotlibCacheCleaner
    from utils.font_installer import FontInstaller
    from utils.plot_config import (
        complete_chinese_font_setup,
        diagnose_chinese_display,
        get_available_fonts,
        list_available_chinese_fonts,
    )
except ImportError as e:
    print(f"✗ 导入工具模块失败: {e}")
    print("请确保在项目根目录下运行此脚本")
    sys.exit(1)


class ChineseFontDiagnostic:
    """
    中文字体诊断器
    
    提供全面的字体和matplotlib配置诊断功能。
    """
    
    def __init__(self):
        """初始化诊断器"""
        self.font_installer = FontInstaller()
        self.cache_cleaner = MatplotlibCacheCleaner()
        self.report = {
            "系统信息": {},
            "字体状态": {},
            "matplotlib配置": {},
            "缓存状态": {},
            "测试结果": {},
            "问题诊断": [],
            "修复建议": []
        }
    
    def run_full_diagnosis(self) -> dict:
        """
        运行完整的诊断流程
        
        返回:
            完整的诊断报告字典
        """
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 20 + "Matplotlib中文显示诊断工具" + " " * 20 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        
        # 1. 系统信息检查
        self._check_system_info()
        
        # 2. 字体状态检查
        self._check_font_status()
        
        # 3. matplotlib配置检查
        self._check_matplotlib_config()
        
        # 4. 缓存状态检查
        self._check_cache_status()
        
        # 5. 中文渲染测试
        self._test_chinese_rendering()
        
        # 6. 问题诊断和建议
        self._diagnose_problems()
        
        # 7. 生成报告
        self._generate_report()
        
        return self.report
    
    def _check_system_info(self):
        """检查系统信息"""
        print("📋 检查系统信息...")
        
        try:
            import platform
            
            system_info = {
                "操作系统": platform.system(),
                "系统版本": platform.release(),
                "Python版本": platform.python_version(),
                "matplotlib版本": matplotlib.__version__,
                "numpy版本": np.__version__
            }
            
            self.report["系统信息"] = system_info
            
            print("✓ 系统信息获取完成")
            for key, value in system_info.items():
                print(f"  - {key}: {value}")
                
        except Exception as e:
            print(f"✗ 系统信息检查失败: {e}")
            self.report["系统信息"] = {"错误": str(e)}
    
    def _check_font_status(self):
        """检查字体状态"""
        print("\n🔤 检查字体状态...")
        
        try:
            # 系统字体状态
            font_status = self.font_installer.check_font_installation_status()
            
            # matplotlib字体状态
            available_fonts = get_available_fonts()
            chinese_fonts = list_available_chinese_fonts()
            
            font_info = {
                "系统字体路径": font_status["font_paths"],
                "系统中文字体数量": font_status["font_count"],
                "系统检测到的中文字体": font_status["chinese_fonts"][:5],  # 只显示前5个
                "matplotlib识别的字体总数": len(available_fonts),
                "matplotlib识别的中文字体": chinese_fonts,
                "推荐字体列表": chinese_fonts[:3] if chinese_fonts else ["无"]
            }
            
            self.report["字体状态"] = font_info
            
            print(f"✓ 字体状态检查完成")
            print(f"  - 系统字体路径: {len(font_status['font_paths'])} 个")
            print(f"  - 系统中文字体: {font_status['font_count']} 个")
            print(f"  - matplotlib中文字体: {len(chinese_fonts)} 个")
            
            if chinese_fonts:
                print("  - 可用中文字体:")
                for font in chinese_fonts:
                    print(f"    • {font}")
            else:
                print("  ⚠ 未检测到中文字体")
                
        except Exception as e:
            print(f"✗ 字体状态检查失败: {e}")
            self.report["字体状态"] = {"错误": str(e)}
    
    def _check_matplotlib_config(self):
        """检查matplotlib配置"""
        print("\n⚙️ 检查matplotlib配置...")
        
        try:
            from matplotlib import rcParams
            
            config_info = {
                "当前字体": rcParams.get("font.sans-serif", [""])[0],
                "字体大小": rcParams.get("font.size", "未知"),
                "字体族": rcParams.get("font.family", "未知"),
                "unicode_minus": rcParams.get("axes.unicode_minus", "未知"),
                "后端": rcParams.get("backend", "未知"),
                "图形大小": rcParams.get("figure.figsize", "未知"),
                "图形DPI": rcParams.get("figure.dpi", "未知")
            }
            
            self.report["matplotlib配置"] = config_info
            
            print("✓ matplotlib配置检查完成")
            for key, value in config_info.items():
                print(f"  - {key}: {value}")
                
        except Exception as e:
            print(f"✗ matplotlib配置检查失败: {e}")
            self.report["matplotlib配置"] = {"错误": str(e)}
    
    def _check_cache_status(self):
        """检查缓存状态"""
        print("\n🗂️ 检查缓存状态...")
        
        try:
            cache_info = self.cache_cleaner.get_cache_info()
            
            cache_status = {
                "缓存目录数量": len(cache_info["cache_dirs"]),
                "缓存文件数量": cache_info["cache_count"],
                "缓存总大小": f"{cache_info['total_size_mb']} MB",
                "缓存文件": [f["name"] for f in cache_info["cache_files"][:5]]  # 只显示前5个
            }
            
            self.report["缓存状态"] = cache_status
            
            print("✓ 缓存状态检查完成")
            for key, value in cache_status.items():
                print(f"  - {key}: {value}")
                
        except Exception as e:
            print(f"✗ 缓存状态检查失败: {e}")
            self.report["缓存状态"] = {"错误": str(e)}
    
    def _test_chinese_rendering(self):
        """测试中文渲染"""
        print("\n🎨 测试中文渲染...")
        
        test_results = {}
        
        # 测试1: 基础中文文本
        try:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, "中文测试", fontsize=16, ha='center', va='center')
            ax.set_title("中文标题测试")
            ax.set_xlabel("X轴标签")
            ax.set_ylabel("Y轴标签")
            
            # 保存测试图
            output_dir = project_root / "outputs"
            output_dir.mkdir(exist_ok=True)
            test_path = output_dir / "chinese_rendering_test.png"
            plt.savefig(test_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            test_results["基础中文渲染"] = "成功"
            test_results["测试图片路径"] = str(test_path)
            print("✓ 基础中文渲染测试通过")
            
        except Exception as e:
            test_results["基础中文渲染"] = f"失败: {e}"
            print(f"✗ 基础中文渲染测试失败: {e}")
        
        # 测试2: 复杂中文文本
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # 测试各种中文元素
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            
            ax.plot(x, y, 'b-', label="正弦函数")
            ax.set_title("三角函数图表：正弦波形展示", fontsize=14, fontweight='bold')
            ax.set_xlabel("横坐标（弧度制）", fontsize=12)
            ax.set_ylabel("纵坐标（函数值）", fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # 添加中文注释
            ax.annotate("最大值点", xy=(np.pi/2, 1), xytext=(2, 0.5),
                       arrowprops=dict(arrowstyle='->'), fontsize=10)
            
            # 保存测试图
            test_path = output_dir / "chinese_complex_test.png"
            plt.savefig(test_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            test_results["复杂中文渲染"] = "成功"
            test_results["复杂测试图片路径"] = str(test_path)
            print("✓ 复杂中文渲染测试通过")
            
        except Exception as e:
            test_results["复杂中文渲染"] = f"失败: {e}"
            print(f"✗ 复杂中文渲染测试失败: {e}")
        
        # 测试3: 字体回退测试
        try:
            fig, ax = plt.subplots(figsize=(6, 3))
            
            # 测试不同字体
            fonts_to_test = ["SimHei", "Microsoft YaHei", "SimSun"]
            for i, font in enumerate(fonts_to_test):
                try:
                    plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
                    ax.text(0.1, 0.8 - i*0.3, f"字体测试：{font}", fontsize=12, transform=ax.transAxes)
                except Exception:
                    pass
            
            ax.set_title("字体回退测试")
            test_path = output_dir / "font_fallback_test.png"
            plt.savefig(test_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            test_results["字体回退"] = "成功"
            print("✓ 字体回退测试通过")
            
        except Exception as e:
            test_results["字体回退"] = f"失败: {e}"
            print(f"✗ 字体回退测试失败: {e}")
        
        self.report["测试结果"] = test_results
    
    def _diagnose_problems(self):
        """诊断问题并生成建议"""
        print("\n🔍 诊断问题...")
        
        problems = []
        suggestions = []
        
        # 检查字体问题
        font_status = self.report.get("字体状态", {})
        if font_status.get("系统中文字体数量", 0) == 0:
            problems.append("系统中未安装中文字体")
            suggestions.append("运行字体安装：python -m utils.font_installer")
            suggestions.append("或手动下载安装SimHei、Microsoft YaHei等字体")
        
        if font_status.get("matplotlib识别的中文字体数量", 0) == 0:
            problems.append("matplotlib无法识别中文字体")
            suggestions.append("清理matplotlib缓存：python -m utils.clear_matplotlib_cache")
            suggestions.append("或运行完整配置：complete_chinese_font_setup(clear_cache=True)")
        
        # 检查配置问题
        mpl_config = self.report.get("matplotlib配置", {})
        current_font = mpl_config.get("当前字体", "")
        if current_font and current_font not in font_status.get("matplotlib识别的中文字体", []):
            problems.append(f"当前配置的字体 '{current_font}' 不支持中文")
            suggestions.append("重新配置字体：setup_chinese_font() 或 complete_chinese_font_setup()")
        
        if mpl_config.get("unicode_minus") is True:
            problems.append("unicode_minus设置可能导致负号显示问题")
            suggestions.append("设置 rcParams['axes.unicode_minus'] = False")
        
        # 检查测试结果
        test_results = self.report.get("测试结果", {})
        failed_tests = [test for test, result in test_results.items() 
                       if isinstance(result, str) and result.startswith("失败")]
        if failed_tests:
            problems.append(f"中文渲染测试失败: {', '.join(failed_tests)}")
            suggestions.append("尝试快速修复：quick_fix_chinese_display()")
        
        # 检查缓存问题
        cache_status = self.report.get("缓存状态", {})
        if cache_status.get("缓存文件数量", 0) > 20:
            problems.append("matplotlib缓存文件过多，可能影响性能")
            suggestions.append("清理缓存：MatplotlibCacheCleaner().clear_font_cache()")
        
        self.report["问题诊断"] = problems
        self.report["修复建议"] = suggestions
        
        # 输出诊断结果
        if problems:
            print(f"发现 {len(problems)} 个问题:")
            for i, problem in enumerate(problems, 1):
                print(f"  {i}. {problem}")
        else:
            print("✓ 未发现明显问题")
        
        if suggestions:
            print(f"\n💡 修复建议:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
    
    def _generate_report(self):
        """生成完整报告"""
        print("\n📄 生成诊断报告...")
        
        # 保存文本报告
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)
        report_path = output_dir / "chinese_font_diagnosis_report.txt"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("Matplotlib中文显示诊断报告\n")
                f.write("=" * 50 + "\n\n")
                
                # 写入各部分内容
                for section, content in self.report.items():
                    f.write(f"【{section}】\n")
                    f.write("-" * 30 + "\n")
                    
                    if isinstance(content, dict):
                        for key, value in content.items():
                            f.write(f"{key}: {value}\n")
                    elif isinstance(content, list):
                        for i, item in enumerate(content, 1):
                            f.write(f"{i}. {item}\n")
                    else:
                        f.write(f"{content}\n")
                    
                    f.write("\n")
            
            print(f"✓ 诊断报告已保存: {report_path}")
            
        except Exception as e:
            print(f"✗ 保存报告失败: {e}")
        
        # 保存JSON格式的详细报告
        try:
            import json
            json_report_path = output_dir / "chinese_font_diagnosis_report.json"
            
            with open(json_report_path, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, ensure_ascii=False, indent=2)
            
            print(f"✓ JSON报告已保存: {json_report_path}")
            
        except Exception as e:
            print(f"✗ 保存JSON报告失败: {e}")
    
    def auto_fix(self) -> bool:
        """
        尝试自动修复发现的问题
        
        返回:
            修复是否成功
        """
        print("\n🔧 尝试自动修复...")
        
        try:
            # 使用完整配置进行修复
            result = complete_chinese_font_setup(
                auto_install=True,
                clear_cache=True,
                enable_warnings=False
            )
            
            if result['status'] == 'success':
                print(f"✓ 自动修复成功！使用字体: {result['font_name']}")
                
                # 重新测试
                print("🔄 重新测试...")
                self._test_chinese_rendering()
                
                return True
            else:
                print("✗ 自动修复失败")
                for error in result.get('errors', []):
                    print(f"  错误: {error}")
                return False
                
        except Exception as e:
            print(f"✗ 自动修复过程出错: {e}")
            return False


def main():
    """
    主函数：运行诊断程序
    """
    diagnostic = ChineseFontDiagnostic()
    
    try:
        # 运行完整诊断
        report = diagnostic.run_full_diagnosis()
        
        # 询问是否自动修复
        if report["问题诊断"]:
            print("\n" + "="*50)
            try:
                response = input("是否尝试自动修复发现的问题？(y/N): ").strip().lower()
                if response in ['y', 'yes', '是']:
                    success = diagnostic.auto_fix()
                    if success:
                        print("\n✓ 自动修复完成！")
                        print("建议重新运行诊断以验证修复效果。")
                    else:
                        print("\n✗ 自动修复失败，请参考上述建议手动修复。")
                else:
                    print("\n请参考上述修复建议手动解决问题。")
            except KeyboardInterrupt:
                print("\n\n操作已取消。")
        else:
            print("\n🎉 系统配置良好，中文显示应该正常工作！")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 诊断过程出现严重错误: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)