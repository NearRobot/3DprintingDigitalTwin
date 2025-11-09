# MATLAB/Simscape 与 PyBullet 联合验证流程

## 概述

本文档描述如何使用 MATLAB/Simscape 和 PyBullet 进行联合仿真验证，确保控制算法在不同仿真平台上的一致性和可靠性。

## 为什么需要联合验证

### MATLAB/Simscape 的优势

- **精确建模**：提供丰富的物理建模库和高精度求解器
- **成熟工具**：完善的控制系统设计和分析工具
- **行业标准**：工业界广泛使用，结果可信度高
- **可视化**：强大的数据分析和可视化能力

### PyBullet 的优势

- **快速仿真**：高效的物理引擎，适合大规模训练
- **开源免费**：无需商业许可，便于分享和部署
- **强化学习集成**：与 Gymnasium 无缝对接
- **GPU 加速**：支持并行仿真，提高训练效率

### 联合验证的价值

1. **交叉验证**：两个独立平台的结果互相验证，提高可信度
2. **优势互补**：结合两者优势，扬长避短
3. **分阶段开发**：MATLAB 快速原型，PyBullet 大规模训练
4. **风险降低**：避免单一平台的局限性

## 联合验证架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     控制算法                            │
│          (Python 实现，两个平台共享)                    │
└────────────────┬───────────────┬────────────────────────┘
                 │               │
        ┌────────▼──────┐   ┌───▼──────────┐
        │   MATLAB      │   │   PyBullet   │
        │   Simscape    │   │   Simulator  │
        │   Simulator   │   │              │
        └───────┬───────┘   └──────┬───────┘
                │                  │
                └────────┬─────────┘
                         ▼
                 ┌───────────────┐
                 │  结果对比分析 │
                 │  与验证报告   │
                 └───────────────┘
```

### 数据流

```
初始条件 → MATLAB 仿真 → 状态轨迹 1
        ↘                          ↘
          PyBullet 仿真 → 状态轨迹 2 → 对比分析 → 验证结论
```

## 实施步骤

### 步骤 1：建立 MATLAB 模型

#### 1.1 创建 Simscape 模型

在 MATLAB/Simulink 中创建物理系统模型：

```matlab
% 示例：简单的质量-弹簧-阻尼系统
% 文件：matlab/models/mass_spring_damper.slx

% 系统参数
m = 1.0;   % 质量 (kg)
k = 10.0;  % 弹簧刚度 (N/m)
c = 0.5;   % 阻尼系数 (N·s/m)

% 状态空间表示
A = [0, 1; -k/m, -c/m];
B = [0; 1/m];
C = [1, 0];
D = 0;

sys = ss(A, B, C, D);
```

#### 1.2 导出接口函数

```matlab
% 文件：matlab/interface/simulate_model.m

function [t, x, u] = simulate_model(x0, u_func, T, dt)
    % 运行 Simscape 模型仿真
    %
    % 参数:
    %   x0: 初始状态向量
    %   u_func: 控制输入函数句柄
    %   T: 仿真时间
    %   dt: 时间步长
    %
    % 返回:
    %   t: 时间序列
    %   x: 状态轨迹
    %   u: 控制输入序列
    
    % 设置仿真参数
    options = simset('Solver', 'ode45', 'FixedStep', dt);
    
    % 运行仿真
    [t, x, u] = sim('mass_spring_damper', [0 T], options);
end
```

### 步骤 2：建立 PyBullet 模型

#### 2.1 创建仿真环境

```python
# 文件：sim/mass_spring_damper_env.py

import numpy as np
import pybullet as p
import pybullet_data


class MassSpringDamperEnv:
    """
    质量-弹簧-阻尼系统的 PyBullet 仿真环境
    
    与 MATLAB 模型保持一致的物理参数
    """
    
    def __init__(self, mass=1.0, stiffness=10.0, damping=0.5):
        """
        初始化仿真环境
        
        参数:
            mass: 质量 (kg)
            stiffness: 弹簧刚度 (N/m)
            damping: 阻尼系数 (N·s/m)
        """
        self.mass = mass
        self.stiffness = stiffness
        self.damping = damping
        
        # 连接物理引擎
        self.client = p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81)
        
        # 创建物体
        self._create_objects()
    
    def _create_objects(self):
        """创建仿真对象"""
        # 创建质量块
        collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.1, 0.1, 0.1])
        self.mass_id = p.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=collision_shape,
            basePosition=[0, 0, 1],
        )
    
    def step(self, control_force, dt=0.01):
        """
        执行一步仿真
        
        参数:
            control_force: 控制力
            dt: 时间步长
        
        返回:
            state: 当前状态 [位置, 速度]
        """
        # 应用控制力
        p.applyExternalForce(
            self.mass_id, -1, [0, 0, control_force],
            [0, 0, 0], p.WORLD_FRAME
        )
        
        # 仿真一步
        p.stepSimulation()
        
        # 获取状态
        pos, _ = p.getBasePositionAndOrientation(self.mass_id)
        vel, _ = p.getBaseVelocity(self.mass_id)
        
        return np.array([pos[2], vel[2]])
    
    def reset(self, initial_state):
        """
        重置环境
        
        参数:
            initial_state: 初始状态 [位置, 速度]
        """
        p.resetBasePositionAndOrientation(
            self.mass_id,
            [0, 0, initial_state[0]],
            [0, 0, 0, 1]
        )
        p.resetBaseVelocity(
            self.mass_id,
            [0, 0, initial_state[1]],
            [0, 0, 0]
        )
```

### 步骤 3：统一控制算法

#### 3.1 Python 控制器实现

```python
# 文件：control/pid_controller.py

class PIDController:
    """
    PID 控制器
    
    可在 MATLAB 和 PyBullet 中共享使用
    """
    
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0
    
    def compute(self, error, dt):
        """
        计算控制输出
        
        参数:
            error: 当前误差
            dt: 时间步长
        
        返回:
            控制输出
        """
        # 比例项
        p_term = self.kp * error
        
        # 积分项
        self.integral += error * dt
        i_term = self.ki * self.integral
        
        # 微分项
        d_term = self.kd * (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error
        
        return p_term + i_term + d_term
    
    def reset(self):
        """重置控制器状态"""
        self.integral = 0.0
        self.prev_error = 0.0
```

#### 3.2 MATLAB 包装器

```matlab
% 文件：matlab/interface/python_controller.m

function u = python_controller(error, dt, controller)
    % 调用 Python 控制器
    %
    % 参数:
    %   error: 误差值
    %   dt: 时间步长
    %   controller: Python 控制器对象
    %
    % 返回:
    %   u: 控制输出
    
    u = double(controller.compute(error, dt));
end
```

### 步骤 4：执行联合验证

#### 4.1 验证脚本

```python
# 文件：tests/test_joint_validation.py

import numpy as np
import matplotlib.pyplot as plt
from control.pid_controller import PIDController
from sim.mass_spring_damper_env import MassSpringDamperEnv


def run_pybullet_simulation(controller, initial_state, duration, dt):
    """
    运行 PyBullet 仿真
    
    返回:
        时间序列、状态轨迹、控制输入
    """
    env = MassSpringDamperEnv()
    env.reset(initial_state)
    
    t_list = []
    x_list = []
    u_list = []
    
    t = 0
    while t < duration:
        # 计算误差（假设目标为 0）
        state = env.step(0, dt)  # 先获取当前状态
        error = 0 - state[0]
        
        # 计算控制输入
        u = controller.compute(error, dt)
        
        # 记录数据
        t_list.append(t)
        x_list.append(state)
        u_list.append(u)
        
        # 执行控制
        env.step(u, dt)
        
        t += dt
    
    return np.array(t_list), np.array(x_list), np.array(u_list)


def run_matlab_simulation(controller, initial_state, duration, dt):
    """
    运行 MATLAB 仿真
    
    需要安装 MATLAB Engine for Python
    """
    import matlab.engine
    
    eng = matlab.engine.start_matlab()
    
    # 调用 MATLAB 函数
    # 这里简化为占位实现
    # 实际需要将 Python 控制器传递给 MATLAB
    
    eng.quit()
    
    # 返回结果
    return t_matlab, x_matlab, u_matlab


def compare_results(t1, x1, u1, t2, x2, u2):
    """
    对比两个仿真结果
    
    返回:
        差异统计信息
    """
    # 插值对齐时间序列
    from scipy.interpolate import interp1d
    
    # 计算状态差异
    x2_interp = interp1d(t2, x2, axis=0, fill_value='extrapolate')
    x2_aligned = x2_interp(t1)
    
    state_diff = np.abs(x1 - x2_aligned)
    
    # 统计信息
    stats = {
        'mean_position_error': np.mean(state_diff[:, 0]),
        'max_position_error': np.max(state_diff[:, 0]),
        'mean_velocity_error': np.mean(state_diff[:, 1]),
        'max_velocity_error': np.max(state_diff[:, 1]),
    }
    
    return stats


def plot_comparison(t1, x1, t2, x2):
    """绘制对比图"""
    plt.figure(figsize=(12, 8))
    
    # 位置对比
    plt.subplot(2, 1, 1)
    plt.plot(t1, x1[:, 0], label='PyBullet', linewidth=2)
    plt.plot(t2, x2[:, 0], label='MATLAB', linewidth=2, linestyle='--')
    plt.xlabel('时间 (s)')
    plt.ylabel('位置 (m)')
    plt.legend()
    plt.grid(True)
    plt.title('位置轨迹对比')
    
    # 速度对比
    plt.subplot(2, 1, 2)
    plt.plot(t1, x1[:, 1], label='PyBullet', linewidth=2)
    plt.plot(t2, x2[:, 1], label='MATLAB', linewidth=2, linestyle='--')
    plt.xlabel('时间 (s)')
    plt.ylabel('速度 (m/s)')
    plt.legend()
    plt.grid(True)
    plt.title('速度轨迹对比')
    
    plt.tight_layout()
    plt.savefig('validation_comparison.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    # 设置参数
    initial_state = [1.0, 0.0]  # 初始位置和速度
    duration = 10.0
    dt = 0.01
    
    # 创建控制器
    controller = PIDController(kp=10.0, ki=1.0, kd=2.0)
    
    # 运行 PyBullet 仿真
    print("运行 PyBullet 仿真...")
    t_pb, x_pb, u_pb = run_pybullet_simulation(
        controller, initial_state, duration, dt
    )
    
    # 重置控制器
    controller.reset()
    
    # 运行 MATLAB 仿真（如果可用）
    # print("运行 MATLAB 仿真...")
    # t_ml, x_ml, u_ml = run_matlab_simulation(
    #     controller, initial_state, duration, dt
    # )
    
    # 对比结果
    # stats = compare_results(t_pb, x_pb, u_pb, t_ml, x_ml, u_ml)
    # print("验证结果：")
    # for key, value in stats.items():
    #     print(f"  {key}: {value:.6f}")
    
    # 绘制对比图
    # plot_comparison(t_pb, x_pb, t_ml, x_ml)
```

### 步骤 5：结果分析

#### 5.1 验证标准

联合验证通过的标准：

1. **位置误差** < 1% 最大位移
2. **速度误差** < 5% 最大速度
3. **控制输入误差** < 5% 最大控制量
4. **能量守恒误差** < 2%

#### 5.2 误差来源分析

可能的误差来源：

- **数值积分方法差异**：MATLAB 和 PyBullet 使用不同的求解器
- **时间步长**：确保两者使用相同的时间步长
- **物理参数**：检查所有参数是否完全一致
- **浮点精度**：累积的数值误差

#### 5.3 校准方法

如果误差过大，采取以下措施：

1. 减小时间步长
2. 使用更高精度的求解器
3. 调整物理引擎参数
4. 检查坐标系和单位一致性

## 最佳实践

### 1. 版本控制

- 记录 MATLAB 版本和工具箱版本
- 记录 PyBullet 和依赖库版本
- 使用固定的随机种子确保可重复性

### 2. 参数管理

- 使用统一的配置文件管理物理参数
- 两个平台从同一配置文件读取参数
- 避免硬编码参数

### 3. 测试策略

- 从简单系统开始验证
- 逐步增加系统复杂度
- 建立自动化测试流程

### 4. 文档记录

- 记录每次验证的参数设置
- 保存验证结果和对比图
- 建立验证日志数据库

## 常见问题

### Q1: MATLAB Engine for Python 安装失败

**解决方案**：
```bash
cd "matlabroot/extern/engines/python"
python setup.py install
```

### Q2: PyBullet 仿真不稳定

**解决方案**：
- 减小时间步长
- 增加求解器迭代次数
- 调整接触参数

### Q3: 结果差异过大

**解决方案**：
- 检查初始条件是否完全一致
- 验证控制器状态是否正确重置
- 确认坐标系定义一致

## 工具和资源

### MATLAB 相关

- [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)
- [Simscape Multibody](https://www.mathworks.com/products/simscape-multibody.html)
- [Control System Toolbox](https://www.mathworks.com/products/control.html)

### PyBullet 相关

- [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/)
- [PyBullet GitHub](https://github.com/bulletphysics/bullet3)

## 下一步

完成基础联合验证后，可以：

1. 扩展到更复杂的系统（机械臂、移动机器人等）
2. 实现实时数据同步
3. 添加硬件在环测试
4. 开发自动化验证流水线
