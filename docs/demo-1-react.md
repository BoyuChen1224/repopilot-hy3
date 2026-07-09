# Demo 1: React/Vite Project Reproduction

## Goal

Show how RepoPilot Hy3 analyzes a frontend repository and returns a practical run plan.

## Input

Upload `examples/demo-react-app.zip` or paste the files from `examples/demo-react-app`.

## Expected Hy3 Output

- Detects Vite + React from `package.json` and `vite.config.ts`.
- Recommends Node.js and npm setup.
- Suggests `npm install` and `npm run dev`.
- Adds verification steps for the local dev server.
- Calls out likely risks such as Node version mismatch or missing lockfile.

## Demo Script

1. Open the web UI.
2. Upload the demo zip.
3. Click Analyze.
4. Show the evidence-backed checklist.
5. Click Report to generate a Markdown reproduction report.

