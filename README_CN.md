# RepoPilot Hy3

[English](README.md) | 中文

RepoPilot Hy3 是面向本机使用的项目复现与研发协作助手。它将项目文件、GitHub 数据和错误日志组织成可追溯的分析、诊断与报告。

## 功能

- 上传 ZIP 或粘贴项目说明，生成复现步骤、错误诊断和 Markdown 报告。
- 将 ZIP 导入工作台，或连接 GitHub／兼容接口仓库，查看 Issue、PR 和 CI。
- 在 AI 工作台使用项目文件搜索、对话、工具调用、Skill 和多 Agent 工作流。
- 上传知识文档，进行检索、带来源的问答、项目记忆和代码图谱浏览。
- 生成周报，管理多个项目、操作草稿、反馈和审计记录。
- 在评测页面运行 RAGAS 评测、查看轨迹和对比结果；固定评测集由使用者自行提供，自动文档冒烟测试只能验证链路。

项目使用 React/Vite、FastAPI 和 SQLite。默认运行在本机，生成任务通过远程模型 API 完成。

## 环境与启动

需要 Python 3.11 或更新版本、Node.js 18 或更新版本、npm 或 pnpm，以及可用的模型 API Key。将 `.env.example` 复制为项目根目录下的 `.env`，配置：

```dotenv
HY3_API_KEY=your_api_key
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy4-flash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

`HY3_MODEL` 用于指定生成模型。不要提交 `.env` 或真实密钥。

Windows PowerShell：

```powershell
.\start.ps1
```

Windows 命令提示符使用 `start.bat`，macOS/Linux 使用 `./start.sh`。脚本会安装依赖并启动服务。默认 Web 地址是 `http://127.0.0.1:5173`，API 文档是 `http://127.0.0.1:8000/docs`，健康检查为 `http://127.0.0.1:8000/health`。首次安装依赖可能需要一些时间。

已有示例：`examples/demo-react-app.zip` 可用于 ZIP 复现；`docs/demo-2-python-error.md` 提供 Python 错误诊断输入。

## 添加项目

首页提供项目复现流程。要在 AI 工作台检索项目文件，可在“仓库”页导入 ZIP 或添加本地目录；本地目录不要求 Git，也不会被复制。ZIP 会在 `.data/repos/imports/` 中创建受大小限制的本地副本。GitHub 数据同步、Issue、PR 和 CI 功能需要连接相应仓库；本地项目不会自动产生远程仓库数据。

## 知识检索与远程服务

默认使用 SQLite、关键词检索和本地确定性演示向量，不需要额外服务。此时向量库状态显示为 `degraded`；这不代表语义向量检索已经启用。重建索引时会提示当前是文档索引还是完整向量索引。

如需完整向量检索，可启动 `docker compose up -d postgres etcd minio milvus`，并在 `.env` 中配置可用的独立远程 Embedding 服务：

```dotenv
MILVUS_ENABLED=true
MILVUS_URI=http://127.0.0.1:19530
MILVUS_COLLECTION=repopilot_rag_v1
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_BASE_URL=https://your-embedding-service.example/v1
EMBEDDING_API_KEY=your_embedding_key
EMBEDDING_MODEL=your_embedding_model
EMBEDDING_DIMENSIONS=1024
```

Embedding 服务需要提供兼容的 `/embeddings` 接口，维度必须与实际返回一致。SQLite 仍可用于业务数据；如需 PostgreSQL，另行设置 `DATABASE_URL`，两个数据库的数据不会自动合并。

可独立配置重排服务：

```dotenv
RERANK_BASE_URL=https://your-rerank-service.example/v1/rerank
RERANK_API_KEY=your_rerank_key
RERANK_MODEL=your_rerank_model
```

服务需接受 `model`、`query`、`documents` 和 `top_n`，并返回带 `index` 和相关性分数的 `results`。可选 `RERANK_INSTRUCTION` 会作为 `instruct` 发送。远程服务不可用时，检索轨迹会标记降级为启发式重排。

改变 Embedding 模型或维度时，应使用新的 Milvus collection，并在每个已有项目的知识问答页重建索引；不同向量空间不能混用。启用服务和切换模型不会自动迁移或删除原有数据。

## 评测与数据

“评测”页面支持 RAGAS 任务、结果和回归对比。可使用自动文档冒烟测试，也可在 `docs/datas/evals/` 放置自行维护的 JSON 评测集。评测需要可用的 Judge 模型；结果会区分质量失败和评分执行异常。

本机数据库、上传文件、项目副本和自动生成的 Token 加密密钥位于 `.data/`，默认不提交到 Git；也可在 `.env` 中自行设置 `TOKEN_ENCRYPTION_KEY`。备份数据库时需妥善保管对应密钥。本机 API 不提供多人登录，应只绑定本机地址；远程或多人部署需要另行增加认证与权限控制。

## 验证

前端运行 `pnpm test` 和 `pnpm build`。后端在 `apps/api` 目录运行 `python -m pytest app/tests`。模型、GitHub、Embedding、重排和 Milvus 的真实联调分别依赖其凭据和服务状态。
