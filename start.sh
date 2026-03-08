#!/bin/bash
# 启动脚本 - 明日方舟终末地伊冯配队展示项目

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ 未找到 $1，请先安装"
        exit 1
    fi
    echo "✅ $1 已安装"
}

is_port_open() {
    local port=$1
    python3 - "$port" <<'PY'
import socket, sys
port = int(sys.argv[1])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(0.5)
    ok = s.connect_ex(("127.0.0.1", port)) == 0
print("1" if ok else "0")
PY
}

cleanup() {
    echo ""
    echo "🛑 正在停止服务..."
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

echo "🎮 启动明日方舟终末地 - 伊冯配队展示项目"
echo "================================"
echo ""
echo "🔍 检查依赖..."
check_dependency uv
check_dependency node
check_dependency npm
check_dependency python3

# 启动后端
echo ""
echo "🚀 启动后端服务..."
cd "$PROJECT_DIR/backend"

VENV_PY=".venv/bin/python"
echo "📦 使用 uv 安装依赖 (优先 Python 3.12)..."
if [ -x "$VENV_PY" ]; then
    echo "♻️ 检测到已存在虚拟环境，跳过创建"
else
    echo "🛠️ 创建虚拟环境..."
    if ! uv venv --python 3.12; then
        echo "⚠️ Python 3.12 不可用，回退到系统默认 Python"
        uv venv
    fi
fi

uv pip install --python "$VENV_PY" -r requirements.txt
mkdir -p ../data

if [ "$(is_port_open 8181)" = "1" ]; then
    echo "ℹ️ 检测到 8181 端口已有服务，跳过后端启动（复用现有服务）"
else
    "$VENV_PY" -m app.main &
    BACKEND_PID=$!
    echo "✅ 后端已启动 (PID: $BACKEND_PID, Port: 8181)"
    sleep 2
fi

if [ "$(is_port_open 8181)" != "1" ]; then
    echo "❌ 后端启动失败：8181 端口未监听"
    exit 1
fi

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

if [ "$(is_port_open 3131)" = "1" ]; then
    echo "ℹ️ 检测到 3131 端口已有服务，跳过前端启动（复用现有服务）"
else
    npm run dev -- --port 3131 &
    FRONTEND_PID=$!
    echo "✅ 前端已启动 (PID: $FRONTEND_PID, Port: 3131)"
fi

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

wait
