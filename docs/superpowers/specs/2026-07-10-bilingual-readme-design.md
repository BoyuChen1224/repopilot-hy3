# Bilingual README Adaptation Design

## Objective

Restructure the English and Chinese README files so developers can quickly understand RepoPilot Hy3, deploy it on a supported platform, and verify its two end-to-end workflows. The documentation must also make the project's relationship to Tencent-Hunyuan/Hy3 Issue #4 explicit and follow the presentation style of the upstream Hy3 repository.

## Scope

The implementation will update `README.md` and `README_CN.md` as synchronized language variants. Existing supporting documents may be linked, but application code, startup scripts, dependencies, and demo behavior will not be changed.

The repository currently has no demo video or GIF. Both README files will therefore reserve a clearly labeled media section stating that the recording will be added later. They will not contain a fake URL or claim that the media requirement is complete.

## Audience and Reading Order

The primary audience is a developer encountering the project for the first time. The secondary audience is a reviewer checking the project against Issue #4.

Both language versions will follow this reading order:

1. Language switch, centered project identity, and concise project positioning.
2. Table of contents.
3. Project overview and the problem it solves.
4. Issue #4 requirement mapping.
5. Hy3's role and the end-to-end request flow.
6. Features and project structure.
7. Quick deployment and verification.
8. Two end-to-end demo workflows and the pending media notice.
9. API reference, troubleshooting, CodeBuddy collaboration disclosure, security notes, and related links.

## Upstream Style Adaptation

The README files will reuse the upstream Hy3 repository's documentation conventions without copying model-specific content:

- A language selector at the top.
- A centered project title and one-sentence description.
- Horizontal separators around the main navigation area.
- A compact table of contents before detailed sections.
- Direct, task-oriented section names such as Quickstart, Deployment, and Demo.
- Short paragraphs, concise tables, fenced commands, and links to deeper documentation.

No badge or section will claim a license, release, test result, or compatibility status that is not evidenced by the repository.

## Issue #4 Coverage

The README requirement table will state the following accurately:

| Requirement | Repository evidence | Documentation treatment |
| --- | --- | --- |
| Hy3 is called through an API | FastAPI backend calls the configured Hy3-compatible endpoint | Explain configuration and request flow; state that there is no training, fine-tuning, or local inference |
| Interactive frontend | React/Vite web application | Link the local web URL and describe the main interactions |
| Two end-to-end demos | React repository analysis and Python error diagnosis examples | Provide exact inputs, actions, expected outputs, and supporting document links |
| Video or GIF no longer than two minutes | Not yet available | Show an explicit “coming soon” notice without a dead link |
| Public project source and stated Hy3 role | Public repository and backend integration | Describe source availability and add dedicated Hy3 role and architecture sections; do not add a license section or imply that public access grants a license |
| CodeBuddy collaboration disclosure is encouraged | Repository implementation and documentation were produced collaboratively | Add a factual list of collaboratively completed areas without inventing line-level attribution |

The documentation will distinguish between implemented requirements and the pending media deliverable.

## Quick Deployment Design

Quick deployment will appear before manual API details. It will include:

- Python 3.10+, Node.js 18+, network access, API credentials, and free ports `8000` and `5173`.
- Copying `.env.example` to `.env` and setting `HY3_API_KEY`, `HY3_BASE_URL`, `HY3_MODEL`, and `VITE_API_BASE_URL`.
- One-click commands for PowerShell, Command Prompt, and macOS/Linux.
- The resulting API, API documentation, health-check, and web addresses.
- A minimal verification sequence: call `/health`, open the web UI, and run one bundled demo.
- A link to `REQUIREMENTS.md` for environment-specific troubleshooting.

Manual backend and frontend startup commands will remain available but will be visually secondary to the one-click path.

## Hy3 Role and Request Flow

The README files will explain that Hy3 is the application's reasoning engine. The local application extracts repository evidence, sends selected context and user-provided logs to a Hy3-compatible API, and renders structured results. Hy3 performs repository understanding, setup planning, error diagnosis, and report generation.

The documented flow will be:

`Developer input -> React web UI -> FastAPI evidence extraction and prompt construction -> Hy3 API -> sanitized, copyable result`

The text will explicitly state that the project does not train, fine-tune, or locally deploy Hy3.

## Demo Documentation

Demo 1 will use `examples/demo-react-app.zip`. Its documented outcome will include detected stack information, runnable commands, risks, and verification steps.

Demo 2 will use the context and error log documented under `docs/demo-2-python-error.md`. Its documented outcome will include the likely root cause, repair commands, and a verification checklist.

Each demo will identify its input, user action, expected output, and detailed guide. A separate media subsection will state that the no-longer-than-two-minute recording or GIF is pending.

## Bilingual Consistency

The English README will be the default landing page and the Chinese README will be a complete localized equivalent, not a summary. Headings, commands, paths, URLs, requirement statuses, and factual claims must match across both files. Product names and identifiers such as Hy3, RepoPilot Hy3, FastAPI, React, Vite, API paths, and environment variable names will remain unchanged.

The Chinese file must be valid UTF-8 and render without mojibake.

## Validation

Before publishing, the implementation will verify:

- Both README files are valid UTF-8.
- Relative links resolve to tracked files.
- Required commands, environment variables, ports, endpoints, and demo paths agree with the repository.
- Both language versions contain equivalent Issue #4 coverage and the pending media notice.
- No unfinished marker, fake link, secret, or unsupported completion claim appears.
- The Git diff contains only intended documentation changes before staging.

## Publishing

After validation, the README implementation will be committed on the current `main` branch and pushed to `origin`. This repository push does not create the separate contribution pull request targeting `Tencent-Hunyuan/Hy3:rhinobird2026`, which remains a later submission step.
