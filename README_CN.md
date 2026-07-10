# RepoPilot Hy3

[English README](README.md)

RepoPilot Hy3 是一个由 Hy3 驱动的开源项目复现与报错诊断助手。它帮助开发者理解陌生仓库、生成可运行的启动方案、诊断终端错误，并输出可复制到 README、Issue 或 PR 的复现报告。

本项目面向 [Tencent-Hunyuan/Hy3 Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4)，展示 Hy3 在“开源项目复现”这一具体开发场景中的能力。

## 场景价值

开发者接手新仓库时，常见问题包括文档不完整、依赖版本漂移、启动命令不明确、终端报错难定位。RepoPilot Hy3 将这些步骤组织成一个交互式流程：

- 上传项目 zip 或粘贴 README、文件树、配置文件。
- 让 Hy3 识别技术栈、入口文件、依赖管理方式和运行命令。
- 粘贴终端错误后，由 Hy3 给出可能原因、修复命令和验证步骤。
- 生成可复制到 README、Issue 或 PR 的复现报告。

## 功能

- 上传项目 zip 或粘贴项目上下文。
- 提取 `README.md`、`package.json`、`requirements.txt`、`pyproject.toml`、`Dockerfile` 等关键文件。
- 生成项目画像、运行命令、风险点和验证步骤。
- 诊断终端错误日志。
- 生成 Markdown 复现报告。
- 提供可复制结果的 Web 界面。

## 项目结构

```text
RepoPilot Hy3/
  apps/
    api/                 # FastAPI 后端
    web/                 # Vite React 前端
  docs/                  # 演示脚本和 Hy3 角色说明
  examples/              # 示例输入
  README.md
  README_CN.md
```

## 快速开始

### 环境要求

- Python 3.10+，包含 `venv` 和 `pip`
- Node.js 18+，包含 `npm`
- 可以访问 PyPI、npm registry 和 Hy3 API 网关的网络环境
- Hy3 兼容 API Key
- 本地 `8000` 和 `5173` 端口未被占用

完整依赖清单见 [REQUIREMENTS.md](REQUIREMENTS.md)。

### 1. 配置 Hy3

复制 `.env.example` 到仓库根目录 `.env`，或复制到 `apps/api/.env`，然后填入你的 key：

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
VITE_API_BASE_URL=http://127.0.0.1:8000
```

不要提交真实 API Key。

### 2. 一键启动

在仓库根目录执行对应平台的脚本。

Windows PowerShell：

```powershell
.\start.ps1
```

Windows 命令提示符：

```bat
start.bat
```

macOS / Linux：

```bash
chmod +x ./start.sh
./start.sh
```

脚本会自动安装缺失的后端和前端依赖，然后启动：

- 后端 API：`http://127.0.0.1:8000`
- 前端页面：`http://127.0.0.1:5173`

脚本不会安装 Python、Node.js 这类系统级依赖。全新电脑需要先安装这些基础环境。

PowerShell、macOS、Linux 中按 `Ctrl+C` 停止；`start.bat` 会打开两个窗口，关闭窗口即可停止。

### 手动启动

如果需要分别排查前后端，可以使用手动命令。

后端：

```bash
cd "apps/api"
python -m venv .venv

# Windows
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# macOS / Linux
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

前端：

```bash
cd "apps/web"
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

打开 `http://127.0.0.1:5173` 即可使用。

## 后端 API 调用

后端 API 运行在 `http://127.0.0.1:8000`。根路径 `/` 不是前端页面，所以直接打开 `http://127.0.0.1:8000` 可能会看到 `404`。请使用接口文档或下面的具体接口：

- API 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`GET /health`
- 分析粘贴的项目上下文：`POST /analyze-text`
- 分析上传的项目 zip：`POST /analyze-zip`
- 诊断错误日志：`POST /diagnose-error`
- 生成复现报告：`POST /generate-report`

健康检查：

```bash
curl http://127.0.0.1:8000/health
```

分析粘贴文本：

```bash
curl -X POST http://127.0.0.1:8000/analyze-text \
  -H "Content-Type: application/json" \
  -d '{
    "project_notes": "这里粘贴 README、文件树、package.json 或启动说明。",
    "error_log": "这里粘贴可选的终端错误日志。"
  }'
```

上传并分析项目 zip：

```bash
curl -X POST http://127.0.0.1:8000/analyze-zip \
  -F "file=@/path/to/project.zip" \
  -F "error_log=可选的终端错误日志"
```

诊断错误日志：

```bash
curl -X POST http://127.0.0.1:8000/diagnose-error \
  -H "Content-Type: application/json" \
  -d '{
    "project_context": "这里粘贴项目上下文。",
    "error_log": "这里粘贴终端错误日志。"
  }'
```

根据前面结果生成报告：

```bash
curl -X POST http://127.0.0.1:8000/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": "这里粘贴分析结果。",
    "diagnosis": "这里粘贴诊断结果，也可以留空。"
  }'
```

## 常见问题

- 提示 `HY3_API_KEY is not configured`：从 `.env.example` 创建 `.env`，并替换占位 key。
- 提示找不到 Python：安装 Python 3.10+，并确认终端可以使用 `python`、`python3` 或 `py`。
- 提示找不到 Node.js 包管理器：安装 Node.js 18+，或安装 pnpm。
- 出现 `npm warn allow-scripts ... esbuild`：这是 npm 的安全提示，不代表安装失败。如果前端正常启动，可以忽略；如果后续 Vite 报 `esbuild` 相关错误，进入 `apps/web` 后执行 `npm approve-scripts --allow-scripts-pending`，批准 `esbuild`，再重新运行启动脚本。
- `start.bat` 在 `found 0 vulnerabilities` 后停止：拉取最新版本。旧版 `start.bat` 没有用 `call` 调用 `npm`，Windows 批处理会在 `npm install` 后中断父脚本。
- 端口被占用：停止占用 `8000` 或 `5173` 的进程，或修改启动脚本的端口参数。
- `/health` 正常但模型调用失败：检查 `HY3_API_KEY`、`HY3_BASE_URL` 和 `HY3_MODEL`。

## Demo

- Demo 1：上传 `examples/demo-react-app.zip`，让 Hy3 生成 React/Vite 项目复现方案。
- Demo 2：粘贴 Python 项目上下文和 `ModuleNotFoundError` 日志，让 Hy3 生成修复清单。

详细脚本见 [docs/demo-1-react.md](docs/demo-1-react.md) 和 [docs/demo-2-python-error.md](docs/demo-2-python-error.md)。
