#!/bin/bash
# 启动脚本 - 明日方舟终末地伊冯配队展示项目

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🎮 启动明日方舟终末地 - 伊冯配队展示项目"
echo "================================"

# 检查依赖
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ 未找到 $1，请先安装"
        exit 1
    fi
    echo "✅ $1 已安装"
}

echo ""
echo "🔍 检查依赖..."
check_dependency uv
check_dependency node
check_dependency npm

# 启动后端
echo ""
echo "🚀 启动后端服务..."
cd "$PROJECT_DIR/backend"

# 使用 uv 创建虚拟环境并安装依赖
echo "📦 使用 uv 安装依赖 (优先 Python 3.12)..."
uv venv --python 3.12
uv pip install -r requirements.txt

# 检查数据库
if [ ! -f "../data/arknights_endfield.db" ]; then
    echo "🗄️ 初始化数据库..."
    mkdir -p ../data
fi

# 后台启动后端
uv run python -m app.main &
BACKEND_PID=$!
echo "✅ 后端已启动 (PID: $BACKEND_PID, Port: 8181)"

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

npm run dev -- --port 3131 &
FRONTEND_PID=$!
echo "✅ 前端已启动 (PID: $FRONTEND_PID, Port: 3131)"

echo ""
echo "================================"
echo "🎉 项目已启动!"
echo ""
echo "📱 前端: http://localhost:3131"
echo "🔌 后端: http://localhost:8181"
echo "📚 API文档: http://localhost:8181/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================"

# 捕获退出信号
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# 保持脚本运行
wait
