import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertCircle, Check, Clipboard, Copy, FileArchive, FileText, Languages, Loader2, Sparkles } from "lucide-react";
import { marked } from "marked";
import DOMPurify from "dompurify";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type ResultState = {
  analysis?: string;
  diagnosis?: string;
  report?: string;
};

type Language = "en" | "zh";

const copy = {
  en: {
    subtitle: "Repository reproduction and error diagnosis assistant.",
    switchLanguage: "中文",
    upload: "Upload project .zip",
    projectNotes: "Project notes or README",
    projectNotesPlaceholder: "Paste README, file tree, package.json, or setup notes...",
    errorLog: "Error log",
    errorLogPlaceholder: "Paste terminal errors, stack traces, or failed install output...",
    analyze: "Analyze",
    diagnose: "Diagnose",
    report: "Report",
    loadingAnalyze: "Analyzing with Hy3...",
    loadingDiagnose: "Diagnosing error log...",
    loadingReport: "Generating report...",
    requestFailed: "Request failed",
    unknownError: "Unknown error",
    noOutput: "No output yet.",
    copy: "Copy",
    copied: "Copied",
    tabs: {
      analysis: "Analysis",
      diagnosis: "Diagnosis",
      report: "Report"
    }
  },
  zh: {
    subtitle: "项目复现与错误诊断助手。",
    switchLanguage: "EN",
    upload: "上传项目 .zip",
    projectNotes: "项目说明或 README",
    projectNotesPlaceholder: "粘贴 README、文件树、package.json 或启动说明...",
    errorLog: "错误日志",
    errorLogPlaceholder: "粘贴终端错误、堆栈跟踪或安装失败输出...",
    analyze: "分析",
    diagnose: "诊断",
    report: "报告",
    loadingAnalyze: "正在使用 Hy3 分析...",
    loadingDiagnose: "正在诊断错误日志...",
    loadingReport: "正在生成报告...",
    requestFailed: "请求失败",
    unknownError: "未知错误",
    noOutput: "暂无输出。",
    copy: "复制",
    copied: "已复制",
    tabs: {
      analysis: "分析",
      diagnosis: "诊断",
      report: "报告"
    }
  }
} as const;

function MarkdownBlock({ content, emptyText }: { content?: string; emptyText: string }) {
  const html = useMemo(() => DOMPurify.sanitize(marked.parse(content || emptyText) as string), [content, emptyText]);
  return <div className="markdown" dangerouslySetInnerHTML={{ __html: html }} />;
}

function CopyButton({ content, labels }: { content?: string; labels: { copy: string; copied: string } }) {
  const [copied, setCopied] = useState(false);
  const copyText = content || "";
  const hasContent = !!copyText.trim();

  async function copyContent() {
    if (!hasContent) {
      return;
    }
    await navigator.clipboard.writeText(copyText);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <button className="copyButton" onClick={copyContent} disabled={!hasContent} type="button">
      {copied ? <Check size={16} /> : <Copy size={16} />}
      {copied ? labels.copied : labels.copy}
    </button>
  );
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [projectNotes, setProjectNotes] = useState("");
  const [errorLog, setErrorLog] = useState("");
  const [projectContext, setProjectContext] = useState("");
  const [result, setResult] = useState<ResultState>({});
  const [activeTab, setActiveTab] = useState<keyof ResultState>("analysis");
  const [language, setLanguage] = useState<Language>("en");
  const [loading, setLoading] = useState("");
  const [error, setError] = useState("");
  const text = copy[language];

  async function parseResponse(response: Response) {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || text.requestFailed);
    }
    return data;
  }

  async function analyze() {
    setError("");
    setLoading(text.loadingAnalyze);
    try {
      let data;
      if (file) {
        const form = new FormData();
        form.append("file", file);
        form.append("error_log", errorLog);
        data = await parseResponse(await fetch(`${API_BASE}/analyze-zip`, { method: "POST", body: form }));
        setProjectContext(data.context_preview || "");
      } else {
        data = await parseResponse(
          await fetch(`${API_BASE}/analyze-text`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ project_notes: projectNotes, error_log: errorLog })
          })
        );
        setProjectContext(projectNotes);
      }
      setResult((current) => ({ ...current, analysis: data.analysis }));
      setActiveTab("analysis");
    } catch (err) {
      setError(err instanceof Error ? err.message : text.unknownError);
    } finally {
      setLoading("");
    }
  }

  async function diagnose() {
    setError("");
    setLoading(text.loadingDiagnose);
    try {
      const data = await parseResponse(
        await fetch(`${API_BASE}/diagnose-error`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ project_context: projectContext || projectNotes || result.analysis || "", error_log: errorLog })
        })
      );
      setResult((current) => ({ ...current, diagnosis: data.diagnosis }));
      setActiveTab("diagnosis");
    } catch (err) {
      setError(err instanceof Error ? err.message : text.unknownError);
    } finally {
      setLoading("");
    }
  }

  async function report() {
    setError("");
    setLoading(text.loadingReport);
    try {
      const data = await parseResponse(
        await fetch(`${API_BASE}/generate-report`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ analysis: result.analysis || projectNotes, diagnosis: result.diagnosis || "" })
        })
      );
      setResult((current) => ({ ...current, report: data.report }));
      setActiveTab("report");
    } catch (err) {
      setError(err instanceof Error ? err.message : text.unknownError);
    } finally {
      setLoading("");
    }
  }

  const activeContent = result[activeTab];

  return (
    <main className="app">
      <section className="workspace">
        <aside className="leftPane">
          <div className="leftPaneScroll">
            <div className="brand">
              <div className="brandIdentity">
                <div className="brandMark"><Sparkles size={22} /></div>
                <div>
                  <h1>RepoPilot Hy3</h1>
                  <p>{text.subtitle}</p>
                </div>
              </div>
              <button className="languageToggle" type="button" onClick={() => setLanguage(language === "en" ? "zh" : "en")}>
                <Languages size={16} />
                {text.switchLanguage}
              </button>
            </div>

            <label className="upload">
              <FileArchive size={20} />
              <span>{file ? file.name : text.upload}</span>
              <input type="file" accept=".zip" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            </label>

            <label className="field">
              <span>{text.projectNotes}</span>
              <textarea value={projectNotes} onChange={(event) => setProjectNotes(event.target.value)} placeholder={text.projectNotesPlaceholder} />
            </label>

            <label className="field">
              <span>{text.errorLog}</span>
              <textarea value={errorLog} onChange={(event) => setErrorLog(event.target.value)} placeholder={text.errorLogPlaceholder} />
            </label>
          </div>

          <div className="leftPaneFooter">
            <div className="actions">
              <button onClick={analyze} disabled={!!loading}>
                <FileText size={18} /> {text.analyze}
              </button>
              <button onClick={diagnose} disabled={!!loading || !errorLog.trim()}>
                <AlertCircle size={18} /> {text.diagnose}
              </button>
              <button onClick={report} disabled={!!loading || !result.analysis}>
                <Clipboard size={18} /> {text.report}
              </button>
            </div>

            {loading && <div className="status"><Loader2 className="spin" size={18} /> {loading}</div>}
            {error && <div className="error">{error}</div>}
          </div>
        </aside>

        <section className="rightPane">
          <div className="resultHeader">
            <div className="tabs">
              {(["analysis", "diagnosis", "report"] as const).map((tab) => (
                <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>
                  {text.tabs[tab]}
                </button>
              ))}
            </div>
            <CopyButton content={activeContent} labels={{ copy: text.copy, copied: text.copied }} />
          </div>
          <MarkdownBlock content={activeContent} emptyText={text.noOutput} />
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
