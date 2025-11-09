# API 参考文档

本文档提供项目主要模块和类的 API 参考。

## 配置管理模块 (config)

### ConfigLoader

配置文件加载和管理类。

```python
from config import ConfigLoader

# 创建配置加载器
config = ConfigLoader('config/default_config.yaml')

# 获取配置项
timestep = config.get('simulation.timestep')
kp = config.get('control.pid.kp', default=1.0)

# 设置配置项
config.set('simulation.duration', 20.0)

# 保存配置
config.save('config/custom_config.yaml')
```

#### 方法

- `__init__(config_path: Optional[str] = None)`: 初始化配置加载器
- `load(config_path: str) -> None`: 从文件加载配置
- `get(key: str, default: Any = None) -> Any`: 获取配置项（支持嵌套键）
- `set(key: str, value: Any) -> None`: 设置配置项
- `save(output_path: Optional[str] = None) -> None`: 保存配置到文件
- `to_dict() -> Dict[str, Any]`: 返回配置字典

### Logger

日志管理类。

```python
from config.logger import get_logger, setup_logger

# 设置日志记录器
logger = setup_logger(name='my-app', level='INFO', log_dir='logs')

# 记录日志
logger.info('仿真开始')
logger.warning('检测到异常值')
logger.error('仿真失败')
```

#### 方法

- `debug(message: str)`: 记录 DEBUG 级别日志
- `info(message: str)`: 记录 INFO 级别日志
- `warning(message: str)`: 记录 WARNING 级别日志
- `error(message: str)`: 记录 ERROR 级别日志
- `critical(message: str)`: 记录 CRITICAL 级别日志
- `exception(message: str)`: 记录异常信息（包含堆栈跟踪）

## 仿真模块 (sim)

### 基础仿真环境（待实现）

```python
from sim import SimulationEnvironment

# 创建仿真环境
env = SimulationEnvironment(config='config/default_config.yaml')

# 重置环境
state = env.reset()

# 执行仿真步骤
next_state, reward, done, info = env.step(action)

# 关闭环境
env.close()
```

## 控制模块 (control)

### PID 控制器（待实现）

```python
from control import PIDController

# 创建 PID 控制器
controller = PIDController(kp=1.0, ki=0.1, kd=0.01)

# 计算控制输出
error = setpoint - current_value
control_output = controller.compute(error, dt=0.01)

# 重置控制器
controller.reset()
```

### LQR 控制器（待实现）

```python
from control import LQRController

# 创建 LQR 控制器
controller = LQRController(A, B, Q, R)

# 计算控制输入
u = controller.compute(state)
```

### MPC 控制器（待实现）

```python
from control import MPCController

# 创建 MPC 控制器
controller = MPCController(
    A, B, Q, R,
    horizon=10,
    constraints={'u_min': -10, 'u_max': 10}
)

# 计算控制输入
u = controller.compute(state, reference)
```

## 强化学习模块 (rl)

### RL 训练器（待实现）

```python
from rl import RLTrainer

# 创建训练器
trainer = RLTrainer(
    env=env,
    algorithm='PPO',
    policy='MlpPolicy',
    config='config/default_config.yaml'
)

# 训练模型
trainer.train(total_timesteps=100000)

# 保存模型
trainer.save('models/ppo_controller')

# 加载模型
trainer.load('models/ppo_controller')

# 评估模型
mean_reward, std_reward = trainer.evaluate(n_episodes=10)
```

## 工具函数

### 数据记录（待实现）

```python
from utils import DataLogger

# 创建数据记录器
data_logger = DataLogger(save_dir='data')

# 记录数据
data_logger.log('state', state, timestamp=t)
data_logger.log('action', action, timestamp=t)

# 保存数据
data_logger.save('simulation_results.pkl')
```

### 可视化（待实现）

```python
from utils import plot_results

# 绘制结果
plot_results(
    time=t_array,
    states=x_array,
    actions=u_array,
    save_path='results/simulation_plot.png'
)
```

## 配置文件格式

### YAML 配置示例

```yaml
# 仿真配置
simulation:
  timestep: 0.01
  duration: 10.0
  gravity: [0, 0, -9.81]
  render: false

# 控制器配置
control:
  type: pid
  pid:
    kp: 1.0
    ki: 0.1
    kd: 0.01

# 强化学习配置
rl:
  algorithm: PPO
  total_timesteps: 100000
  learning_rate: 0.0003
```

## 注意事项

1. 所有配置文件使用 UTF-8 编码
2. 路径使用相对路径或绝对路径
3. 日志文件自动按时间戳命名
4. 模型文件使用 `.zip` 或 `.pkl` 格式

## 更新日志

- **v0.1.0** (当前版本): 初始 API 设计，配置和日志模块已实现
- 后续版本将添加控制和强化学习模块的完整实现
