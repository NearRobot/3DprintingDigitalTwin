# 测试目录

本目录包含项目的单元测试和集成测试。

## 测试结构

```
tests/
├── test_config.py          # 配置模块测试
├── test_control.py         # 控制器测试
├── test_simulation.py      # 仿真环境测试
├── test_rl.py             # 强化学习测试
└── integration/           # 集成测试
    └── test_joint_validation.py
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_config.py -v

# 运行带覆盖率报告的测试
pytest --cov=. tests/

# 运行特定测试函数
pytest tests/test_config.py::test_config_loader -v
```

## 编写测试

所有测试函数应遵循命名规范：`test_<功能>_<场景>()`

示例：
```python
def test_pid_controller_basic_functionality():
    """测试 PID 控制器基本功能"""
    # 测试代码
    pass

def test_config_loader_with_invalid_file():
    """测试配置加载器处理无效文件"""
    # 测试代码
    pass
```
