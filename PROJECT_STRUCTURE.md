# 项目结构说明

本文档描述项目的完整目录结构和文件说明。

## 根目录文件

```
.
├── .gitignore              # Git 忽略文件配置
├── LICENSE                 # MIT 许可证
├── README.md               # 项目主说明文档
├── CONTRIBUTING.md         # 贡献指南
├── pyproject.toml          # Python 项目配置（推荐方式）
├── setup.py                # Setup.py（向后兼容）
├── requirements.txt        # pip 依赖列表
├── environment.yml         # Conda 环境配置
└── run_tests.sh            # 测试运行脚本
```

## 目录结构

### config/ - 配置管理

```
config/
├── __init__.py             # 模块初始化
├── config_loader.py        # 配置加载器实现
├── logger.py               # 日志管理器实现
└── default_config.yaml     # 默认配置文件
```

**功能**：
- 统一的配置文件管理
- 日志记录功能
- 支持嵌套键访问
- YAML 格式配置

### sim/ - 仿真环境

```
sim/
└── __init__.py             # 模块初始化（占位）
```

**规划功能**：
- PyBullet 仿真环境
- Gymnasium 接口封装
- 自定义物理环境

### control/ - 控制算法

```
control/
└── __init__.py             # 模块初始化（占位）
```

**规划功能**：
- PID 控制器
- LQR 控制器
- MPC 控制器
- 其他控制算法

### rl/ - 强化学习

```
rl/
└── __init__.py             # 模块初始化（占位）
```

**规划功能**：
- Stable-Baselines3 训练器
- 自定义环境包装器
- 训练和评估工具

### matlab/ - MATLAB 相关

```
matlab/
└── README.md               # MATLAB 使用说明
```

**规划功能**：
- Simscape 模型文件
- MATLAB 脚本
- Python-MATLAB 接口
- 联合仿真工具

### tests/ - 测试

```
tests/
├── README.md               # 测试说明
└── test_config.py          # 配置模块测试
```

**功能**：
- 单元测试
- 集成测试
- 使用 pytest 框架

### examples/ - 示例

```
examples/
├── README.md               # 示例说明
├── verify_install.py       # 依赖验证脚本
└── simple_simulation.py    # 简单仿真示例
```

**功能**：
- 演示基本用法
- 验证安装
- 提供学习材料

### docs/ - 文档

```
docs/
├── quickstart.md           # 快速开始指南
├── research_roadmap.md     # 研究路径概述
├── joint_validation.md     # 联合验证流程
└── api_reference.md        # API 参考文档
```

**内容**：
- 使用指南
- 技术文档
- API 参考
- 开发指南

## 文件说明

### 核心配置文件

#### pyproject.toml
- Python 项目元数据
- 依赖声明
- 工具配置（black, isort, pytest, mypy）

#### environment.yml
- Conda 环境配置
- 包含所有依赖及版本
- 支持跨平台

#### requirements.txt
- pip 依赖列表
- 简化的依赖声明

### 配置模块

#### config_loader.py
主要类：`ConfigLoader`

功能：
- 加载 YAML 配置文件
- 嵌套键访问（例如：`simulation.timestep`）
- 配置保存

#### logger.py
主要类：`Logger`

功能：
- 统一的日志接口
- 支持控制台和文件输出
- 可配置日志级别

#### default_config.yaml
包含：
- 仿真参数
- 控制器参数
- 日志配置
- 强化学习参数
- PyBullet 配置
- MATLAB 集成配置

### 示例脚本

#### verify_install.py
功能：
- 检查 Python 版本
- 验证依赖安装
- 检查项目结构
- 测试模块功能

#### simple_simulation.py
演示：
- 配置文件使用
- 日志系统使用
- 简单系统仿真
- PID 控制器实现
- 结果可视化

### 文档

#### quickstart.md
内容：
- 环境安装步骤
- 验证方法
- 运行第一个示例
- 常见问题

#### research_roadmap.md
内容：
- 项目背景和目标
- 研究阶段规划
- 技术路线图
- 评估指标
- 风险应对

#### joint_validation.md
内容：
- 联合验证架构
- 实施步骤
- MATLAB-PyBullet 对接
- 验证标准
- 最佳实践

#### api_reference.md
内容：
- 模块 API 说明
- 使用示例
- 配置格式

## 开发工作流

### 1. 环境配置
```bash
conda env create -f environment.yml
conda activate control-sim
```

### 2. 开发
```bash
# 编辑代码
vim control/pid_controller.py

# 运行示例测试
python examples/simple_simulation.py
```

### 3. 测试
```bash
# 运行测试
pytest tests/ -v

# 或使用脚本
./run_tests.sh
```

### 4. 提交
```bash
git add .
git commit -m "功能: 添加新功能"
git push
```

## 扩展指南

### 添加新的控制器

1. 在 `control/` 目录创建文件
2. 实现控制器类
3. 添加测试到 `tests/`
4. 更新文档
5. 添加示例到 `examples/`

### 添加新的仿真环境

1. 在 `sim/` 目录创建环境类
2. 实现 Gymnasium 接口
3. 添加配置到 `default_config.yaml`
4. 编写测试
5. 创建使用示例

### 添加文档

1. 在 `docs/` 目录创建 Markdown 文件
2. 使用中文撰写
3. 包含代码示例
4. 更新主 README.md

## 依赖管理

### 添加新依赖

1. 更新 `pyproject.toml` 的 `dependencies` 列表
2. 更新 `requirements.txt`
3. 更新 `environment.yml`
4. 重新安装：`pip install -e .`

### 版本固定

生产环境建议固定版本：
```
numpy==1.21.0
scipy==1.7.0
```

开发环境可以使用范围：
```
numpy>=1.21.0
scipy>=1.7.0
```

## 日志和数据

### 生成的文件

项目运行时会生成：

- `logs/` - 日志文件
- `models/` - 训练的模型
- `tensorboard/` - TensorBoard 日志
- `results/` - 仿真结果
- `examples/*.png` - 示例图像

这些目录已在 `.gitignore` 中配置，不会提交到 Git。

## 最佳实践

1. **所有代码注释使用中文**
2. **遵循 PEP 8 代码风格**
3. **为新功能编写测试**
4. **更新相关文档**
5. **使用有意义的提交信息**

## 版本历史

- **v0.1.0** - 初始项目框架
  - 配置管理模块
  - 日志系统
  - 基础文档
  - 示例脚本

---

更新日期：2024-11
