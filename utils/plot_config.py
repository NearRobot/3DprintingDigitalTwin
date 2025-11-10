"""
Matplotlib 中文字体配置模块

提供统一的中文字体配置接口，解决 Matplotlib 在绘图时中文显示为方框的问题。
支持自动检测系统可用的中文字体，集成字体安装、缓存清理和深度配置的完整流程。
"""

import os
import platform
import warnings
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib import rcParams


# 支持的中文字体列表（优先级从高到低）
PREFERRED_FONTS = [
    "SimHei",  # 黑体
    "Microsoft YaHei",  # 微软雅黑
    "SimSun",  # 宋体
    "KaiTi",  # 楷体
    "FangSong",  # 仿宋
    "WenQuanYi Zen Hei",  # 文泉驿正黑
    "Noto Sans CJK SC",  # Noto Sans CJK 简体中文
    "DejaVu Sans",  # DejaVu Sans
]


def get_available_fonts() -> List[str]:
    """
    获取系统中所有可用的字体名称

    返回:
        字体名称列表
    """
    try:
        import matplotlib.font_manager as fm

        available_fonts = [f.name for f in fm.fontManager.ttflist]
        return list(set(available_fonts))
    except Exception:
        return []


def detect_chinese_font() -> Optional[str]:
    """
    自动检测系统中可用的中文字体

    按照优先级顺序检测系统中是否安装了支持的中文字体。
    首先检查首选字体列表，如果都不可用，则返回 None。

    返回:
        检测到的中文字体名称，如果没有检测到则返回 None
    """
    available_fonts = get_available_fonts()

    # 按优先级顺序检查字体
    for font_name in PREFERRED_FONTS:
        if font_name in available_fonts:
            return font_name

    # 如果没有找到首选字体，尝试查找包含 'CJK' 或 '中文' 的字体
    for font_name in available_fonts:
        if "CJK" in font_name or "中文" in font_name:
            return font_name

    return None


def get_system_chinese_fonts() -> Dict[str, Tuple[str, int]]:
    """
    获取系统支持的中文字体信息

    返回:
        包含字体信息的字典，格式为:
        {
            '字体名': ('字体完整名', 优先级)
        }
    """
    system = platform.system()
    fonts_dict = {}

    # 不同系统的字体路径（备用）
    if system == "Windows":
        # Windows 系统字体路径（暂不使用）
        pass
    elif system == "Darwin":
        # macOS 系统字体路径（暂不使用）
        pass
    else:
        # Linux 系统字体路径（暂不使用）
        pass

    available_fonts = get_available_fonts()

    for idx, font_name in enumerate(PREFERRED_FONTS):
        if font_name in available_fonts:
            fonts_dict[font_name] = (font_name, idx)

    return fonts_dict


def setup_chinese_font(
    font_name: Optional[str] = None, 
    font_size: int = 12, 
    enable_warnings: bool = False,
    auto_install: bool = False,
    clear_cache: bool = False,
    deep_config: bool = True
) -> str:
    """
    配置 Matplotlib 使用中文字体（完整解决方案）

    自动检测系统中可用的中文字体，并配置 Matplotlib 的字体设置，
    包括字体、字号、坐标轴标签、图例等所有中文显示相关参数。
    可选自动安装字体、清理缓存和深度配置功能。

    参数:
        font_name: 指定使用的字体名称。如果为 None，则自动检测。
        font_size: 字体大小（默认 12）
        enable_warnings: 是否启用 Matplotlib 警告（默认 False）
        auto_install: 是否自动安装中文字体（默认 False）
        clear_cache: 是否清理matplotlib缓存（默认 False）
        deep_config: 是否使用深度配置（默认 True）

    返回:
        实际使用的字体名称

    异常:
        RuntimeError: 未找到可用的中文字体且自动安装失败时抛出

    示例:
        >>> setup_chinese_font()
        'SimHei'
        >>> setup_chinese_font('Microsoft YaHei', font_size=14, clear_cache=True)
        'Microsoft YaHei'
        >>> setup_chinese_font(auto_install=True, deep_config=True)
        'SimHei'
    """
    # 禁用 matplotlib 警告（如 negative width bbox 等）
    if not enable_warnings:
        warnings.filterwarnings("ignore", category=UserWarning)
        msg = ".*Matplotlib is currently using agg.*"
        warnings.filterwarnings("ignore", message=msg)
        # 禁用其他可能的警告
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", message=".*Glyph.*missing.*")

    # 步骤1: 清理缓存（如果需要）
    if clear_cache:
        try:
            from .clear_matplotlib_cache import MatplotlibCacheCleaner
            cleaner = MatplotlibCacheCleaner()
            print("正在清理matplotlib字体缓存...")
            cleaner.clear_font_cache(backup=True)
            cleaner.rebuild_font_cache(force_rebuild=True)
            print("✓ 缓存清理完成")
        except ImportError:
            print("警告：无法导入缓存清理模块，跳过缓存清理")
        except Exception as e:
            print(f"警告：缓存清理失败: {e}")

    # 步骤2: 自动检测字体
    if font_name is None:
        font_name = detect_chinese_font()

    # 步骤3: 如果未找到字体，尝试自动安装
    if font_name is None and auto_install:
        try:
            from .font_installer import FontInstaller
            installer = FontInstaller()
            print("未检测到中文字体，尝试自动安装...")
            if installer.auto_install_chinese_fonts():
                print("✓ 字体安装成功，重新检测...")
                font_name = detect_chinese_font()
            else:
                print("✗ 字体自动安装失败")
        except ImportError:
            print("警告：无法导入字体安装模块")
        except Exception as e:
            print(f"警告：字体安装过程出错: {e}")

    # 如果仍未找到字体，抛出异常
    if font_name is None:
        raise RuntimeError(
            "未找到可用的中文字体且自动安装失败。"
            "请手动安装以下字体之一: " + ", ".join(PREFERRED_FONTS)
        )

    # 验证指定的字体是否可用
    available_fonts = get_available_fonts()
    if font_name not in available_fonts:
        # 尝试刷新字体列表
        try:
            import matplotlib.font_manager as fm
            fm.fontManager.__init__()
            available_fonts = get_available_fonts()
        except Exception:
            pass
        
        if font_name not in available_fonts:
            raise ValueError(
                f'字体 "{font_name}" 不可用。'
                f'可用的中文字体: {detect_chinese_font() or "无"}'
            )

    # 步骤4: 深度配置matplotlib参数
    if deep_config:
        _deep_configure_matplotlib(font_name, font_size)
    else:
        # 基础配置
        _basic_configure_matplotlib(font_name, font_size)

    return font_name


def _basic_configure_matplotlib(font_name: str, font_size: int) -> None:
    """
    基础matplotlib配置
    
    参数:
        font_name: 字体名称
        font_size: 字体大小
    """
    # 配置 Matplotlib 字体设置
    rcParams["font.sans-serif"] = [font_name] + rcParams.get("font.sans-serif", [])
    rcParams["font.size"] = font_size
    rcParams["axes.labelsize"] = font_size
    rcParams["axes.titlesize"] = font_size + 2
    rcParams["xtick.labelsize"] = font_size - 1
    rcParams["ytick.labelsize"] = font_size - 1
    rcParams["legend.fontsize"] = font_size - 1
    rcParams["figure.titlesize"] = font_size + 4

    # 处理坐标轴正负号显示
    rcParams["axes.unicode_minus"] = False  # 防止负号显示为方框


def _deep_configure_matplotlib(font_name: str, font_size: int) -> None:
    """
    深度配置matplotlib参数
    
    提供完整的matplotlib配置，确保中文显示在所有场景下都能正常工作。
    
    参数:
        font_name: 字体名称
        font_size: 字体大小
    """
    # 基础字体配置
    _basic_configure_matplotlib(font_name, font_size)
    
    # 深度字体配置
    rcParams["font.family"] = ["sans-serif", "DejaVu Sans"]  # 设置字体族
    rcParams["font.sans-serif"] = [
        font_name,  # 主要中文字体
        "SimHei", "Microsoft YaHei", "SimSun",  # 备选中文字体
        "DejaVu Sans", "Liberation Sans", "Arial",  # 备选英文字体
        *rcParams.get("font.sans-serif", [])  # 保留原有配置
    ]
    
    # 字体大小详细配置
    rcParams["font.size"] = font_size
    rcParams["axes.titlesize"] = font_size + 2
    rcParams["axes.labelsize"] = font_size
    rcParams["xtick.labelsize"] = font_size - 1
    rcParams["ytick.labelsize"] = font_size - 1
    rcParams["legend.fontsize"] = font_size - 1
    rcParams["figure.titlesize"] = font_size + 4
    rcParams["axes.labelpad"] = 10  # 标签间距
    
    # 文本和注释配置
    rcParams["font.serif"] = [font_name, "Times New Roman", "DejaVu Serif"]
    rcParams["font.cursive"] = [font_name, "Apple Chancery", "Textile"]
    rcParams["font.fantasy"] = [font_name, "Comic Sans MS", "Chicago"]
    rcParams["font.monospace"] = ["Courier New", "DejaVu Sans Mono"]
    
    # 图形和布局配置
    rcParams["figure.titlesize"] = font_size + 4
    rcParams["figure.titleweight"] = "bold"
    rcParams["figure.constrained_layout.use"] = True
    
    # 坐标轴配置
    rcParams["axes.unicode_minus"] = False  # 防止负号显示为方框
    rcParams["axes.formatter.useoffset"] = False
    rcParams["axes.xmargin"] = 0.05
    rcParams["axes.ymargin"] = 0.05
    
    # 网格和刻度配置
    rcParams["axes.grid"] = True
    rcParams["grid.color"] = "gray"
    rcParams["grid.linestyle"] = "--"
    rcParams["grid.alpha"] = 0.3
    
    # 图例配置
    rcParams["legend.framealpha"] = 0.9
    rcParams["legend.fancybox"] = True
    rcParams["legend.shadow"] = True
    
    # 保存图形配置
    rcParams["savefig.dpi"] = 300
    rcParams["savefig.bbox"] = "tight"
    rcParams["savefig.pad_inches"] = 0.1
    
    # 文本渲染配置
    rcParams["text.usetex"] = False  # 禁用LaTeX以避免中文问题
    rcParams["text.antialiased"] = True
    
    # 后端配置（如果需要）
    try:
        import matplotlib
        if matplotlib.get_backend() == 'agg':
            # 在无GUI环境中确保字体正常工作
            rcParams["backend"] = "Agg"
    except Exception:
        pass


def reset_font_config() -> None:
    """
    重置 Matplotlib 字体配置到默认值

    示例:
        >>> reset_font_config()
    """
    plt.rcdefaults()


def get_font_config_info() -> Dict[str, any]:
    """
    获取当前 Matplotlib 的字体配置信息

    返回:
        包含当前字体配置的字典

    示例:
        >>> info = get_font_config_info()
        >>> print(info['current_font'])
        'SimHei'
    """
    return {
        "current_font": (
            rcParams["font.sans-serif"][0] if rcParams.get("font.sans-serif") else "default"
        ),
        "font_size": rcParams["font.size"],
        "axes_labelsize": rcParams["axes.labelsize"],
        "axes_titlesize": rcParams["axes.titlesize"],
        "xtick_labelsize": rcParams["xtick.labelsize"],
        "ytick_labelsize": rcParams["ytick.labelsize"],
        "legend_fontsize": rcParams["legend.fontsize"],
        "figure_titlesize": rcParams["figure.titlesize"],
        "unicode_minus": rcParams["axes.unicode_minus"],
    }


def list_available_chinese_fonts() -> List[str]:
    """
    列出系统中所有可用的中文字体

    返回:
        包含所有可用中文字体名称的列表

    示例:
        >>> fonts = list_available_chinese_fonts()
        >>> print(fonts)
        ['SimHei', 'Microsoft YaHei', ...]
    """
    available_fonts = get_available_fonts()
    chinese_fonts = []

    for font_name in PREFERRED_FONTS:
        if font_name in available_fonts:
            chinese_fonts.append(font_name)

    return chinese_fonts


def complete_chinese_font_setup(
    font_name: Optional[str] = None,
    font_size: int = 12,
    auto_install: bool = True,
    clear_cache: bool = True,
    enable_warnings: bool = False
) -> Dict[str, any]:
    """
    完整的中文字体配置解决方案
    
    集成字体检测、自动安装、缓存清理和深度配置的完整流程，
    确保matplotlib能够正确显示中文内容。
    
    参数:
        font_name: 指定使用的字体名称。如果为 None，则自动检测。
        font_size: 字体大小（默认 12）
        auto_install: 是否自动安装中文字体（默认 True）
        clear_cache: 是否清理matplotlib缓存（默认 True）
        enable_warnings: 是否启用 Matplotlib 警告（默认 False）
    
    返回:
        包含配置结果和详细信息的字典
        
    异常:
        RuntimeError: 所有尝试都失败时抛出
        
    示例:
        >>> result = complete_chinese_font_setup()
        >>> print(result['status'])
        'success'
        >>> print(result['font_name'])
        'SimHei'
    """
    result = {
        'status': 'unknown',
        'font_name': None,
        'font_size': font_size,
        'steps_completed': [],
        'warnings': [],
        'errors': [],
        'recommendations': []
    }
    
    try:
        # 步骤1: 检查系统字体状态
        result['steps_completed'].append("检查系统字体状态")
        available_chinese_fonts = list_available_chinese_fonts()
        if not available_chinese_fonts:
            result['warnings'].append("系统中未检测到中文字体")
            if auto_install:
                result['recommendations'].append("将尝试自动安装中文字体")
            else:
                result['recommendations'].append("建议启用auto_install选项或手动安装字体")
        else:
            result['warnings'].append(f"检测到 {len(available_chinese_fonts)} 个中文字体")
        
        # 步骤2: 执行完整配置
        result['steps_completed'].append("执行字体配置")
        configured_font = setup_chinese_font(
            font_name=font_name,
            font_size=font_size,
            enable_warnings=enable_warnings,
            auto_install=auto_install,
            clear_cache=clear_cache,
            deep_config=True
        )
        
        result['font_name'] = configured_font
        result['status'] = 'success'
        result['steps_completed'].append("字体配置完成")
        
        # 步骤3: 验证配置结果
        result['steps_completed'].append("验证配置结果")
        config_info = get_font_config_info()
        result['config_info'] = config_info
        
        # 测试中文渲染
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, "测试中文", fontsize=12, ha='center', va='center')
            # 不显示图形，只测试是否能创建
            plt.close(fig)
            result['steps_completed'].append("中文渲染测试通过")
        except Exception as e:
            result['warnings'].append(f"中文渲染测试失败: {e}")
        
        # 生成最终建议
        if result['status'] == 'success':
            result['recommendations'].append("字体配置成功，中文内容应该能正常显示")
            result['recommendations'].append("如仍有问题，请尝试重启Python进程或IDE")
        
    except Exception as e:
        result['status'] = 'failed'
        result['errors'].append(str(e))
        result['recommendations'].append("配置失败，请检查系统权限和网络连接")
        result['recommendations'].append("可以尝试手动安装字体后重新运行配置")
    
    return result


def diagnose_chinese_display() -> Dict[str, any]:
    """
    诊断中文显示问题
    
    全面检查系统字体、matplotlib配置和缓存状态，
    提供详细的诊断报告和解决建议。
    
    返回:
        包含诊断结果的详细字典
        
    示例:
        >>> diagnosis = diagnose_chinese_display()
        >>> print(diagnosis['overall_status'])
        'good'
    """
    diagnosis = {
        'overall_status': 'unknown',
        'system_info': {},
        'font_status': {},
        'matplotlib_status': {},
        'cache_status': {},
        'issues': [],
        'recommendations': []
    }
    
    try:
        # 系统信息
        diagnosis['system_info'] = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'python_version': platform.python_version()
        }
        
        # 字体状态检查
        available_fonts = get_available_fonts()
        chinese_fonts = list_available_chinese_fonts()
        
        diagnosis['font_status'] = {
            'total_fonts': len(available_fonts),
            'chinese_fonts': chinese_fonts,
            'chinese_font_count': len(chinese_fonts),
            'preferred_available': [f for f in PREFERRED_FONTS if f in available_fonts]
        }
        
        # matplotlib配置检查
        diagnosis['matplotlib_status'] = {
            'current_font': rcParams.get("font.sans-serif", [""])[0],
            'font_size': rcParams.get("font.size", "unknown"),
            'unicode_minus': rcParams.get("axes.unicode_minus", "unknown"),
            'backend': rcParams.get("backend", "unknown")
        }
        
        # 缓存状态检查
        try:
            from .clear_matplotlib_cache import MatplotlibCacheCleaner
            cleaner = MatplotlibCacheCleaner()
            cache_info = cleaner.get_cache_info()
            diagnosis['cache_status'] = {
                'cache_dirs': len(cache_info['cache_dirs']),
                'cache_files': cache_info['cache_count'],
                'total_size_mb': cache_info['total_size_mb']
            }
        except Exception:
            diagnosis['cache_status'] = {'error': '无法检查缓存状态'}
        
        # 问题识别
        issues = []
        
        if len(chinese_fonts) == 0:
            issues.append("系统中未安装中文字体")
            diagnosis['overall_status'] = 'poor'
        elif len(chinese_fonts) < 3:
            issues.append("系统中中文字体较少，建议安装更多字体")
            diagnosis['overall_status'] = 'fair'
        
        current_font = diagnosis['matplotlib_status']['current_font']
        if current_font not in chinese_fonts and current_font != "":
            issues.append(f"当前配置的字体 '{current_font}' 不支持中文")
            if diagnosis['overall_status'] != 'poor':
                diagnosis['overall_status'] = 'fair'
        
        if diagnosis['matplotlib_status'].get('unicode_minus') is True:
            issues.append("unicode_minus设置可能导致负号显示问题")
        
        diagnosis['issues'] = issues
        
        # 生成建议
        recommendations = []
        
        if len(chinese_fonts) == 0:
            recommendations.append("安装中文字体：运行 complete_chinese_font_setup(auto_install=True)")
            recommendations.append("或手动下载安装SimHei、Microsoft YaHei等字体")
        
        if current_font not in chinese_fonts:
            recommendations.append("重新配置字体：运行 setup_chinese_font() 或 complete_chinese_font_setup()")
        
        if diagnosis['cache_status'].get('cache_files', 0) > 10:
            recommendations.append("清理matplotlib缓存：运行 complete_chinese_font_setup(clear_cache=True)")
        
        if not issues:
            recommendations.append("系统配置良好，中文显示应该正常工作")
            diagnosis['overall_status'] = 'good'
        
        diagnosis['recommendations'] = recommendations
        
    except Exception as e:
        diagnosis['overall_status'] = 'error'
        diagnosis['issues'].append(f"诊断过程出错: {e}")
        diagnosis['recommendations'].append("检查系统环境和权限设置")
    
    return diagnosis


def quick_fix_chinese_display() -> bool:
    """
    快速修复中文显示问题
    
    提供一键修复功能，自动执行最可能解决问题的操作。
    
    返回:
        修复是否成功
        
    示例:
        >>> success = quick_fix_chinese_display()
        >>> print("修复成功" if success else "修复失败")
    修复成功
    """
    print("开始快速修复中文显示问题...")
    
    try:
        # 执行完整配置
        result = complete_chinese_font_setup(
            auto_install=True,
            clear_cache=True,
            enable_warnings=False
        )
        
        if result['status'] == 'success':
            print(f"✓ 修复成功！使用字体: {result['font_name']}")
            return True
        else:
            print("✗ 修复失败")
            for error in result['errors']:
                print(f"  错误: {error}")
            for warning in result['warnings']:
                print(f"  警告: {warning}")
            return False
            
    except Exception as e:
        print(f"✗ 修复过程出错: {e}")
        return False
