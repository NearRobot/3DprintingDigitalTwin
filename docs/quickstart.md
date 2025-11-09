# 快速开始指南

本指南帮助您快速搭建开发环境并运行第一个示例。

## 环境要求

- Python 3.8 或更高版本
- （可选）Anaconda/Miniconda
- （可选）MATLAB R2020a 或更高版本（用于联合仿真）

## 安装步骤

### 方法一：使用 Conda（推荐）

```bash
# 1. 克隆仓库
git clone <repository-url>
cd <project-directory>

# 2. 创建 conda 环境
conda env create -f environment.yml

# 3. 激活环境
conda activate control-sim

# 4. 验证安装
python examples/verify_install.py
```

### 方法二：使用 pip + 虚拟环境

```bash
# 1. 克隆仓库
git clone <repository-url>
cd <project-directory>

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 4. 安装依赖
pip install -e .

# 5. 验证安装
python examples/verify_install.py
```

## 验证安装

运行验证脚本检查所有依赖是否正确安装：

```bash
python examples/verify_install.py
```

预期输出：
```
============================================================
  依赖安装验证
============================================================

Python 版本
============================================================
  Python 3.x ✓

依赖库检查
============================================================
  numpy                : x.x.x ✓
  scipy                : x.x.x ✓
  matplotlib           : x.x.x ✓
  ...

项目目录结构
============================================================
  config               : ✓
  sim                  : ✓
  control              : ✓
  ...

配置文件
============================================================
  config/default_config.yaml               : ✓
  README.md                                : ✓
  ...

模块功能测试
============================================================
  配置模块: 配置模块正常 ✓
  日志模块: 日志模块正常 ✓

============================================================
  ✓ 所有检查通过！环境配置完成。
  您可以开始使用本项目进行开发。
============================================================
```

## 运行第一个示例

```bash
# 运行简单仿真示例
python examples/simple_simulation.py
```

这将：
1. 加载配置文件
2. 创建一个质量-弹簧-阻尼系统
3. 使用 PID 控制器进行控制
4. 绘制仿真结果图

查看生成的图像：`examples/simulation_results.png`

查看日志文件：`logs/simple-simulation_*.log`

## 自定义配置

### 修改仿真参数

编辑 `config/default_config.yaml`:

```yaml
simulation:
  timestep: 0.01      # 修改时间步长
  duration: 20.0      # 修改仿真时长

control:
  pid:
    kp: 2.0          # 修改 PID 参数
    ki: 0.2
    kd: 0.02
```

### 使用自定义配置

```python
from config import ConfigLoader

# 加载自定义配置
config = ConfigLoader('config/my_config.yaml')

# 使用配置
timestep = config.get('simulation.timestep')
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 或使用脚本
./run_tests.sh
```

## 常见问题

### Q: 安装依赖时出现错误

**A:** 尝试升级 pip：
```bash
pip install --upgrade pip
```

如果使用 conda，尝试：
```bash
conda update conda
```

### Q: PyBullet 安装失败

**A:** 某些系统可能需要额外的依赖：
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# macOS
xcode-select --install
```

### Q: 如何启用 GPU 支持（PyTorch）

**A:** 根据您的 CUDA 版本安装对应的 PyTorch：
```bash
# CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# CPU only
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Q: MATLAB Engine for Python 安装失败

**A:** 
1. 确保 MATLAB 已安装
2. 找到 MATLAB 根目录
3. 运行：
   ```bash
   cd "matlabroot/extern/engines/python"
   python setup.py install
   ```

## 下一步

- 阅读 [研究路径概述](research_roadmap.md)
- 学习 [MATLAB 与 PyBullet 联合验证](joint_validation.md)
- 查看 [API 参考文档](api_reference.md)
- 参与 [贡献](../CONTRIBUTING.md)

## 获取帮助

如果遇到问题：

1. 检查 [常见问题](#常见问题)
2. 查看项目 [Issues](../../issues)
3. 提交新的 Issue 描述问题

---

祝您使用愉快！
