# 示例目录

本目录包含项目的示例脚本和演示代码。

## 可用示例

### 1. 依赖验证脚本

**文件**: `verify_install.py`

验证所有依赖是否正确安装。

```bash
python examples/verify_install.py
```

### 2. 简单仿真示例

**文件**: `simple_simulation.py`

演示一个简单的质量-弹簧-阻尼系统的 PID 控制仿真。

```bash
python examples/simple_simulation.py
```

这个示例展示了：
- 如何使用配置文件
- 如何使用日志系统
- 基础的控制系统仿真
- 结果可视化

### 3. PyBullet 基础示例（待添加）

演示如何使用 PyBullet 创建仿真环境。

### 4. 强化学习训练示例（待添加）

演示如何使用 Stable-Baselines3 训练控制策略。

## 运行示例的前提条件

确保已安装所有依赖：

```bash
# 使用 pip
pip install -e .

# 或使用 conda
conda env create -f environment.yml
conda activate control-sim
```

## 自定义示例

您可以复制现有示例并根据需要修改：

1. 复制示例文件
2. 修改配置参数
3. 调整控制器参数
4. 运行并观察结果

## 输出文件

示例脚本可能会生成以下文件：

- `*.png`: 结果图像
- `*.log`: 日志文件（保存在 logs/ 目录）
- `*.pkl`: 数据文件

这些文件已在 `.gitignore` 中配置为不提交到版本控制。
