<div align="center">

中文 | [English](README.md)

# RepoPilot Hy3

**由 Hy3 驱动的项目复现与错误诊断助手。**

将仓库证据和终端日志转化为可执行的部署方案、可操作的诊断建议与可复用的 Markdown 报告。

</div>

---

## 目录

- [项目概览](#项目概览)
- [Issue #4 要求对照](#issue-4-要求对照)
- [Hy3 在系统中的角色](#hy3-在系统中的角色)
- [主要功能](#主要功能)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [端到端 Demo](#端到端-demo)
- [后端 API](#后端-api)
- [常见问题](#常见问题)
- [CodeBuddy 协作说明](#codebuddy-协作说明)
- [安全说明](#安全说明)
- [相关文档](#相关文档)
- [活动提交说明](#活动提交说明)

---

## 项目概览

复现一个陌生仓库通常不只是执行一条命令：文档可能不完整，依赖版本可能发生漂移，入口文件可能不明确，终端输出也经常难以快速定位。

RepoPilot Hy3 将这套流程组织成一个交互式开发者工具。上传项目 zip 或粘贴仓库说明，再按需添加错误日志，即可让 Hy3 生成：

- 基于仓库文件证据的项目画像。
- 检测到的框架、运行时、包管理器与入口文件。
- 包含运行命令的分步复现清单。
- 针对终端报错的可能根因与修复步骤。
- 可复制到 README、Issue 或 PR 的 Markdown 复现报告。

本项目面向 [Tencent-Hunyuan/Hy3 Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 构建。该 Issue 要求参与者在具体真实场景中，通过 Hy3 API 完成一个可端到端运行的应用。

## Issue #4 要求对照

| Issue 要求 | 本仓库状态 | 对应实现 |
| --- | --- | --- |
| 通过 Hy3 API 调用模型，不训练、不微调、不做本地推理 | 已完成 | FastAPI 后端调用可配置的 Hy3 兼容 OpenAI API |
| 至少提供一个可交互前端 | 已完成 | 双语 React/Vite Web 界面，支持上传、文本输入、操作按钮、结果标签页与复制 |
| 至少跑通两个端到端 Demo | 已完成 | 下文提供 React/Vite 项目复现与 Python 错误诊断流程 |
| 提供不超过两分钟的视频或 GIF | 已完成 | [Demo 视频](#demo-视频)提供两段 1080p 演示，每段均不超过一分钟 |
| 公开项目源码并说明 Hy3 的角色 | 已记录 | 仓库源码公开，Hy3 职责在下文完整说明；本 README 不作许可证声明 |
| 记录 CodeBuddy 协作完成的内容 | 已记录 | 详见 [CodeBuddy 协作说明](#codebuddy-协作说明) |

## Hy3 在系统中的角色

Hy3 是 RepoPilot 的核心推理引擎，不是本地依赖，也不是简单的通用聊天组件。应用使用 Hy3 完成：

- 理解 README、依赖清单、配置文件、文件树和终端日志。
- 推断项目技术栈，并生成基于证据的部署说明。
- 诊断安装与运行错误，给出可能原因、修复命令和验证步骤。
- 将分析与诊断结果整理为结构化 Markdown 复现报告。

```text
开发者输入
    -> React Web 界面
    -> FastAPI 提取证据并构造提示词
    -> Hy3 API
    -> 经过净化、可直接复制的 Markdown
```

所有模型能力均通过配置的 API 端点访问。RepoPilot Hy3 **不进行模型训练、微调、本地推理或本地模型部署**。

处理上传压缩包时，后端会先验证 zip 路径，再筛选相关文本文件并限制提交上下文的长度。前端在渲染模型生成的 Markdown 前会进行安全净化。

## 主要功能

- 上传项目 `.zip`，或粘贴 README、文件树、配置与部署说明。
- 从 `README.md`、`package.json`、`requirements.txt`、`pyproject.toml`、`Dockerfile` 和框架配置中提取关键证据。
- 生成项目画像、可能的运行命令、风险点和验证方案。
- 诊断粘贴的终端错误和堆栈信息。
- 生成可复用的 Markdown 项目复现报告。
- 在 Web 界面中切换中文和英文。
- 直接复制分析、诊断与报告结果。

## 项目结构

```text
RepoPilot Hy3/
├── apps/
│   ├── api/                  # FastAPI 后端与 Hy3 API 集成
│   └── web/                  # React/Vite 交互式前端
├── docs/                     # Demo 指南与 Hy3 角色说明
├── examples/                 # 内置 Demo 输入
├── video/                    # Demo 1 与 Demo 2 演示视频
├── .env.example              # Hy3 API 配置模板
├── start.ps1                 # PowerShell 一键启动脚本
├── start.bat                 # 命令提示符一键启动脚本
├── start.sh                  # macOS/Linux 一键启动脚本
├── README.md                 # 英文文档
└── README_CN.md              # 中文文档
```

## 快速开始

### 环境要求

- Python 3.10+，包含 `venv` 和 `pip`。
- Node.js 18+，包含 `npm`（也可使用 `pnpm`）。
- 能够访问 Python、JavaScript 包仓库和已配置 Hy3 API 端点的网络环境。
- Hy3 兼容 API Key。
- 本地 `8000` 和 `5173` 端口未被占用。

完整环境检查和平台说明见 [REQUIREMENTS.md](REQUIREMENTS.md)。

### 1. 克隆并配置

```bash
git clone https://github.com/BoyuChen1224/repopilot-hy3.git
cd repopilot-hy3
```

复制环境变量模板：

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bat
:: Windows 命令提示符
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

编辑 `.env`，替换 API Key 占位值：

```dotenv
HY3_API_KEY=your_hy3_api_key
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
VITE_API_BASE_URL=http://127.0.0.1:8000
```

不要提交真实 API Key。如果希望使用后端服务目录中的配置，也可以将文件保存为 `apps/api/.env`。

### 2. 启动前后端服务

在仓库根目录执行对应平台的一条命令。

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

启动脚本会在需要时创建后端虚拟环境、安装项目依赖，并启动两个服务：

| 服务 | 地址 |
| --- | --- |
| Web 界面 | `http://127.0.0.1:5173` |
| 后端 API | `http://127.0.0.1:8000` |
| 交互式 API 文档 | `http://127.0.0.1:8000/docs` |
| 健康检查 | `http://127.0.0.1:8000/health` |

API 根路径 `/` 不是 Web 页面，直接打开时可能返回 `404`；请访问 Web 界面或 API 文档。

### 3. 验证部署

```bash
curl http://127.0.0.1:8000/health
```

预期响应：

```json
{"status":"ok"}
```

然后打开 `http://127.0.0.1:5173`，运行 [Demo 1](#demo-1reactvite-项目复现)。

### 手动启动

需要分别查看前后端日志时，可以在两个终端中启动服务。

后端：

```bash
cd apps/api
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
cd apps/web
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## 端到端 Demo

### Demo 1：React/Vite 项目复现

**输入：** [`examples/demo-react-app.zip`](examples/demo-react-app.zip)

**操作流程：**

1. 打开 Web 界面。
2. 上传 `examples/demo-react-app.zip`。
3. 点击 **分析**，生成基于仓库证据的复现方案。
4. 查看“分析”标签页，再点击 **报告**。

**预期输出：** Hy3 根据仓库证据识别 Vite 和 React，推荐 Node.js/npm 命令，提示运行时版本不匹配或缺少锁文件等风险，给出验证步骤，并生成可复用的 Markdown 报告。

详细指南：[docs/demo-1-react.md](docs/demo-1-react.md)

### Demo 2：Python 错误诊断

**输入：** 粘贴 [`examples/demo-python-error/README.md`](examples/demo-python-error/README.md) 中的项目上下文，以及 [`docs/demo-2-python-error.md`](docs/demo-2-python-error.md) 中的 `ModuleNotFoundError` 日志。

**操作流程：**

1. 将项目上下文粘贴到 **项目说明或 README**。
2. 将终端日志粘贴到 **错误日志**。
3. 依次点击 **分析** 和 **诊断**。
4. 查看可能原因和修复步骤，再点击 **报告**。

**预期输出：** Hy3 识别缺失的 `requests` 依赖，以 `requirements.txt` 为诊断依据，建议创建虚拟环境并执行 `pip install -r requirements.txt`，最后通过 `python main.py` 验证修复结果。

详细指南：[docs/demo-2-python-error.md](docs/demo-2-python-error.md)

### Demo 视频

| Demo | 视频 | 时长 | 分辨率 |
| --- | --- | --- | --- |
| React/Vite 项目复现 | [观看 Demo 1](video/Demo_1.mp4) | 00:47 | 1920×1080 |
| Python 错误诊断 | [观看 Demo 2](video/Demo_2.mp4) | 00:59 | 1920×1080 |

两段视频均满足 Issue #4 的两分钟以内要求。如果浏览器无法内嵌播放 MP4，请从对应的 GitHub 文件页面打开视频。

## 后端 API

| 方法 | 接口 | 用途 |
| --- | --- | --- |
| `GET` | `/health` | 检查后端是否正常运行 |
| `POST` | `/analyze-text` | 分析粘贴的项目说明和可选错误日志 |
| `POST` | `/analyze-zip` | 提取并分析上传的项目 zip |
| `POST` | `/diagnose-error` | 结合项目上下文诊断终端错误 |
| `POST` | `/generate-report` | 将分析与诊断结果整理为 Markdown 报告 |

打开 `http://127.0.0.1:8000/docs` 可查看请求结构并直接调试接口。

## 常见问题

- **提示 `HY3_API_KEY is not configured`：** 从 `.env.example` 创建 `.env`，并将占位值替换为有效 Key。
- **找不到 Python：** 安装 Python 3.10+，并确认终端中可以使用 `python`、`python3` 或 `py`。
- **找不到 Node.js 包管理器：** 安装带 npm 的 Node.js 18+，或安装 pnpm。
- **端口被占用：** 停止占用 `8000` 或 `5173` 的进程，或在启动脚本支持的情况下传入其他端口。
- **健康检查正常但模型调用失败：** 检查 `HY3_API_KEY`、`HY3_BASE_URL` 和 `HY3_MODEL`。
- **npm 提示 `esbuild` 安装脚本未批准：** 如果 Vite 无法启动，在 `apps/web` 下执行 `npm approve-scripts --allow-scripts-pending`，批准 `esbuild` 后重试。

更多说明见 [REQUIREMENTS.md](REQUIREMENTS.md)。

## CodeBuddy 协作说明

CodeBuddy 协作完成的项目内容包括：

- FastAPI 接口与 Hy3 兼容 API 集成。
- React/Vite 交互式前端、双语界面文案、结果标签页和复制操作。
- 仓库 zip 证据提取与压缩包路径安全校验。
- 分析、诊断和报告生成所使用的提示词设计。
- 跨平台一键启动脚本与环境变量处理。
- Demo 输入、Issue 提交说明、故障排查内容和双语 README 组织。

项目最终行为和文档内容均根据仓库中的实际代码与 Issue #4 要求进行了复核。

## 安全说明

- 真实 API Key 只应保存在 `.env` 或进程环境变量中，不要提交到仓库。
- 解压前会校验 zip 成员路径，避免压缩包路径穿越。
- 上传的仓库上下文在发送至已配置 API 前会受到长度限制。
- 模型生成的 Markdown 在浏览器渲染前会通过 DOMPurify 净化。
- 在陌生环境中运行模型建议的命令前，应先人工检查。

## 相关文档

- [环境要求](REQUIREMENTS.md)
- [Hy3 角色与提示词原则](docs/hy3-role.md)
- [Demo 1 指南](docs/demo-1-react.md)
- [Demo 2 指南](docs/demo-2-python-error.md)
- [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4)
- [Tencent-Hunyuan/Hy3](https://github.com/Tencent-Hunyuan/Hy3)

## 活动提交说明

Issue #4 要求通过 Pull Request 将活动成果提交到 [`Tencent-Hunyuan/Hy3:rhinobird2026`](https://github.com/Tencent-Hunyuan/Hy3/tree/rhinobird2026)。RepoPilot Hy3 是独立应用仓库，因此该 PR 应补充本仓库链接、简要项目说明、两条 Demo 流程，以及 [Demo 1](video/Demo_1.mp4) 和 [Demo 2](video/Demo_2.mp4) 视频链接。
