# Hy3 Role in RepoPilot

RepoPilot Hy3 treats Hy3 as a repository reproduction agent rather than a generic chatbot.

## Responsibilities

- Parse natural-language setup notes and extracted repository evidence.
- Infer framework, package manager, runtime, and likely entry points.
- Generate a runnable plan with evidence from files.
- Diagnose install/runtime errors from logs.
- Convert analysis into a reproducibility report.

## Prompting Principles

- Ask Hy3 to ground every major claim in the provided evidence.
- Prefer actionable commands over broad advice.
- Separate confirmed facts from assumptions.
- Keep missing evidence explicit.

