"""
Matplotlib 中文字体配置模块

提供统一的中文字体配置接口，解决 Matplotlib 在绘图时中文显示为方框的问题。
支持自动检测系统可用的中文字体，并提供方便的配置函数。
"""

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
    font_name: Optional[str] = None, font_size: int = 12, enable_warnings: bool = False
) -> str:
    """
    配置 Matplotlib 使用中文字体

    自动检测系统中可用的中文字体，并配置 Matplotlib 的字体设置，
    包括字体、字号、坐标轴标签、图例等所有中文显示相关参数。

    参数:
        font_name: 指定使用的字体名称。如果为 None，则自动检测。
        font_size: 字体大小（默认 12）
        enable_warnings: 是否启用 Matplotlib 警告（默认 False）

    返回:
        实际使用的字体名称

    异常:
        RuntimeError: 未找到可用的中文字体时抛出

    示例:
        >>> setup_chinese_font()
        'SimHei'
        >>> setup_chinese_font('Microsoft YaHei', font_size=14)
        'Microsoft YaHei'
    """
    # 禁用 matplotlib 警告（如 negative width bbox 等）
    if not enable_warnings:
        warnings.filterwarnings("ignore", category=UserWarning)
        msg = ".*Matplotlib is currently using agg.*"
        warnings.filterwarnings("ignore", message=msg)

    # 如果未指定字体，自动检测
    if font_name is None:
        font_name = detect_chinese_font()

    # 如果仍未找到字体，抛出异常
    if font_name is None:
        raise RuntimeError(
            "未找到可用的中文字体。" "请安装以下字体之一: " + ", ".join(PREFERRED_FONTS)
        )

    # 验证指定的字体是否可用
    available_fonts = get_available_fonts()
    if font_name not in available_fonts:
        raise ValueError(f'字体 "{font_name}" 不可用。' f"可用的中文字体: {detect_chinese_font()}")

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

    return font_name


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
