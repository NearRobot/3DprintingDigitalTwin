"""
配置加载器

负责加载和解析 YAML 配置文件，提供配置访问接口。
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigLoader:
    """
    配置加载器类
    
    支持从 YAML 文件加载配置，并提供便捷的配置访问方法。
    
    属性:
        config (dict): 配置字典
        config_path (Path): 配置文件路径
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置加载器
        
        参数:
            config_path: 配置文件路径，如果为 None 则加载默认配置
        """
        self.config_path = Path(config_path) if config_path else None
        self.config: Dict[str, Any] = {}
        
        if config_path:
            self.load(config_path)
        else:
            self.config = get_default_config()
    
    def load(self, config_path: str) -> None:
        """
        从文件加载配置
        
        参数:
            config_path: 配置文件路径
        
        异常:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML 格式错误
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.config_path = config_path
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        支持使用点号分隔的键访问嵌套配置，例如 'simulation.timestep'
        
        参数:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值，当键不存在时返回
        
        返回:
            配置值或默认值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        
        支持使用点号分隔的键设置嵌套配置。
        
        参数:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        # 遍历到倒数第二个键
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置最后一个键的值
        config[keys[-1]] = value
    
    def save(self, output_path: Optional[str] = None) -> None:
        """
        保存配置到文件
        
        参数:
            output_path: 输出文件路径，如果为 None 则保存到原文件
        """
        path = Path(output_path) if output_path else self.config_path
        
        if not path:
            raise ValueError("必须指定输出路径")
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.config, f, allow_unicode=True, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        返回配置字典
        
        返回:
            配置字典的副本
        """
        return self.config.copy()


def load_config(config_path: str) -> Dict[str, Any]:
    """
    加载配置文件的便捷函数
    
    参数:
        config_path: 配置文件路径
    
    返回:
        配置字典
    """
    loader = ConfigLoader(config_path)
    return loader.to_dict()


def get_default_config() -> Dict[str, Any]:
    """
    获取默认配置
    
    返回:
        默认配置字典
    """
    return {
        'simulation': {
            'timestep': 0.01,
            'duration': 10.0,
            'gravity': [0, 0, -9.81],
            'render': False,
        },
        'control': {
            'type': 'pid',
            'pid': {
                'kp': 1.0,
                'ki': 0.1,
                'kd': 0.01,
            },
        },
        'logging': {
            'level': 'INFO',
            'log_dir': 'logs',
            'save_frequency': 100,
        },
        'rl': {
            'algorithm': 'PPO',
            'total_timesteps': 100000,
            'learning_rate': 0.0003,
            'n_steps': 2048,
            'batch_size': 64,
            'policy': 'MlpPolicy',
        },
    }
