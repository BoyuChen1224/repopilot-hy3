@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "API_DIR=%ROOT%\apps\api"
set "WEB_DIR=%ROOT%\apps\web"
set "VENV_DIR=%API_DIR%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "HOST=127.0.0.1"
set "API_PORT=8000"
set "WEB_PORT=5173"

call :load_env "%API_DIR%\.env"
call :load_env "%ROOT%\.env"

if "%HY3_API_KEY%"=="" (
  echo HY3_API_KEY is not configured.
  echo Copy .env.example to .env or apps\api\.env, then set your Hy3 API key.
  exit /b 1
)

if "%HY3_API_KEY%"=="replace_with_your_hy3_api_key" (
  echo HY3_API_KEY is still the placeholder value.
  echo Update .env or apps\api\.env with your real Hy3 API key.
  exit /b 1
)

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python was not found. Install Python 3.10+ and retry.
    exit /b 1
  )
  set "PY_CMD=python"
)

if not exist "%VENV_PYTHON%" (
  echo.
  echo ==^> Creating backend virtual environment
  %PY_CMD% -m venv "%VENV_DIR%"
  if errorlevel 1 exit /b 1
)

echo.
echo ==^> Installing backend dependencies
"%VENV_PYTHON%" -m pip install -r "%API_DIR%\requirements.txt"
if errorlevel 1 exit /b 1

set "PM_CMD="
if exist "%WEB_DIR%\pnpm-lock.yaml" (
  where pnpm >nul 2>nul
  if %errorlevel%==0 set "PM_CMD=pnpm"
)
if "%PM_CMD%"=="" (
  where npm >nul 2>nul
  if %errorlevel%==0 set "PM_CMD=npm"
)
if "%PM_CMD%"=="" (
  where pnpm >nul 2>nul
  if %errorlevel%==0 set "PM_CMD=pnpm"
)
if "%PM_CMD%"=="" (
  echo Node.js package manager was not found. Install Node.js 18+ with npm, or install pnpm.
  exit /b 1
)

echo.
echo ==^> Installing frontend dependencies
pushd "%WEB_DIR%"
%PM_CMD% install
if errorlevel 1 exit /b 1
popd

set "VITE_API_BASE_URL=http://%HOST%:%API_PORT%"

echo.
echo Starting RepoPilot Hy3...
echo API: http://%HOST%:%API_PORT%
echo Web: http://%HOST%:%WEB_PORT%
echo Close both opened windows to stop the project.
echo.

start "RepoPilot Hy3 API" /D "%API_DIR%" cmd /k ""%VENV_PYTHON%" -m uvicorn app.main:app --host %HOST% --port %API_PORT%"
start "RepoPilot Hy3 Web" /D "%WEB_DIR%" cmd /k "set "VITE_API_BASE_URL=%VITE_API_BASE_URL%" && %PM_CMD% run dev -- --host %HOST% --port %WEB_PORT%"

exit /b 0

:load_env
if not exist "%~1" exit /b 0
for /f "usebackq eol=# tokens=1,* delims==" %%A in ("%~1") do (
  if not "%%A"=="" (
    if not defined %%A set "%%A=%%~B"
  )
)
exit /b 0
