# 主动控制与仿真研究平台

## 项目简介

本项目旨在研究从被动滤波到主动控制的控制系统优化方法。通过结合 MATLAB/Simscape 的精确建模能力与 PyBullet 物理引擎的高效仿真，实现控制算法的快速验证和强化学习训练。

### 主要研究方向

- **被动滤波分析**：基于传统控制理论的滤波器设计与优化
- **主动控制策略**：包括 PID、LQR、MPC 等现代控制方法
- **强化学习控制**：利用 Stable-Baselines3 训练智能控制器
- **联合验证**：MATLAB/Simscape 与 PyBullet 的协同仿真验证

## 快速开始

请查看 [快速开始指南](docs/quickstart.md) 了解如何快速搭建开发环境。

## 目录结构

```
.
├── config/          # 配置文件目录
├── control/         # 控制算法实现
├── docs/            # 项目文档
├── examples/        # 示例脚本
├── matlab/          # MATLAB/Simscape 模型与脚本
├── rl/              # 强化学习相关代码
├── sim/             # PyBullet 仿真环境
├── tests/           # 单元测试
├── README.md        # 项目说明
├── CONTRIBUTING.md  # 贡献指南
├── pyproject.toml   # Python 项目配置
├── requirements.txt # Python 依赖列表
└── environment.yml  # Conda 环境配置
```

## 环境配置

### 方法一：使用 Conda（推荐）

```bash
# 创建并激活 conda 环境
conda env create -f environment.yml
conda activate control-sim

# 验证安装
python examples/verify_install.py
```

### 方法二：使用 pip

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 用户使用: venv\Scripts\activate

# 安装依赖
pip install -e .

# 验证安装
python examples/verify_install.py
```

### 核心依赖

- **Python >= 3.8**
- **PyBullet**：物理仿真引擎
- **Gymnasium**：强化学习环境接口
- **NumPy**：数值计算
- **SciPy**：科学计算
- **Stable-Baselines3**：强化学习算法库
- **Matplotlib**：数据可视化
- **PyYAML**：配置文件解析

## 快速开始

### 1. 运行示例仿真

```bash
# 激活环境后运行
python examples/simple_simulation.py
```

### 2. 查看配置示例

```bash
# 查看默认配置
cat config/default_config.yaml
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_config.py -v
```

## 开发规范

### 代码注释规范

**重要：本项目所有代码注释必须使用中文。**

```python
# 正确示例
def calculate_pid(error, kp, ki, kd):
    """
    计算 PID 控制器输出
    
    参数:
        error: 当前误差值
        kp: 比例增益
        ki: 积分增益
        kd: 微分增益
    
    返回:
        控制输出值
    """
    pass

# 错误示例（不要使用英文注释）
# Calculate PID output - ❌ 禁止
```

### 提交规范

- 提交信息使用中文描述
- 遵循常规提交格式：`类型: 简短描述`
- 详细说明请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

## 文档

详细文档请查看 [docs/](docs/) 目录：

- [快速开始指南](docs/quickstart.md)
- [研究路径概述](docs/research_roadmap.md)
- [MATLAB 与 PyBullet 联合验证流程](docs/joint_validation.md)
- [API 文档](docs/api_reference.md)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。
