"""
简单仿真示例

演示如何使用配置文件和日志系统运行基础仿真。
这是一个占位示例，展示项目的基本使用模式。
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from config import ConfigLoader
from config.logger import setup_logger


class SimpleSystem:
    """
    简单的一维质量-弹簧-阻尼系统
    
    状态方程：
        m * x'' + c * x' + k * x = u
    
    其中：
        m: 质量
        c: 阻尼系数
        k: 弹簧刚度
        u: 外力（控制输入）
    """
    
    def __init__(self, mass=1.0, damping=0.5, stiffness=10.0):
        """
        初始化系统
        
        参数:
            mass: 质量 (kg)
            damping: 阻尼系数 (N·s/m)
            stiffness: 弹簧刚度 (N/m)
        """
        self.m = mass
        self.c = damping
        self.k = stiffness
        
        # 状态 [位置, 速度]
        self.state = np.array([0.0, 0.0])
    
    def reset(self, initial_state=None):
        """
        重置系统状态
        
        参数:
            initial_state: 初始状态 [位置, 速度]
        """
        if initial_state is None:
            self.state = np.array([1.0, 0.0])  # 默认初始位置为 1m
        else:
            self.state = np.array(initial_state)
        
        return self.state.copy()
    
    def step(self, control_input, dt):
        """
        执行一步仿真
        
        参数:
            control_input: 控制输入（力）
            dt: 时间步长
        
        返回:
            新状态
        """
        # 当前状态
        x, v = self.state
        
        # 加速度：a = (u - c*v - k*x) / m
        acceleration = (control_input - self.c * v - self.k * x) / self.m
        
        # 使用欧拉法更新状态
        new_v = v + acceleration * dt
        new_x = x + new_v * dt
        
        self.state = np.array([new_x, new_v])
        
        return self.state.copy()


class SimplePIDController:
    """
    简单的 PID 控制器实现
    """
    
    def __init__(self, kp, ki, kd):
        """
        初始化控制器
        
        参数:
            kp: 比例增益
            ki: 积分增益
            kd: 微分增益
        """
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
        # 积分项（带简单的抗饱和）
        self.integral = np.clip(self.integral + error * dt, -10, 10)
        
        # 微分项
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error
        
        # PID 输出
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        
        return output
    
    def reset(self):
        """重置控制器状态"""
        self.integral = 0.0
        self.prev_error = 0.0


def run_simulation(config_path='config/default_config.yaml'):
    """
    运行仿真主函数
    
    参数:
        config_path: 配置文件路径
    """
    # 加载配置
    config = ConfigLoader(config_path)
    
    # 设置日志
    logger = setup_logger(
        name='simple-simulation',
        level=config.get('logging.level', 'INFO'),
        log_dir=config.get('logging.log_dir', 'logs')
    )
    
    logger.info("="*60)
    logger.info("开始简单仿真示例")
    logger.info("="*60)
    
    # 获取仿真参数
    timestep = config.get('simulation.timestep', 0.01)
    duration = config.get('simulation.duration', 10.0)
    
    logger.info(f"仿真参数: 时间步长={timestep}s, 持续时间={duration}s")
    
    # 创建系统
    system = SimpleSystem(mass=1.0, damping=0.5, stiffness=10.0)
    initial_state = [1.0, 0.0]  # 初始位置 1m，速度 0
    system.reset(initial_state)
    
    logger.info(f"系统初始状态: 位置={initial_state[0]}m, 速度={initial_state[1]}m/s")
    
    # 创建控制器
    kp = config.get('control.pid.kp', 1.0)
    ki = config.get('control.pid.ki', 0.1)
    kd = config.get('control.pid.kd', 0.01)
    controller = SimplePIDController(kp, ki, kd)
    
    logger.info(f"PID 控制器参数: Kp={kp}, Ki={ki}, Kd={kd}")
    
    # 目标位置
    setpoint = 0.0
    logger.info(f"控制目标: {setpoint}m")
    
    # 仿真循环
    num_steps = int(duration / timestep)
    
    # 数据记录
    time_history = []
    position_history = []
    velocity_history = []
    control_history = []
    error_history = []
    
    logger.info(f"开始仿真，总步数: {num_steps}")
    
    for step in range(num_steps):
        t = step * timestep
        
        # 计算误差
        error = setpoint - system.state[0]
        
        # 计算控制输入
        control_input = controller.compute(error, timestep)
        
        # 执行仿真步骤
        state = system.step(control_input, timestep)
        
        # 记录数据
        time_history.append(t)
        position_history.append(state[0])
        velocity_history.append(state[1])
        control_history.append(control_input)
        error_history.append(error)
        
        # 定期输出日志
        if step % 500 == 0:
            logger.info(
                f"步骤 {step}/{num_steps}: "
                f"位置={state[0]:.4f}m, 速度={state[1]:.4f}m/s, "
                f"控制输入={control_input:.4f}N, 误差={error:.4f}m"
            )
    
    logger.info("仿真完成")
    
    # 转换为 numpy 数组
    time_history = np.array(time_history)
    position_history = np.array(position_history)
    velocity_history = np.array(velocity_history)
    control_history = np.array(control_history)
    error_history = np.array(error_history)
    
    # 计算性能指标
    settling_time = calculate_settling_time(time_history, error_history)
    max_overshoot = np.max(np.abs(position_history - setpoint))
    steady_state_error = np.mean(np.abs(error_history[-100:]))
    
    logger.info("="*60)
    logger.info("性能指标:")
    logger.info(f"  调节时间: {settling_time:.2f}s")
    logger.info(f"  最大超调: {max_overshoot:.4f}m")
    logger.info(f"  稳态误差: {steady_state_error:.6f}m")
    logger.info("="*60)
    
    # 绘制结果
    plot_results(
        time_history,
        position_history,
        velocity_history,
        control_history,
        error_history,
        setpoint
    )
    
    logger.info("结果图已保存到 examples/simulation_results.png")
    logger.info("仿真结束")


def calculate_settling_time(time, error, threshold=0.02):
    """
    计算调节时间（2% 准则）
    
    参数:
        time: 时间序列
        error: 误差序列
        threshold: 误差阈值
    
    返回:
        调节时间
    """
    # 找到误差小于阈值的时刻
    settled_indices = np.where(np.abs(error) < threshold)[0]
    
    if len(settled_indices) == 0:
        return time[-1]  # 未达到稳定
    
    # 找到最后一次超过阈值后的时间
    for i in range(len(settled_indices) - 1, 0, -1):
        if settled_indices[i] - settled_indices[i-1] > 1:
            return time[settled_indices[i]]
    
    return time[settled_indices[0]]


def plot_results(time, position, velocity, control, error, setpoint):
    """
    绘制仿真结果
    
    参数:
        time: 时间序列
        position: 位置序列
        velocity: 速度序列
        control: 控制输入序列
        error: 误差序列
        setpoint: 设定值
    """
    plt.figure(figsize=(14, 10))
    
    # 位置曲线
    plt.subplot(2, 2, 1)
    plt.plot(time, position, 'b-', linewidth=2, label='位置')
    plt.axhline(y=setpoint, color='r', linestyle='--', label='设定值')
    plt.xlabel('时间 (s)')
    plt.ylabel('位置 (m)')
    plt.title('位置响应')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 速度曲线
    plt.subplot(2, 2, 2)
    plt.plot(time, velocity, 'g-', linewidth=2)
    plt.xlabel('时间 (s)')
    plt.ylabel('速度 (m/s)')
    plt.title('速度响应')
    plt.grid(True, alpha=0.3)
    
    # 控制输入
    plt.subplot(2, 2, 3)
    plt.plot(time, control, 'orange', linewidth=2)
    plt.xlabel('时间 (s)')
    plt.ylabel('控制力 (N)')
    plt.title('控制输入')
    plt.grid(True, alpha=0.3)
    
    # 误差曲线
    plt.subplot(2, 2, 4)
    plt.plot(time, error, 'purple', linewidth=2)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.xlabel('时间 (s)')
    plt.ylabel('误差 (m)')
    plt.title('跟踪误差')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图像
    output_dir = Path('examples')
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'simulation_results.png', dpi=300, bbox_inches='tight')
    
    # 显示图像（如果在交互环境中）
    try:
        plt.show()
    except:
        pass  # 非交互环境下跳过


if __name__ == '__main__':
    try:
        run_simulation()
    except Exception as e:
        print(f"仿真过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
