# Bilingual README Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish synchronized English and Chinese README files that explain RepoPilot Hy3, provide a fast deployment path, and accurately map the project to Tencent-Hunyuan/Hy3 Issue #4.

**Architecture:** Keep `README.md` as the English landing page and `README_CN.md` as its complete Chinese equivalent. Both files will use the upstream Hy3 README's language selector, centered identity, separators, table of contents, task-oriented headings, compact tables, and fenced commands while linking to existing detailed documents instead of duplicating them unnecessarily.

**Tech Stack:** GitHub-flavored Markdown, PowerShell, Windows batch, POSIX shell, FastAPI, React/Vite, Hy3-compatible OpenAI API.

## Global Constraints

- Modify documentation only; do not change application code, startup scripts, dependencies, or demo behavior.
- State that Hy3 is called only through an API and that this project performs no training, fine-tuning, local inference, or local model deployment.
- Document both bundled end-to-end demos and mark the no-longer-than-two-minute video/GIF as pending without adding a fake link.
- Keep commands, paths, ports, endpoints, environment variables, and requirement status identical across the two language versions.
- Preserve both README files as valid UTF-8 and do not expose a real API key.
- Do not add a license section or describe public repository access as an open-source license grant.
- Push the finished commits to the current `origin/main`; do not claim that the separate `Tencent-Hunyuan/Hy3:rhinobird2026` pull request has been created.

---

### Task 1: Rebuild the English README

**Files:**

- Modify: `README.md`

**Interfaces:**

- Consumes: `.env.example`, `start.ps1`, `start.bat`, `start.sh`, `apps/api/app/main.py`, `apps/web/src/main.tsx`, `REQUIREMENTS.md`, `docs/demo-1-react.md`, and `docs/demo-2-python-error.md`.
- Produces: The default project landing page and the canonical facts that `README_CN.md` must localize exactly.

- [ ] **Step 1: Replace the opening and navigation**

  Use `[中文](README_CN.md) | English`, a centered `RepoPilot Hy3` title and subtitle, horizontal separators, and a compact table of contents. The opening must identify the product as a Hy3-powered repository reproduction and error-diagnosis assistant built for Issue #4.

- [ ] **Step 2: Add project and issue context**

  Add `Overview`, `Why RepoPilot Hy3`, and `Issue #4 Checklist` sections. The checklist must report API-only Hy3 integration, the React/Vite frontend, two demo flows, public source availability, and the CodeBuddy disclosure factually, while reporting the video/GIF as “Coming soon.” It must not include a license claim.

- [ ] **Step 3: Document Hy3's role and request flow**

  State that Hy3 performs repository understanding, reproduction planning, error diagnosis, and Markdown report generation. Include this exact conceptual flow:

  ```text
  Developer input -> React web UI -> FastAPI evidence extraction and prompt construction -> Hy3 API -> sanitized, copyable Markdown
  ```

  Explain that archives are path-validated, selected evidence is bounded before API submission, and rendered Markdown is sanitized.

- [ ] **Step 4: Add the developer quickstart**

  Document Python 3.10+, Node.js 18+, an API key, network access, and ports `8000`/`5173`; show copying `.env.example` to `.env`; include the four environment variables; list `start.ps1`, `start.bat`, and `start.sh`; then list web, API, API docs, and health-check URLs.

- [ ] **Step 5: Add verification and manual startup**

  Show `curl http://127.0.0.1:8000/health` with expected response `{"status":"ok"}`. Keep separate backend and frontend commands for developers who need to debug service startup, and link `REQUIREMENTS.md` for full environment notes.

- [ ] **Step 6: Document both demos and pending media**

  Demo 1 must use `examples/demo-react-app.zip` and describe Analyze followed by Report. Demo 2 must use `docs/demo-2-python-error.md` and describe Analyze, Diagnose, and Report. Each must list its input, actions, expected output, and detailed guide. Add a media subsection that says a video or GIF no longer than two minutes will be added later.

- [ ] **Step 7: Retain concise reference material**

  Include project structure, endpoint summary, high-value troubleshooting items, CodeBuddy collaboration areas, security notes, related documents, and the activity submission reminder for the upstream `rhinobird2026` pull request.

- [ ] **Step 8: Review the English README against repository evidence**

  Run:

  ```powershell
  rg -n "HY3_API_KEY|HY3_BASE_URL|HY3_MODEL|VITE_API_BASE_URL|8000|5173|analyze-text|analyze-zip|diagnose-error|generate-report|Coming soon|CodeBuddy|rhinobird2026" README.md
  ```

  Expected: every required configuration value, port, endpoint, pending-media status, collaboration disclosure, and submission branch is present.

### Task 2: Rebuild the Chinese README as a Full Equivalent

**Files:**

- Modify: `README_CN.md`

**Interfaces:**

- Consumes: The completed `README.md` structure and facts.
- Produces: A UTF-8 Chinese landing page with matching commands, links, status values, and technical claims.

- [ ] **Step 1: Mirror the English hierarchy**

  Use `中文 | [English](README.md)`, the same centered identity, separators, table of contents, tables, section order, and code blocks. Translate explanatory prose naturally while keeping product and technical identifiers unchanged.

- [ ] **Step 2: Mirror Issue #4 coverage accurately**

  Mark the interactive frontend, API-only Hy3 usage, two demos, public source availability, and CodeBuddy disclosure factually. Mark the video/GIF as `即将补充`, with no link or completion claim, and do not add a license claim.

- [ ] **Step 3: Mirror quickstart and verification commands exactly**

  Preserve all environment-variable names, values, paths, commands, URLs, ports, API endpoints, JSON, and filenames exactly as they appear in the English README.

- [ ] **Step 4: Mirror demo, safety, and submission guidance**

  Translate the two demo workflows, CodeBuddy collaboration list, security notes, troubleshooting, and the reminder that a later pull request must target `Tencent-Hunyuan/Hy3:rhinobird2026`.

- [ ] **Step 5: Verify UTF-8 and required Chinese copy**

  Run:

  ```powershell
  $utf8 = New-Object System.Text.UTF8Encoding($false, $true)
  $null = $utf8.GetString([System.IO.File]::ReadAllBytes((Resolve-Path 'README_CN.md')))
  rg -n "即将补充|快速开始|Hy3 在系统中的角色|CodeBuddy|rhinobird2026" README_CN.md
  ```

  Expected: UTF-8 decoding succeeds and all required Chinese sections are found.

### Task 3: Validate Bilingual Consistency and Markdown References

**Files:**

- Verify: `README.md`
- Verify: `README_CN.md`

**Interfaces:**

- Consumes: Both completed README files and all relative link targets.
- Produces: Evidence that the documentation is internally consistent and ready to commit.

- [ ] **Step 1: Check the Git diff for whitespace errors**

  Run:

  ```powershell
  git diff --check
  ```

  Expected: exit code `0` with no output.

- [ ] **Step 2: Check for unfinished markers and accidental secrets**

  Run:

  ```powershell
  rg -n "TB[D]|TO[D]O|your_key_here|replace_with_your_hy3_api_key|sk-[A-Za-z0-9]" README.md README_CN.md
  ```

  Expected: no matches. The documented API-key value must be a neutral placeholder such as `your_hy3_api_key` that is not copied from `.env.example`.

- [ ] **Step 3: Verify relative link targets**

  Extract local Markdown link destinations from both README files, ignore anchors and external URLs, strip optional fragments, and confirm every resulting path exists under the repository root.

  Expected: zero missing paths.

- [ ] **Step 4: Compare required literals across languages**

  Verify that both files contain `.env.example`, all four environment variables, all four API endpoints, ports `8000` and `5173`, both demo paths, `CodeBuddy`, and `rhinobird2026`.

  Expected: every required literal appears in both files.

- [ ] **Step 5: Run the existing documentation-adjacent frontend check**

  Run:

  ```powershell
  npm test
  ```

  Working directory: `apps/web`.

  Expected: the UI structure test exits with code `0`.

### Task 4: Commit and Push the Documentation

**Files:**

- Stage: `README.md`
- Stage: `README_CN.md`
- Stage: `docs/superpowers/specs/2026-07-10-bilingual-readme-design.md`
- Stage: `docs/superpowers/plans/2026-07-10-bilingual-readme.md`

**Interfaces:**

- Consumes: Validated documentation and a clean understanding of the intended Git diff.
- Produces: A documentation commit published to `origin/main`.

- [ ] **Step 1: Confirm the final scope**

  Run:

  ```powershell
  git status -sb
  git diff -- README.md README_CN.md docs/superpowers/specs/2026-07-10-bilingual-readme-design.md docs/superpowers/plans/2026-07-10-bilingual-readme.md
  ```

  Expected: only the two README files, the user-approved license clarification in the design spec, and this plan are uncommitted; the original design-spec commit is already in branch history.

- [ ] **Step 2: Stage explicit paths**

  Run:

  ```powershell
  git add -- README.md README_CN.md docs/superpowers/specs/2026-07-10-bilingual-readme-design.md docs/superpowers/plans/2026-07-10-bilingual-readme.md
  ```

- [ ] **Step 3: Commit the README adaptation**

  Run:

  ```powershell
  git commit -m "docs: align bilingual README with Hy3 issue 4"
  ```

  Expected: one commit containing only the intended documentation files.

- [ ] **Step 4: Re-run final verification on committed content**

  Run the UTF-8 check, required-literal comparison, relative-link check, `git diff --check HEAD^ HEAD`, and `npm test` again.

  Expected: all checks exit with code `0`.

- [ ] **Step 5: Push the current branch**

  Run:

  ```powershell
  git push -u origin main
  ```

  Expected: `origin/main` advances to the new documentation commit, including the preceding design-spec commit.
