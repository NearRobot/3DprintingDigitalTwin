#!/bin/bash
# 测试运行脚本

set -e

echo "运行项目测试..."
echo "================================"

# 激活虚拟环境（如果存在）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# 运行 pytest
echo "运行单元测试..."
pytest tests/ -v --tb=short

echo ""
echo "================================"
echo "测试完成！"
