"""
中文绘图演示脚本

展示如何使用 utils.plot_config 模块配置 Matplotlib 中文显示。
演示内容包括：
- 中文标题
- 中文坐标轴标签
- 中文图例
- 中文注释
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# 添加项目根目录到 Python 路径，这必须在其他导入前进行
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 在 utils 可用后再导入
from utils import (  # noqa: E402
    get_font_config_info,
    list_available_chinese_fonts,
    setup_chinese_font,
)


def demo_basic_plot():
    """
    演示基础的中文绘图

    创建一个简单的折线图，包含中文标题、轴标签和图例。
    """
    print("=" * 50)
    print("演示 1: 基础中文绘图")
    print("=" * 50)

    # 配置中文字体
    font_name = setup_chinese_font()
    print(f"✓ 已配置字体: {font_name}")

    # 打印当前字体配置信息
    config_info = get_font_config_info()
    print("✓ 当前字体配置:")
    for key, value in config_info.items():
        print(f"  - {key}: {value}")

    # 创建数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, y1, "b-", label="正弦函数", linewidth=2)
    ax.plot(x, y2, "r--", label="余弦函数", linewidth=2)

    # 设置中文标题和标签
    ax.set_title("三角函数示例图", fontsize=16, fontweight="bold")
    ax.set_xlabel("X轴（弧度）", fontsize=12)
    ax.set_ylabel("Y轴（函数值）", fontsize=12)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    # 添加中文注释
    max_sin_idx = np.argmax(y1)
    ax.annotate(
        "最大值",
        xy=(x[max_sin_idx], y1[max_sin_idx]),
        xytext=(x[max_sin_idx] + 1, y1[max_sin_idx] + 0.3),
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=10,
    )

    # 保存图表
    output_path = project_root / "outputs" / "demo_basic_plot.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"✓ 图表已保存: {output_path}")

    plt.close()


def demo_multi_subplot():
    """
    演示多子图的中文绘图

    创建一个包含多个子图的图表，每个子图都带有中文标签。
    """
    print("\n" + "=" * 50)
    print("演示 2: 多子图中文绘图")
    print("=" * 50)

    # 配置中文字体
    setup_chinese_font()

    # 创建数据
    x = np.linspace(0, 2 * np.pi, 100)

    # 创建多子图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("多个三角函数的图表展示", fontsize=16, fontweight="bold")

    # 第一个子图：正弦函数
    axes[0, 0].plot(x, np.sin(x), "b-", linewidth=2)
    axes[0, 0].set_title("正弦函数", fontsize=12)
    axes[0, 0].set_xlabel("自变量")
    axes[0, 0].set_ylabel("函数值")
    axes[0, 0].grid(True, alpha=0.3)

    # 第二个子图：余弦函数
    axes[0, 1].plot(x, np.cos(x), "r-", linewidth=2)
    axes[0, 1].set_title("余弦函数", fontsize=12)
    axes[0, 1].set_xlabel("自变量")
    axes[0, 1].set_ylabel("函数值")
    axes[0, 1].grid(True, alpha=0.3)

    # 第三个子图：正切函数
    y_tan = np.tan(x)
    # 限制 y 值范围以便显示
    y_tan = np.clip(y_tan, -5, 5)
    axes[1, 0].plot(x, y_tan, "g-", linewidth=2)
    axes[1, 0].set_title("正切函数（限制范围）", fontsize=12)
    axes[1, 0].set_xlabel("自变量")
    axes[1, 0].set_ylabel("函数值")
    axes[1, 0].grid(True, alpha=0.3)

    # 第四个子图：柱状图
    categories = ["类别A", "类别B", "类别C", "类别D", "类别E"]
    values = np.random.randint(10, 100, size=5)
    axes[1, 1].bar(categories, values, color=["blue", "green", "red", "orange", "purple"])
    axes[1, 1].set_title("分类数据柱状图", fontsize=12)
    axes[1, 1].set_ylabel("数值")
    axes[1, 1].tick_params(axis="x", rotation=45)

    plt.tight_layout()

    # 保存图表
    output_path = project_root / "outputs" / "demo_multi_subplot.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"✓ 图表已保存: {output_path}")

    plt.close()


def demo_scatter_plot():
    """
    演示散点图的中文绘图

    创建一个散点图，展示数据点和中文标签。
    """
    print("\n" + "=" * 50)
    print("演示 3: 散点图中文绘图")
    print("=" * 50)

    # 配置中文字体
    setup_chinese_font()

    # 生成随机数据
    np.random.seed(42)
    n_points = 100
    x_data = np.random.randn(n_points)
    y_data = 2 * x_data + np.random.randn(n_points)
    colors = np.random.rand(n_points)
    sizes = np.random.randint(50, 300, n_points)

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        x_data,
        y_data,
        c=colors,
        s=sizes,
        alpha=0.6,
        cmap="viridis",
        edgecolors="black",
        linewidth=0.5,
    )

    # 设置标题和标签
    ax.set_title("数据点分布散点图", fontsize=14, fontweight="bold")
    ax.set_xlabel("横坐标数据", fontsize=12)
    ax.set_ylabel("纵坐标数据", fontsize=12)

    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("数据密度", fontsize=11)

    # 添加网格
    ax.grid(True, alpha=0.3)

    # 保存图表
    output_path = project_root / "outputs" / "demo_scatter_plot.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"✓ 图表已保存: {output_path}")

    plt.close()


def demo_chinese_text():
    """
    演示中文文本显示

    创建一个展示各种中文文本元素的图表。
    """
    print("\n" + "=" * 50)
    print("演示 4: 中文文本显示")
    print("=" * 50)

    # 配置中文字体
    setup_chinese_font()

    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 8))

    # 创建示例数据
    categories = ["一月", "二月", "三月", "四月", "五月", "六月"]
    values1 = [10, 24, 36, 18, 7, 28]
    values2 = [20, 14, 26, 28, 17, 32]

    x = np.arange(len(categories))
    width = 0.35

    # 创建柱状图
    bars1 = ax.bar(x - width / 2, values1, width, label="部门A", color="skyblue")
    bars2 = ax.bar(x + width / 2, values2, width, label="部门B", color="lightcoral")

    # 设置标题和标签
    ax.set_title("每月业绩对比统计", fontsize=16, fontweight="bold")
    ax.set_xlabel("月份", fontsize=12)
    ax.set_ylabel("业绩值（单位：万元）", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    # 在柱子上添加数值标签
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

    add_value_labels(bars1)
    add_value_labels(bars2)

    # 添加文本注释
    ax.text(
        0.5,
        0.95,
        "数据说明：单位为万元，数据来自2024年统计",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="center",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.tight_layout()

    # 保存图表
    output_path = project_root / "outputs" / "demo_chinese_text.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"✓ 图表已保存: {output_path}")

    plt.close()


def main():
    """
    主函数：运行所有演示
    """
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "  Matplotlib 中文字体配置演示程序".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "=" * 48 + "╝")

    # 列出可用的中文字体
    print("\n检测系统中可用的中文字体:")
    available_fonts = list_available_chinese_fonts()
    if available_fonts:
        print(f"✓ 找到 {len(available_fonts)} 个中文字体:")
        for font in available_fonts:
            print(f"  - {font}")
    else:
        print("✗ 未找到中文字体，某些演示可能无法正常显示")

    try:
        # 运行所有演示
        demo_basic_plot()
        demo_multi_subplot()
        demo_scatter_plot()
        demo_chinese_text()

        print("\n" + "=" * 50)
        print("✓ 所有演示已完成！")
        print("=" * 50)
        print("\n生成的图表已保存到 outputs/ 目录:")
        print("  - demo_basic_plot.png")
        print("  - demo_multi_subplot.png")
        print("  - demo_scatter_plot.png")
        print("  - demo_chinese_text.png")
        print("\n所有中文内容应该能正确显示，而不是显示为方框。")

    except Exception as e:
        print(f"\n✗ 演示过程中出现错误: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
