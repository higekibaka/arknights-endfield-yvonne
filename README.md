# 明日方舟终末地 - 伊冯配队展示项目

## 🚀 快速启动

### 前置要求
- [uv](https://docs.astral.sh/uv/) - Python 包管理器
- Node.js + npm

### 一键启动

```bash
./start.sh
```

### 手动启动

#### 后端启动

```bash
cd backend

# 使用 uv 创建虚拟环境并安装依赖（优先 Python 3.12）
uv venv --python 3.12
uv pip install -r requirements.txt

# 安装Playwright浏览器
uv run playwright install chromium

# 启动服务
uv run python -m app.main
```

后端将在 http://localhost:8181 运行
API文档: http://localhost:8181/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动 (端口 3131)
npm run dev -- --port 3131
```

前端将在 http://localhost:3131 运行

## 📁 项目结构

```
projects/arknights-endfield-yvonne/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── main.py       # API入口
│   │   ├── models/       # 数据库模型
│   │   └── services/     # 业务逻辑
│   └── requirements.txt
├── frontend/             # Next.js 前端
│   ├── app/              # 页面
│   ├── components/       # 组件
│   └── styles/           # 样式
├── data/                 # 数据存储
└── docs/                 # 文档
```

## 🔧 功能特性

- ✅ 每日自动抓取多平台数据
- ✅ 现代化科幻风格UI
- ✅ 配队方案展示
- ✅ 装备配置可视化
- ✅ 输出手法说明
- ✅ 数据来源追踪

## 📝 定时任务

系统已配置每日 08:00 (北京时间) 自动执行数据抓取，可通过以下方式查看：

```bash
openclaw status  # 查看定时任务状态
```

---

Made with 🦐 by 虾虾
