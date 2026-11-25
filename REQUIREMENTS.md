# Requirements

RepoPilot Hy3 includes one-click startup scripts, but a fresh computer still needs a small set of system dependencies before those scripts can run.

## System Requirements

- Operating system:
  - Windows 10/11 with PowerShell 5+ or Command Prompt
  - macOS or Linux with a POSIX-compatible `sh`
- Python 3.11+ with `venv` and `pip`
- Node.js 18+ with `npm`
- Network access to:
  - PyPI, for backend Python packages
  - npm registry, for frontend packages
  - `https://tokenhub.tencentmaas.com/v1`, for model API calls
- A compatible model API key
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

## Model Configuration

Create `.env` in the repository root or `apps/api/.env`:

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy4-flash
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

## npm Script Approval Warning

Some npm versions may print this warning while installing frontend dependencies:

```text
npm warn allow-scripts 1 package has install scripts not yet covered by allowScripts:
npm warn allow-scripts   esbuild@... (install: (install scripts present))
```

This is a security warning, not an install failure. If the Vite frontend starts normally, no action is needed.

If Vite later fails with an `esbuild` error, approve the script once:

```bash
cd apps/web
npm approve-scripts --allow-scripts-pending
```

Select and approve `esbuild`, then run the startup script again.

## WSL `.env` line ending error

If WSL prints an error like this when running `./start.sh`:

```text
: not found 5: /path/to/repopilot-hy3/.env:
```

Check the `.env` syntax and convert it to Linux line endings if needed:

```bash
sed -i 's/\r$//' .env
```
