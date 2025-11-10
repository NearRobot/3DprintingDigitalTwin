"""
Matplotlib缓存清理模块

提供Matplotlib字体缓存清理和重建功能。
解决因缓存导致的字体设置不生效问题。
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MatplotlibCacheCleaner:
    """
    Matplotlib缓存清理器
    
    专门用于清理和重建matplotlib的字体缓存，
    确保新安装的字体能被正确识别和使用。
    """
    
    def __init__(self):
        """初始化缓存清理器"""
        self.cache_dirs = self._find_cache_dirs()
        self.font_cache_files = []
        
    def _find_cache_dirs(self) -> List[str]:
        """
        查找matplotlib缓存目录
        
        返回:
            matplotlib缓存目录列表
        """
        cache_dirs = []
        
        try:
            import matplotlib
            # 获取matplotlib配置目录
            config_dir = matplotlib.get_configdir()
            cache_dir = os.path.join(config_dir, 'fontlist-v*.json')
            
            # 查找所有匹配的缓存文件
            import glob
            cache_files = glob.glob(cache_dir)
            
            for cache_file in cache_files:
                cache_dirs.append(os.path.dirname(cache_file))
                
        except Exception:
            # 如果无法通过matplotlib获取，尝试常见路径
            home = Path.home()
            possible_paths = [
                home / ".cache" / "matplotlib",
                home / ".matplotlib",
                tempfile.gettempdir() / "matplotlib",
            ]
            
            for path in possible_paths:
                if path.exists():
                    cache_dirs.append(str(path))
        
        return list(set(cache_dirs))  # 去重
    
    def get_cache_info(self) -> Dict[str, any]:
        """
        获取缓存信息
        
        返回:
            包含缓存详细信息的字典
        """
        info = {
            'cache_dirs': self.cache_dirs,
            'cache_files': [],
            'total_size': 0,
            'cache_count': 0,
            'recommendations': []
        }
        
        # 查找所有缓存文件
        for cache_dir in self.cache_dirs:
            try:
                for item in os.listdir(cache_dir):
                    item_path = os.path.join(cache_dir, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        info['cache_files'].append({
                            'name': item,
                            'path': item_path,
                            'size': size,
                            'size_mb': round(size / (1024 * 1024), 2)
                        })
                        info['total_size'] += size
                    elif os.path.isdir(item_path):
                        # 递归计算目录大小
                        dir_size = self._get_dir_size(item_path)
                        info['cache_files'].append({
                            'name': item,
                            'path': item_path,
                            'size': dir_size,
                            'size_mb': round(dir_size / (1024 * 1024), 2),
                            'is_dir': True
                        })
                        info['total_size'] += dir_size
                        
            except (PermissionError, OSError) as e:
                info['recommendations'].append(f"无法访问缓存目录 {cache_dir}: {e}")
        
        info['cache_count'] = len(info['cache_files'])
        info['total_size_mb'] = round(info['total_size'] / (1024 * 1024), 2)
        
        # 生成建议
        if info['cache_count'] > 0:
            info['recommendations'].append("建议清理matplotlib缓存以确保字体设置生效")
        else:
            info['recommendations'].append("未找到matplotlib缓存文件")
            
        return info
    
    def _get_dir_size(self, dir_path: str) -> int:
        """
        计算目录大小
        
        参数:
            dir_path: 目录路径
            
        返回:
            目录大小（字节）
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        return total_size
    
    def clear_font_cache(self, backup: bool = True) -> bool:
        """
        清理matplotlib字体缓存
        
        参数:
            backup: 是否创建备份（默认True）
            
        返回:
            清理是否成功
        """
        success = True
        cleared_files = []
        
        for cache_dir in self.cache_dirs:
            try:
                # 创建备份
                if backup:
                    backup_dir = cache_dir + "_backup_" + str(int(os.path.getmtime(cache_dir)))
                    if os.path.exists(cache_dir):
                        shutil.copytree(cache_dir, backup_dir)
                        print(f"✓ 已创建备份: {backup_dir}")
                
                # 清理字体相关缓存文件
                for item in os.listdir(cache_dir):
                    item_path = os.path.join(cache_dir, item)
                    
                    # 删除字体列表文件
                    if item.startswith('fontlist-') and item.endswith('.json'):
                        os.remove(item_path)
                        cleared_files.append(item_path)
                        print(f"✓ 已删除字体缓存: {item}")
                    
                    # 删除字体管理器缓存
                    elif item == 'fontManager.py':
                        os.remove(item_path)
                        cleared_files.append(item_path)
                        print(f"✓ 已删除字体管理器缓存: {item}")
                    
                    # 可选：删除整个缓存目录（谨慎操作）
                    elif item in ['ttf', 'afm', 'pdfcorefonts']:
                        item_full_path = os.path.join(cache_dir, item)
                        if os.path.isdir(item_full_path):
                            shutil.rmtree(item_full_path)
                            cleared_files.append(item_full_path)
                            print(f"✓ 已删除字体目录: {item}")
                            
            except (PermissionError, OSError) as e:
                print(f"✗ 清理缓存失败 {cache_dir}: {e}")
                success = False
        
        if cleared_files:
            print(f"✓ 共清理了 {len(cleared_files)} 个缓存文件")
        else:
            print("ℹ 未找到需要清理的字体缓存文件")
            
        return success
    
    def rebuild_font_cache(self, force_rebuild: bool = True) -> bool:
        """
        重建matplotlib字体缓存
        
        参数:
            force_rebuild: 是否强制重建（默认True）
            
        返回:
            重建是否成功
        """
        try:
            import matplotlib.font_manager as fm
            
            if force_rebuild:
                # 强制重建字体管理器
                print("正在重建matplotlib字体缓存...")
                fm._rebuild()
                print("✓ 字体缓存重建完成")
            else:
                # 只刷新字体列表
                print("正在刷新字体列表...")
                fm.fontManager.__init__()
                print("✓ 字体列表刷新完成")
            
            # 验证重建结果
            font_count = len(fm.fontManager.ttflist)
            print(f"✓ 当前已加载 {font_count} 个字体")
            
            return True
            
        except Exception as e:
            print(f"✗ 重建字体缓存失败: {e}")
            return False
    
    def verify_font_cache(self, font_name: Optional[str] = None) -> Dict[str, any]:
        """
        验证字体缓存状态
        
        参数:
            font_name: 要验证的特定字体名称，如果为None则验证所有中文字体
            
        返回:
            验证结果字典
        """
        result = {
            'success': False,
            'font_found': False,
            'available_fonts': [],
            'chinese_fonts': [],
            'target_font': None,
            'cache_status': 'unknown',
            'recommendations': []
        }
        
        try:
            import matplotlib.font_manager as fm
            
            # 获取所有可用字体
            all_fonts = [f.name for f in fm.fontManager.ttflist]
            result['available_fonts'] = list(set(all_fonts))
            result['cache_status'] = 'loaded'
            
            # 查找中文字体
            chinese_keywords = [
                'simhei', 'simsun', 'kaiti', 'fangsong', 'yahei', 
                'wenquanyi', 'noto.*cjk', 'source.*han', 'cjk'
            ]
            
            for font in result['available_fonts']:
                font_lower = font.lower()
                for keyword in chinese_keywords:
                    if keyword in font_lower:
                        result['chinese_fonts'].append(font)
                        break
            
            # 验证特定字体
            if font_name:
                result['target_font'] = font_name
                if font_name in result['available_fonts']:
                    result['font_found'] = True
                    result['recommendations'].append(f"字体 '{font_name}' 可用")
                else:
                    result['recommendations'].append(f"字体 '{font_name}' 不可用")
            
            # 生成建议
            if result['chinese_fonts']:
                result['recommendations'].append(f"找到 {len(result['chinese_fonts'])} 个中文字体")
                result['success'] = True
            else:
                result['recommendations'].append("未找到中文字体，建议安装字体或清理缓存")
            
            # 检查缓存文件状态
            cache_info = self.get_cache_info()
            if cache_info['cache_count'] == 0:
                result['recommendations'].append("缓存已清理，matplotlib将重新扫描字体")
            
        except Exception as e:
            result['cache_status'] = 'error'
            result['recommendations'].append(f"验证过程出错: {e}")
        
        return result
    
    def full_reset(self, backup: bool = True) -> bool:
        """
        完整重置matplotlib字体系统
        
        参数:
            backup: 是否创建备份（默认True）
            
        返回:
            重置是否成功
        """
        print("开始完整重置matplotlib字体系统...")
        
        # 1. 清理缓存
        print("\n步骤 1/3: 清理字体缓存")
        success1 = self.clear_font_cache(backup)
        
        # 2. 重建缓存
        print("\n步骤 2/3: 重建字体缓存")
        success2 = self.rebuild_font_cache(force_rebuild=True)
        
        # 3. 验证结果
        print("\n步骤 3/3: 验证重置结果")
        verification = self.verify_font_cache()
        
        if verification['success']:
            print("✓ matplotlib字体系统重置成功")
            if verification['chinese_fonts']:
                print(f"✓ 识别到 {len(verification['chinese_fonts'])} 个中文字体")
            return True
        else:
            print("✗ matplotlib字体系统重置失败")
            for rec in verification['recommendations']:
                print(f"  - {rec}")
            return False


def main():
    """
    主函数：演示缓存清理器的使用
    """
    print("Matplotlib缓存清理工具")
    print("="*50)
    
    cleaner = MatplotlibCacheCleaner()
    
    # 显示缓存信息
    cache_info = cleaner.get_cache_info()
    print(f"\n缓存信息:")
    print(f"  缓存目录: {len(cache_info['cache_dirs'])} 个")
    print(f"  缓存文件: {cache_info['cache_count']} 个")
    print(f"  总大小: {cache_info['total_size_mb']} MB")
    
    if cache_info['cache_files']:
        print("\n主要缓存文件:")
        for file_info in cache_info['cache_files'][:5]:  # 只显示前5个
            file_type = "目录" if file_info.get('is_dir') else "文件"
            print(f"  - {file_info['name']} ({file_type}, {file_info['size_mb']} MB)")
    
    # 显示建议
    print("\n建议:")
    for rec in cache_info['recommendations']:
        print(f"  {rec}")
    
    # 验证当前字体状态
    print("\n当前字体状态:")
    verification = cleaner.verify_font_cache()
    print(f"  可用字体总数: {len(verification['available_fonts'])}")
    print(f"  中文字体数量: {len(verification['chinese_fonts'])}")
    
    if verification['chinese_fonts']:
        print("  中文字体列表:")
        for font in verification['chinese_fonts'][:5]:
            print(f"    - {font}")
        if len(verification['chinese_fonts']) > 5:
            print(f"    ... 还有 {len(verification['chinese_fonts']) - 5} 个字体")
    
    # 询问是否执行清理
    try:
        response = input("\n是否清理matplotlib缓存？(y/N): ").strip().lower()
        if response in ['y', 'yes', '是']:
            success = cleaner.full_reset(backup=True)
            if success:
                print("\n✓ 缓存清理完成！matplotlib将重新扫描系统字体。")
            else:
                print("\n✗ 缓存清理失败，请检查权限设置。")
        else:
            print("\n操作已取消。")
    except KeyboardInterrupt:
        print("\n\n操作已取消。")


if __name__ == "__main__":
    main()