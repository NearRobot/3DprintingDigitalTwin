"""
系统字体检测与安装模块

提供跨平台的中文字体检测、安装和管理功能。
支持 Windows、Linux 和 macOS 系统。
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class FontInstaller:
    """
    字体安装器类
    
    提供字体检测、安装和管理的完整解决方案。
    支持自动安装中文字体到系统，并提供详细的诊断信息。
    """
    
    # 中文字体下载链接（备选方案）
    FONT_DOWNLOADS = {
        "simhei": {
            "name": "SimHei",
            "url": "https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf",
            "description": "黑体"
        },
        "wqy-zenhei": {
            "name": "WenQuanYi Zen Hei",
            "url": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
            "description": "文泉驿正黑"
        }
    }
    
    # 系统字体路径
    SYSTEM_FONT_PATHS = {
        "Windows": [
            "C:/Windows/Fonts",
            os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
        ],
        "Darwin": [
            "/System/Library/Fonts",
            "/Library/Fonts",
            os.path.expanduser("~/Library/Fonts")
        ],
        "Linux": [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.fonts"),
            os.path.expanduser("~/.local/share/fonts")
        ]
    }
    
    def __init__(self):
        """初始化字体安装器"""
        self.system = platform.system()
        self.font_paths = self.SYSTEM_FONT_PATHS.get(self.system, [])
        
    def get_system_font_paths(self) -> List[str]:
        """
        获取系统字体路径列表
        
        返回:
            系统字体路径列表，只返回存在的路径
        """
        existing_paths = []
        for path in self.font_paths:
            if os.path.exists(path):
                existing_paths.append(path)
        return existing_paths
    
    def scan_system_fonts(self) -> Dict[str, List[str]]:
        """
        扫描系统中所有可用的字体文件
        
        返回:
            字典，键为字体路径，值为该路径下的字体文件列表
        """
        font_files = {}
        font_extensions = {'.ttf', '.otf', '.ttc', '.woff', '.woff2'}
        
        for font_path in self.get_system_font_paths():
            try:
                fonts_in_path = []
                for root, dirs, files in os.walk(font_path):
                    for file in files:
                        if Path(file).suffix.lower() in font_extensions:
                            fonts_in_path.append(os.path.join(root, file))
                
                if fonts_in_path:
                    font_files[font_path] = fonts_in_path
                    
            except (PermissionError, OSError) as e:
                print(f"警告：无法访问字体路径 {font_path}: {e}")
                continue
                
        return font_files
    
    def detect_chinese_fonts(self) -> List[Dict[str, str]]:
        """
        检测系统中已安装的中文字体
        
        返回:
            中文字体信息列表，每个元素包含字体名称、路径和类型
        """
        chinese_fonts = []
        chinese_keywords = [
            'simhei', 'simsun', 'kaiti', 'fangsong', 'yahei', 
            'wenquanyi', 'noto.*cjk', 'source.*han', 'cjk',
            '黑体', '宋体', '楷体', '仿宋', '微软雅黑'
        ]
        
        font_files = self.scan_system_fonts()
        
        for path, fonts in font_files.items():
            for font_file in fonts:
                font_name = os.path.basename(font_file).lower()
                
                # 检查是否包含中文关键词
                for keyword in chinese_keywords:
                    if keyword in font_name:
                        chinese_fonts.append({
                            'name': os.path.basename(font_file),
                            'path': font_file,
                            'type': 'system',
                            'keyword': keyword
                        })
                        break
        
        return chinese_fonts
    
    def check_font_installation_status(self) -> Dict[str, any]:
        """
        检查字体安装状态
        
        返回:
            包含详细状态信息的字典
        """
        status = {
            'system': self.system,
            'font_paths': self.get_system_font_paths(),
            'chinese_fonts': self.detect_chinese_fonts(),
            'font_count': 0,
            'recommendations': []
        }
        
        status['font_count'] = len(status['chinese_fonts'])
        
        # 生成建议
        if status['font_count'] == 0:
            status['recommendations'].append("系统中未检测到中文字体，建议安装字体")
            if self.system == "Linux":
                status['recommendations'].append("Linux用户可运行: sudo apt-get install fonts-wqy-zenhei")
            elif self.system == "Windows":
                status['recommendations'].append("Windows用户需要手动下载并安装中文字体")
        else:
            status['recommendations'].append("系统已安装中文字体")
            
        return status
    
    def install_font_linux(self, font_file: str, user_install: bool = True) -> bool:
        """
        在Linux系统上安装字体
        
        参数:
            font_file: 字体文件路径
            user_install: 是否仅对当前用户安装（默认True）
            
        返回:
            安装是否成功
        """
        try:
            if user_install:
                # 用户级安装
                font_dir = os.path.expanduser("~/.local/share/fonts")
                os.makedirs(font_dir, exist_ok=True)
            else:
                # 系统级安装（需要sudo权限）
                font_dir = "/usr/local/share/fonts"
                os.makedirs(font_dir, exist_ok=True)
            
            # 复制字体文件
            dest_path = os.path.join(font_dir, os.path.basename(font_file))
            shutil.copy2(font_file, dest_path)
            
            # 更新字体缓存
            subprocess.run(['fc-cache', '-fv'], check=True, capture_output=True)
            
            print(f"✓ 字体已安装到: {dest_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ 更新字体缓存失败: {e}")
            return False
        except Exception as e:
            print(f"✗ 安装字体失败: {e}")
            return False
    
    def install_font_windows(self, font_file: str) -> bool:
        """
        在Windows系统上安装字体
        
        参数:
            font_file: 字体文件路径
            
        返回:
            安装是否成功
        """
        try:
            import ctypes
            
            # Windows字体目录
            font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
            dest_path = os.path.join(font_dir, os.path.basename(font_file))
            
            # 复制字体文件
            shutil.copy2(font_file, dest_path)
            
            # 注册字体到系统
            ctypes.windll.gdi32.AddFontResourceW(dest_path)
            
            # 通知系统字体已更改
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, dest_path)
            
            print(f"✓ 字体已安装到: {dest_path}")
            return True
            
        except Exception as e:
            print(f"✗ 安装字体失败: {e}")
            return False
    
    def install_font_macos(self, font_file: str, user_install: bool = True) -> bool:
        """
        在macOS系统上安装字体
        
        参数:
            font_file: 字体文件路径
            user_install: 是否仅对当前用户安装（默认True）
            
        返回:
            安装是否成功
        """
        try:
            if user_install:
                font_dir = os.path.expanduser("~/Library/Fonts")
            else:
                font_dir = "/Library/Fonts"
                
            os.makedirs(font_dir, exist_ok=True)
            dest_path = os.path.join(font_dir, os.path.basename(font_file))
            
            # 复制字体文件
            shutil.copy2(font_file, dest_path)
            
            print(f"✓ 字体已安装到: {dest_path}")
            return True
            
        except Exception as e:
            print(f"✗ 安装字体失败: {e}")
            return False
    
    def download_font(self, font_key: str, dest_dir: Optional[str] = None) -> Optional[str]:
        """
        下载字体文件
        
        参数:
            font_key: 字体键名（如 'simhei'）
            dest_dir: 下载目录，如果为None则使用临时目录
            
        返回:
            下载的字体文件路径，失败返回None
        """
        if font_key not in self.FONT_DOWNLOADS:
            print(f"✗ 不支持的字体: {font_key}")
            return None
        
        font_info = self.FONT_DOWNLOADS[font_key]
        
        try:
            import urllib.request
            
            if dest_dir is None:
                dest_dir = tempfile.mkdtemp()
            else:
                os.makedirs(dest_dir, exist_ok=True)
            
            filename = font_info['name'] + '.ttf'
            dest_path = os.path.join(dest_dir, filename)
            
            print(f"正在下载字体 {font_info['description']}...")
            urllib.request.urlretrieve(font_info['url'], dest_path)
            
            print(f"✓ 字体下载完成: {dest_path}")
            return dest_path
            
        except Exception as e:
            print(f"✗ 下载字体失败: {e}")
            return None
    
    def auto_install_chinese_fonts(self) -> bool:
        """
        自动安装中文字体
        
        返回:
            安装是否成功
        """
        status = self.check_font_installation_status()
        
        if status['font_count'] > 0:
            print("✓ 系统中已存在中文字体，无需安装")
            return True
        
        print("系统中未检测到中文字体，开始自动安装...")
        
        # 根据系统选择安装策略
        if self.system == "Linux":
            try:
                # 尝试使用包管理器安装
                subprocess.run(['sudo', 'apt-get', 'update'], check=True, capture_output=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'fonts-wqy-zenhei'], 
                             check=True, capture_output=True)
                print("✓ 已通过apt-get安装文泉驿正黑字体")
                return True
            except subprocess.CalledProcessError:
                print("apt-get安装失败，尝试下载安装...")
        
        # 下载并安装字体
        for font_key in ['wqy-zenhei', 'simhei']:
            font_file = self.download_font(font_key)
            if font_file:
                success = False
                if self.system == "Linux":
                    success = self.install_font_linux(font_file)
                elif self.system == "Windows":
                    success = self.install_font_windows(font_file)
                elif self.system == "Darwin":
                    success = self.install_font_macos(font_file)
                
                if success:
                    return True
        
        print("✗ 自动安装失败，请手动安装中文字体")
        return False
    
    def get_installation_guide(self) -> str:
        """
        获取平台特定的字体安装指南
        
        返回:
            安装指南字符串
        """
        guide = f"\n{'='*50}\n"
        guide += f"{self.system} 系统字体安装指南\n"
        guide += f"{'='*50}\n"
        
        if self.system == "Linux":
            guide += """
方法1: 使用包管理器（推荐）
  sudo apt-get update
  sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei

方法2: 手动安装
  1. 下载字体文件（如SimHei.ttf）
  2. 复制到 ~/.local/share/fonts/ 或 /usr/local/share/fonts/
  3. 运行 fc-cache -fv 更新字体缓存

方法3: 使用本工具自动安装
  from utils.font_installer import FontInstaller
  installer = FontInstaller()
  installer.auto_install_chinese_fonts()
"""
        elif self.system == "Windows":
            guide += """
方法1: 手动安装（推荐）
  1. 下载字体文件（.ttf或.otf格式）
  2. 右键点击字体文件，选择"安装"
  3. 或者复制字体文件到 C:\\Windows\\Fonts\\ 目录

方法2: 使用设置应用
  1. 打开 Windows 设置 > 个性化 > 字体
  2. 拖拽字体文件到安装区域

注意: Windows系统需要重启Matplotlib才能识别新字体
"""
        elif self.system == "Darwin":
            guide += """
方法1: 用户级安装（推荐）
  1. 下载字体文件（.ttf或.otf格式）
  2. 双击字体文件，点击"安装字体"
  3. 或复制到 ~/Library/Fonts/ 目录

方法2: 系统级安装
  1. 复制字体文件到 /Library/Fonts/ 目录
  2. 需要管理员权限

注意: 安装后可能需要重启应用程序
"""
        
        return guide


def main():
    """
    主函数：演示字体安装器的使用
    """
    print("字体检测与安装工具")
    print("="*50)
    
    installer = FontInstaller()
    
    # 检查当前状态
    status = installer.check_font_installation_status()
    print(f"\n系统信息:")
    print(f"  操作系统: {status['system']}")
    print(f"  字体路径: {len(status['font_paths'])} 个")
    print(f"  中文字体: {status['font_count']} 个")
    
    if status['chinese_fonts']:
        print("\n检测到的中文字体:")
        for font in status['chinese_fonts'][:5]:  # 只显示前5个
            print(f"  - {font['name']} ({font['keyword']})")
        if len(status['chinese_fonts']) > 5:
            print(f"  ... 还有 {len(status['chinese_fonts']) - 5} 个字体")
    
    # 显示建议
    print("\n建议:")
    for rec in status['recommendations']:
        print(f"  {rec}")
    
    # 显示安装指南
    print(installer.get_installation_guide())
    
    # 询问是否自动安装
    if status['font_count'] == 0:
        try:
            response = input("是否尝试自动安装字体？(y/N): ").strip().lower()
            if response in ['y', 'yes', '是']:
                success = installer.auto_install_chinese_fonts()
                if success:
                    print("✓ 字体安装成功！")
                else:
                    print("✗ 字体安装失败，请参考上述指南手动安装")
        except KeyboardInterrupt:
            print("\n操作已取消")


if __name__ == "__main__":
    main()