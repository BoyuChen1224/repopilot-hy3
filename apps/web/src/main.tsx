import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import { Sparkles } from "lucide-react";
import Reproduction from "./reproduction";
import "./portal/app/globals.css";
import "./shell.css";

const Workspace = React.lazy(() => import("./portal/app/page"));
const Repositories = React.lazy(() => import("./portal/app/repos/page"));
const Chat = React.lazy(() => import("./portal/app/chat/page"));
const Issues = React.lazy(() => import("./portal/app/issues/page"));
const PullRequests = React.lazy(() => import("./portal/app/pull-requests/page"));
const CI = React.lazy(() => import("./portal/app/ci/page"));
const Knowledge = React.lazy(() => import("./portal/app/knowledge/page"));
const KnowledgeDetail = React.lazy(() => import("./portal/app/knowledge/[id]/page"));
const RAG = React.lazy(() => import("./portal/app/rag/page"));
const CodeGraph = React.lazy(() => import("./portal/app/code-graph/page"));
const Workspaces = React.lazy(() => import("./portal/app/workspaces/page"));
const WorkflowRuns = React.lazy(() => import("./portal/app/workflow-runs/page"));
const ActionDrafts = React.lazy(() => import("./portal/app/action-drafts/page"));
const Reports = React.lazy(() => import("./portal/app/reports/page"));
const Evals = React.lazy(() => import("./portal/app/evals/page"));

const navigation = [["/", "项目复现"], ["/workspace", "AI 工作台"], ["/repos", "仓库"], ["/rag", "知识问答"]] as const;
const collaboration = [["/issues", "Issue"], ["/pull-requests", "PR"], ["/ci", "CI"], ["/knowledge", "项目知识"], ["/code-graph", "代码图谱"]] as const;
const management = [["/workflow-runs", "工作流"], ["/workspaces", "多仓库"], ["/reports", "报告"], ["/action-drafts", "操作草稿"], ["/evals", "评测"]] as const;

function NavigationMenu({ label, items }: { label: string; items: readonly (readonly [string, string])[] }) {
  return <details className="shellMenu">
    <summary className="shellLink">{label} ▾</summary>
    <div className="shellMenuList">
      {items.map(([path, title]) => <NavLink key={path} to={path} className="shellMenuLink" onClick={(event) => event.currentTarget.closest("details")?.removeAttribute("open")}>{title}</NavLink>)}
    </div>
  </details>;
}

function AppShell() {
  return (
    <div className="shell">
      <header className="shellHeader">
        <NavLink className="shellBrand" to="/" aria-label="RepoPilot Hy3">
          <span className="shellMark"><Sparkles size={18} /></span>
          <strong>RepoPilot Hy3</strong>
        </NavLink>
        <nav className="shellNav" aria-label="主导航">
          {navigation.map(([path, label]) => (
            <NavLink key={path} to={path} end={path === "/"} className={({ isActive }) => isActive ? "shellLink active" : "shellLink"}>
              {label}
            </NavLink>
          ))}
          <NavigationMenu label="研发协作" items={collaboration} />
          <NavigationMenu label="管理与评测" items={management} />
        </nav>
      </header>
      <div className="shellContent">
        <React.Suspense fallback={<p className="shellLoading">正在加载…</p>}>
        <Routes>
          <Route path="/" element={<Reproduction />} />
          <Route path="/workspace" element={<Workspace />} />
          <Route path="/repos" element={<Repositories />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/issues" element={<Issues />} />
          <Route path="/pull-requests" element={<PullRequests />} />
          <Route path="/ci" element={<CI />} />
          <Route path="/knowledge" element={<Knowledge />} />
          <Route path="/knowledge/:id" element={<KnowledgeDetail />} />
          <Route path="/rag" element={<RAG />} />
          <Route path="/code-graph" element={<CodeGraph />} />
          <Route path="/workspaces" element={<Workspaces />} />
          <Route path="/workflow-runs" element={<WorkflowRuns />} />
          <Route path="/action-drafts" element={<ActionDrafts />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/evals" element={<Evals />} />
          <Route path="*" element={<Reproduction />} />
        </Routes>
        </React.Suspense>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<BrowserRouter><AppShell /></BrowserRouter>);
