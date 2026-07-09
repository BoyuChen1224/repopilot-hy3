# Requirements

RepoPilot Hy3 includes one-click startup scripts, but a fresh computer still needs a small set of system dependencies before those scripts can run.

## System Requirements

- Operating system:
  - Windows 10/11 with PowerShell 5+ or Command Prompt
  - macOS or Linux with a POSIX-compatible `sh`
- Python 3.10+ with `venv` and `pip`
- Node.js 18+ with `npm`
- Network access to:
  - PyPI, for backend Python packages
  - npm registry, for frontend packages
  - `https://tokenhub.tencentmaas.com/v1`, for Hy3 API calls
- A Hy3-compatible API key
- Available local ports:
  - `8000` for the FastAPI backend
  - `5173` for the Vite frontend

Git is recommended for cloning and updating the project, but it is not required if the source code is downloaded as a zip.

## Project Dependencies

Backend Python dependencies are declared in:

```text
apps/api/requirements.txt
```

For convenience, the repository root also contains:

```text
requirements.txt
```

It delegates to `apps/api/requirements.txt`, so developers can install backend dependencies from either location.

Frontend JavaScript dependencies are declared in:

```text
apps/web/package.json
```

The startup scripts install these project dependencies automatically:

- Windows PowerShell: `start.ps1`
- Windows Command Prompt: `start.bat`
- macOS / Linux: `start.sh`

## Hy3 Configuration

Create `.env` in the repository root or `apps/api/.env`:

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Do not commit real API keys.

## Quick Checks

Run these commands before using one-click startup on a new machine:

```bash
python --version
node --version
npm --version
```

On macOS or Linux, `python3 --version` is also acceptable because `start.sh` checks `python3` first.

If any command is missing, install the corresponding system dependency before running the startup script.
