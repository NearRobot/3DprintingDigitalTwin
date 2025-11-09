# 贡献指南

感谢您对本项目的关注！本文档将帮助您了解如何为项目做出贡献。

## 行为准则

- 尊重所有贡献者
- 提供建设性的反馈
- 专注于对项目最有利的方向

## 开发流程

### 1. 准备开发环境

```bash
# 克隆仓库
git clone <repository-url>
cd <project-directory>

# 创建开发环境
conda env create -f environment.yml
conda activate control-sim

# 安装开发依赖
pip install -e ".[dev]"
```

### 2. 创建功能分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name

# 或修复 bug
git checkout -b fix/bug-description
```

### 3. 开发与测试

```bash
# 运行测试
pytest tests/ -v

# 检查代码覆盖率
pytest --cov=. tests/

# 代码格式化（如果配置）
black .
isort .
```

### 4. 提交更改

```bash
# 添加更改
git add .

# 提交（使用中文描述）
git commit -m "功能: 添加新的控制器实现"
```

## 代码规范

### 注释规范

**所有代码注释和文档字符串必须使用中文。**

#### 模块注释

```python
"""
模块说明：PID 控制器实现

本模块提供标准 PID 控制器的实现，支持参数调优和抗积分饱和。
"""
```

#### 函数注释

```python
def calculate_control_output(state, setpoint, controller_params):
    """
    计算控制器输出
    
    参数:
        state (np.ndarray): 当前系统状态向量
        setpoint (float): 目标设定值
        controller_params (dict): 控制器参数字典
            - kp: 比例增益
            - ki: 积分增益
            - kd: 微分增益
    
    返回:
        float: 控制输出值
    
    异常:
        ValueError: 当参数不合法时抛出
    
    示例:
        >>> params = {'kp': 1.0, 'ki': 0.1, 'kd': 0.01}
        >>> output = calculate_control_output(state, 10.0, params)
    """
    pass
```

#### 类注释

```python
class PIDController:
    """
    PID 控制器类
    
    实现标准的比例-积分-微分控制器，包含抗积分饱和功能。
    
    属性:
        kp (float): 比例增益
        ki (float): 积分增益
        kd (float): 微分增益
        integral (float): 积分累积值
        prev_error (float): 上一次误差值
    
    示例:
        >>> controller = PIDController(kp=1.0, ki=0.1, kd=0.01)
        >>> output = controller.compute(error=5.0, dt=0.01)
    """
    pass
```

#### 行内注释

```python
# 计算误差
error = setpoint - current_value

# 更新积分项（带抗饱和处理）
self.integral = np.clip(self.integral + error * dt, -100, 100)

# 计算微分项
derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
```

### 命名规范

- **变量名**：使用英文小写加下划线（snake_case）
  - 示例：`control_output`, `sample_time`, `max_velocity`
- **函数名**：使用英文小写加下划线（snake_case）
  - 示例：`calculate_pid()`, `update_state()`, `run_simulation()`
- **类名**：使用驼峰命名（PascalCase）
  - 示例：`PIDController`, `SimulationEnvironment`, `RLAgent`
- **常量**：使用英文大写加下划线
  - 示例：`MAX_ITERATIONS`, `DEFAULT_TIMESTEP`, `PI`

### 代码风格

- 遵循 PEP 8 规范
- 每行最多 100 字符
- 使用 4 个空格缩进
- 函数之间空两行
- 类方法之间空一行

## 提交信息规范

### 提交类型

- **功能**: 新增功能
- **修复**: Bug 修复
- **文档**: 文档更新
- **样式**: 代码格式调整（不影响功能）
- **重构**: 代码重构
- **性能**: 性能优化
- **测试**: 测试相关
- **构建**: 构建系统或依赖更新
- **配置**: 配置文件更新

### 提交格式

```
类型: 简短描述（不超过 50 字符）

详细说明（如果需要）：
- 更改的原因
- 解决的问题
- 相关的 issue 编号

相关 Issue: #123
```

### 示例

```
功能: 添加 LQR 控制器实现

实现了线性二次调节器（LQR）控制器：
- 支持连续和离散系统
- 自动求解 Riccati 方程
- 提供增益矩阵计算接口

相关 Issue: #45
```

## 测试规范

### 单元测试

- 所有新功能必须包含单元测试
- 测试覆盖率应保持在 80% 以上
- 测试文件命名：`test_<module_name>.py`
- 测试函数命名：`test_<function_name>_<scenario>()`

```python
def test_pid_controller_basic_functionality():
    """测试 PID 控制器基本功能"""
    controller = PIDController(kp=1.0, ki=0.1, kd=0.01)
    output = controller.compute(error=10.0, dt=0.01)
    assert isinstance(output, float)
    assert output > 0  # 正误差应产生正输出
```

### 集成测试

- 测试模块间的交互
- 验证完整的工作流程
- 放在 `tests/integration/` 目录

## 文档规范

### 文档位置

- 概念性文档：`docs/`
- API 文档：通过代码注释自动生成
- 示例代码：`examples/`

### 文档内容

- 使用中文撰写
- 包含代码示例
- 提供清晰的步骤说明
- 添加必要的图表和公式

## Pull Request 流程

1. **确保所有测试通过**
   ```bash
   pytest tests/ -v
   ```

2. **更新相关文档**
   - 如果添加新功能，更新 README.md
   - 如果修改 API，更新文档注释

3. **创建 Pull Request**
   - 使用清晰的标题（中文）
   - 在描述中说明更改内容
   - 引用相关的 issue

4. **代码审查**
   - 响应审查意见
   - 进行必要的修改
   - 保持讨论专业和建设性

5. **合并**
   - 等待维护者批准
   - 确保没有冲突
   - 合并后删除功能分支

## 报告问题

### Bug 报告

使用 issue 模板报告 bug，包含以下信息：

- **环境信息**：操作系统、Python 版本、依赖版本
- **重现步骤**：详细的重现步骤
- **预期行为**：应该发生什么
- **实际行为**：实际发生了什么
- **错误信息**：完整的错误堆栈
- **相关代码**：最小可重现示例

### 功能请求

- 清晰描述建议的功能
- 说明使用场景和价值
- 提供可能的实现思路

## 获取帮助

如果您在贡献过程中遇到问题：

1. 查阅项目文档
2. 搜索现有的 issues
3. 创建新的 issue 提问

## 许可证

贡献的代码将遵循项目的许可证。

---

再次感谢您的贡献！
