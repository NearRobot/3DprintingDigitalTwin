"""
依赖安装验证脚本

用于验证所有必需的依赖库是否正确安装。
"""

import sys
from typing import Dict, List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """检查 Python 版本"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version >= required_version:
        return True, f"Python {current_version[0]}.{current_version[1]} ✓"
    else:
        return False, f"Python {current_version[0]}.{current_version[1]} (需要 >= 3.8) ✗"


def check_dependencies() -> Dict[str, Tuple[bool, str]]:
    """
    检查所有依赖库
    
    返回:
        字典，包含每个库的检查结果
    """
    results = {}
    
    # 核心依赖列表
    dependencies = [
        'numpy',
        'scipy',
        'matplotlib',
        'pybullet',
        'gymnasium',
        'stable_baselines3',
        'torch',
        'yaml',
        'pandas',
        'seaborn',
    ]
    
    for package in dependencies:
        try:
            # 尝试导入
            if package == 'yaml':
                import yaml
                version = yaml.__version__
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
            
            results[package] = (True, f"{version} ✓")
        except ImportError as e:
            results[package] = (False, f"未安装 ✗")
        except Exception as e:
            results[package] = (False, f"导入错误: {str(e)} ✗")
    
    return results


def check_project_structure() -> Dict[str, bool]:
    """检查项目目录结构"""
    import os
    
    required_dirs = [
        'config',
        'sim',
        'control',
        'rl',
        'matlab',
        'tests',
        'docs',
        'examples',
    ]
    
    results = {}
    for directory in required_dirs:
        results[directory] = os.path.isdir(directory)
    
    return results


def check_config_files() -> Dict[str, bool]:
    """检查配置文件"""
    import os
    
    required_files = [
        'config/default_config.yaml',
        'README.md',
        'CONTRIBUTING.md',
        'requirements.txt',
        'environment.yml',
        'pyproject.toml',
    ]
    
    results = {}
    for file in required_files:
        results[file] = os.path.isfile(file)
    
    return results


def test_config_module():
    """测试配置模块功能"""
    try:
        from config import ConfigLoader, get_default_config
        
        # 测试默认配置
        default_config = get_default_config()
        assert 'simulation' in default_config
        assert 'control' in default_config
        
        # 测试配置加载器
        loader = ConfigLoader()
        timestep = loader.get('simulation.timestep')
        assert timestep is not None
        
        return True, "配置模块正常 ✓"
    except Exception as e:
        return False, f"配置模块错误: {str(e)} ✗"


def test_logger_module():
    """测试日志模块功能"""
    try:
        from config.logger import Logger
        
        # 创建临时日志记录器
        logger = Logger(
            name='test',
            level='INFO',
            log_dir='logs',
            console_output=False,
            file_output=False
        )
        
        # 测试日志记录
        logger.info('测试日志')
        
        return True, "日志模块正常 ✓"
    except Exception as e:
        return False, f"日志模块错误: {str(e)} ✗"


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  依赖安装验证")
    print("="*60)
    
    all_passed = True
    
    # 检查 Python 版本
    print_section("Python 版本")
    passed, message = check_python_version()
    print(f"  {message}")
    all_passed = all_passed and passed
    
    # 检查依赖库
    print_section("依赖库检查")
    dep_results = check_dependencies()
    for package, (passed, message) in dep_results.items():
        print(f"  {package:20s} : {message}")
        all_passed = all_passed and passed
    
    # 检查项目结构
    print_section("项目目录结构")
    dir_results = check_project_structure()
    for directory, exists in dir_results.items():
        status = "✓" if exists else "✗"
        print(f"  {directory:20s} : {status}")
        all_passed = all_passed and exists
    
    # 检查配置文件
    print_section("配置文件")
    file_results = check_config_files()
    for file, exists in file_results.items():
        status = "✓" if exists else "✗"
        print(f"  {file:40s} : {status}")
        all_passed = all_passed and exists
    
    # 测试模块功能
    print_section("模块功能测试")
    
    config_passed, config_msg = test_config_module()
    print(f"  配置模块: {config_msg}")
    all_passed = all_passed and config_passed
    
    logger_passed, logger_msg = test_logger_module()
    print(f"  日志模块: {logger_msg}")
    all_passed = all_passed and logger_passed
    
    # 输出总结
    print("\n" + "="*60)
    if all_passed:
        print("  ✓ 所有检查通过！环境配置完成。")
        print("  您可以开始使用本项目进行开发。")
    else:
        print("  ✗ 部分检查失败，请根据上述信息解决问题。")
        print("  提示：运行 'pip install -e .' 或")
        print("       'conda env create -f environment.yml' 安装依赖。")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
