"""
配置模块测试

测试配置加载器和日志管理器的功能。
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from config import ConfigLoader, get_default_config
from config.logger import Logger


class TestConfigLoader:
    """配置加载器测试类"""
    
    def test_default_config(self):
        """测试默认配置加载"""
        config = get_default_config()
        
        assert 'simulation' in config
        assert 'control' in config
        assert 'logging' in config
        assert 'rl' in config
    
    def test_config_loader_initialization(self):
        """测试配置加载器初始化"""
        loader = ConfigLoader()
        
        assert loader.config is not None
        assert isinstance(loader.config, dict)
    
    def test_get_nested_config(self):
        """测试获取嵌套配置项"""
        loader = ConfigLoader()
        
        # 测试嵌套键访问
        timestep = loader.get('simulation.timestep')
        assert timestep is not None
        
        kp = loader.get('control.pid.kp')
        assert kp is not None
    
    def test_get_with_default(self):
        """测试带默认值的配置获取"""
        loader = ConfigLoader()
        
        # 不存在的键应返回默认值
        value = loader.get('nonexistent.key', default=42)
        assert value == 42
    
    def test_set_config(self):
        """测试设置配置项"""
        loader = ConfigLoader()
        
        # 设置简单值
        loader.set('test.value', 100)
        assert loader.get('test.value') == 100
        
        # 设置嵌套值
        loader.set('test.nested.value', 'hello')
        assert loader.get('test.nested.value') == 'hello'
    
    def test_load_from_file(self):
        """测试从文件加载配置"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'test': {
                    'value': 123,
                    'name': 'test_config'
                }
            }
            yaml.safe_dump(config_data, f)
            temp_file = f.name
        
        try:
            # 加载配置
            loader = ConfigLoader(temp_file)
            
            assert loader.get('test.value') == 123
            assert loader.get('test.name') == 'test_config'
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    def test_save_config(self):
        """测试保存配置到文件"""
        loader = ConfigLoader()
        loader.set('test.save', 'saved_value')
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_file = f.name
        
        try:
            # 保存配置
            loader.save(temp_file)
            
            # 重新加载验证
            with open(temp_file, 'r', encoding='utf-8') as f:
                loaded_data = yaml.safe_load(f)
            
            assert 'test' in loaded_data
            assert loaded_data['test']['save'] == 'saved_value'
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    def test_to_dict(self):
        """测试转换为字典"""
        loader = ConfigLoader()
        config_dict = loader.to_dict()
        
        assert isinstance(config_dict, dict)
        assert 'simulation' in config_dict


class TestLogger:
    """日志管理器测试类"""
    
    def test_logger_initialization(self):
        """测试日志管理器初始化"""
        logger = Logger(
            name='test_logger',
            level='INFO',
            console_output=False,
            file_output=False
        )
        
        assert logger.logger is not None
        assert logger.logger.name == 'test_logger'
    
    def test_logger_methods(self):
        """测试日志记录方法"""
        logger = Logger(
            name='test_methods',
            level='DEBUG',
            console_output=False,
            file_output=False
        )
        
        # 测试各级别日志方法（不应抛出异常）
        logger.debug('调试信息')
        logger.info('信息')
        logger.warning('警告')
        logger.error('错误')
        logger.critical('严重错误')
    
    def test_logger_file_output(self):
        """测试日志文件输出"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = Logger(
                name='test_file',
                level='INFO',
                log_dir=temp_dir,
                console_output=False,
                file_output=True
            )
            
            logger.info('测试日志输出')
            
            # 检查日志文件是否创建
            log_files = list(Path(temp_dir).glob('*.log'))
            assert len(log_files) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
