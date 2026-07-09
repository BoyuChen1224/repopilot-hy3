# RepoPilot Hy3

RepoPilot Hy3 是一个由 Hy3 驱动的开源项目复现与报错诊断助手。它面向开发者在运行陌生仓库时遇到的真实问题：文档不完整、依赖版本漂移、启动命令不明确、终端报错难以定位。

本项目用于 [Tencent-Hunyuan/Hy3 Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4)，展示 Hy3 在“开源仓库复现”这一具体开发场景下的能力。

## 场景价值

开发者接手一个新仓库时，通常要先读 README、判断技术栈、安装依赖、试运行命令，并在报错后反复排查。RepoPilot Hy3 把这些步骤组织成一个可交互流程：

- 上传项目 zip 或粘贴 README、文件树、配置文件。
- 让 Hy3 识别技术栈、入口文件、依赖管理方式和运行命令。
- 粘贴终端错误后，由 Hy3 给出可能原因、修复命令和验证步骤。
- 生成可复制到 README、Issue 或 PR 的复现报告。

## Hy3 的角色

Hy3 是本项目的核心推理引擎，负责：

- 从仓库文件和日志中提取证据。
- 区分确定事实、合理推断和缺失信息。
- 生成可执行的复现清单。
- 诊断安装、启动和运行时错误。
- 输出结构化 Markdown 报告。

项目不做模型微调，也不在本地运行模型；智能分析均通过 Hy3 API 完成。

## 亮点

- 具体场景明确：聚焦开源项目复现，不是通用聊天壳。
- 端到端闭环：仓库分析、错误诊断、报告生成三个步骤串联。
- 证据驱动：后端提取重要文件，Prompt 要求 Hy3 基于文件和日志说明原因。
- 可演示性强：包含 React/Vite 与 Python 报错两个 demo。
- 工程细节完整：后端校验 zip 路径，前端清洗模型返回的 Markdown。

## 快速开始

### 1. 配置 Hy3

创建根目录 `.env` 或 `apps/api/.env`：

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
```

请不要提交真实 API Key。

### 2. 启动后端

```bash
cd "apps/api"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd "apps/web"
npm install
npm run dev
```

打开终端中显示的 Vite 地址即可使用。

## Demo

- Demo 1：上传 `examples/demo-react-app.zip`，让 Hy3 生成 React/Vite 项目复现方案。
- Demo 2：粘贴 Python 项目上下文和 `ModuleNotFoundError` 日志，让 Hy3 生成修复清单。

详细脚本见 [docs/demo-1-react.md](docs/demo-1-react.md) 和 [docs/demo-2-python-error.md](docs/demo-2-python-error.md)。
