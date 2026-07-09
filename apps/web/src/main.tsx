import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertCircle, Check, Clipboard, Copy, FileArchive, FileText, Loader2, Sparkles } from "lucide-react";
import { marked } from "marked";
import DOMPurify from "dompurify";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type ResultState = {
  analysis?: string;
  diagnosis?: string;
  report?: string;
};

function MarkdownBlock({ content }: { content?: string }) {
  const html = useMemo(() => DOMPurify.sanitize(marked.parse(content || "No output yet.") as string), [content]);
  return <div className="markdown" dangerouslySetInnerHTML={{ __html: html }} />;
}

function CopyButton({ content }: { content?: string }) {
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
      {copied ? "Copied" : "Copy"}
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
  const [loading, setLoading] = useState("");
  const [error, setError] = useState("");

  async function parseResponse(response: Response) {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    return data;
  }

  async function analyze() {
    setError("");
    setLoading("Analyzing with Hy3...");
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
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading("");
    }
  }

  async function diagnose() {
    setError("");
    setLoading("Diagnosing error log...");
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
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading("");
    }
  }

  async function report() {
    setError("");
    setLoading("Generating report...");
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
      setError(err instanceof Error ? err.message : "Unknown error");
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
              <div className="brandMark"><Sparkles size={22} /></div>
              <div>
                <h1>RepoPilot Hy3</h1>
                <p>Repository reproduction and error diagnosis assistant.</p>
              </div>
            </div>

            <label className="upload">
              <FileArchive size={20} />
              <span>{file ? file.name : "Upload project .zip"}</span>
              <input type="file" accept=".zip" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            </label>

            <label className="field">
              <span>Project notes or README</span>
              <textarea value={projectNotes} onChange={(event) => setProjectNotes(event.target.value)} placeholder="Paste README, file tree, package.json, or setup notes..." />
            </label>

            <label className="field">
              <span>Error log</span>
              <textarea value={errorLog} onChange={(event) => setErrorLog(event.target.value)} placeholder="Paste terminal errors, stack traces, or failed install output..." />
            </label>
          </div>

          <div className="leftPaneFooter">
            <div className="actions">
              <button onClick={analyze} disabled={!!loading}>
                <FileText size={18} /> Analyze
              </button>
              <button onClick={diagnose} disabled={!!loading || !errorLog.trim()}>
                <AlertCircle size={18} /> Diagnose
              </button>
              <button onClick={report} disabled={!!loading || !result.analysis}>
                <Clipboard size={18} /> Report
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
                  {tab}
                </button>
              ))}
            </div>
            <CopyButton content={activeContent} />
          </div>
          <MarkdownBlock content={activeContent} />
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
