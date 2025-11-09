# MATLAB 目录

本目录包含 MATLAB/Simscape 模型和相关脚本。

## 目录结构

```
matlab/
├── models/              # Simscape 模型文件 (.slx)
├── scripts/             # MATLAB 脚本文件 (.m)
├── interface/           # Python-MATLAB 接口
└── utils/               # 工具函数
```

## MATLAB Engine for Python

### 安装

```bash
# 找到 MATLAB 安装路径
cd "matlabroot/extern/engines/python"

# 安装 MATLAB Engine
python setup.py install
```

### 使用示例

```python
import matlab.engine

# 启动 MATLAB 引擎
eng = matlab.engine.start_matlab()

# 调用 MATLAB 函数
result = eng.sqrt(4.0)

# 关闭引擎
eng.quit()
```

## 模型开发指南

1. 所有模型文件使用中文注释
2. 模型参数应可配置（使用 MATLAB 工作区变量）
3. 提供模型验证脚本
4. 记录模型的物理假设和限制

## 联合仿真

参考文档：[MATLAB 与 PyBullet 联合验证流程](../docs/joint_validation.md)
