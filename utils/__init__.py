"""
工具模块包

提供绘图、配置和其他通用工具函数。
包含完整的Matplotlib中文字体解决方案。
"""

from . import plot_config
from .plot_config import (
    setup_chinese_font,
    detect_chinese_font,
    get_available_fonts,
    reset_font_config,
    get_font_config_info,
    list_available_chinese_fonts,
    complete_chinese_font_setup,
    diagnose_chinese_display,
    quick_fix_chinese_display,
)

# 导入字体安装和缓存清理模块
try:
    from . import font_installer
    from .font_installer import FontInstaller
    from . import clear_matplotlib_cache
    from .clear_matplotlib_cache import MatplotlibCacheCleaner
    
    _FONT_INSTALLER_AVAILABLE = True
except ImportError:
    _FONT_INSTALLER_AVAILABLE = False
    FontInstaller = None
    MatplotlibCacheCleaner = None

__all__ = [
    "plot_config",
    "setup_chinese_font",
    "detect_chinese_font",
    "get_available_fonts",
    "reset_font_config",
    "get_font_config_info",
    "list_available_chinese_fonts",
    "complete_chinese_font_setup",
    "diagnose_chinese_display",
    "quick_fix_chinese_display",
    "font_installer",
    "clear_matplotlib_cache",
    "FontInstaller",
    "MatplotlibCacheCleaner",
    "_FONT_INSTALLER_AVAILABLE",
]
