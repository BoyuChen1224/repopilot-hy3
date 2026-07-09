param(
  [string]$HostAddress = "127.0.0.1",
  [int]$ApiPort = 8000,
  [int]$WebPort = 5173
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ApiDir = Join-Path $Root "apps/api"
$WebDir = Join-Path $Root "apps/web"
$VenvDir = Join-Path $ApiDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts/python.exe"

function Import-DotEnv {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    return
  }

  Get-Content -LiteralPath $Path | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
      return
    }
    $parts = $line -split "=", 2
    $name = $parts[0]
    $value = $parts[1]
    $name = $name.Trim()
    $value = $value.Trim().Trim('"').Trim("'")
    if ($name -and -not [Environment]::GetEnvironmentVariable($name, "Process")) {
      [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
  }
}

function Get-CommandName {
  param([string[]]$Names)
  foreach ($name in $Names) {
    $cmd = Get-Command "$name.cmd" -ErrorAction SilentlyContinue
    if ($cmd) {
      return $cmd.Source
    }
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
      return $cmd.Source
    }
  }
  return $null
}

function Invoke-Step {
  param(
    [string]$Label,
    [scriptblock]$Command
  )
  Write-Host ""
  Write-Host "==> $Label" -ForegroundColor Cyan
  & $Command
  if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

Import-DotEnv (Join-Path $ApiDir ".env")
Import-DotEnv (Join-Path $Root ".env")

if (-not $env:HY3_API_KEY -or $env:HY3_API_KEY -eq "replace_with_your_hy3_api_key") {
  Write-Error "HY3_API_KEY is not configured. Copy .env.example to .env or apps/api/.env, then set your Hy3 API key."
}

$python = Get-CommandName @("py", "python")
if (-not $python) {
  Write-Error "Python was not found. Install Python 3.10+ and retry."
}

if (-not (Test-Path -LiteralPath $VenvPython)) {
  Invoke-Step "Creating backend virtual environment" {
    if ((Split-Path -Leaf $python) -eq "py.exe") {
      & $python -3 -m venv $VenvDir
    } else {
      & $python -m venv $VenvDir
    }
  }
}

Invoke-Step "Installing backend dependencies" {
  & $VenvPython -m pip install -r (Join-Path $ApiDir "requirements.txt")
}

$npm = Get-CommandName @("npm")
$pnpm = Get-CommandName @("pnpm")
$packageManager = $null
$packageArgs = @()

if ((Test-Path -LiteralPath (Join-Path $WebDir "pnpm-lock.yaml")) -and $pnpm) {
  $packageManager = $pnpm
  $packageArgs = @("install")
} elseif ($npm) {
  $packageManager = $npm
  $packageArgs = @("install")
} elseif ($pnpm) {
  $packageManager = $pnpm
  $packageArgs = @("install")
} else {
  Write-Error "Node.js package manager was not found. Install Node.js 18+ with npm, or install pnpm."
}

Invoke-Step "Installing frontend dependencies" {
  Push-Location $WebDir
  try {
    & $packageManager @packageArgs
  } finally {
    Pop-Location
  }
}

$env:VITE_API_BASE_URL = "http://$HostAddress`:$ApiPort"

Write-Host ""
Write-Host "Starting RepoPilot Hy3..." -ForegroundColor Green
Write-Host "API: http://$HostAddress`:$ApiPort"
Write-Host "Web: http://$HostAddress`:$WebPort"
Write-Host "Press Ctrl+C to stop both services."
Write-Host ""

$api = Start-Process -FilePath $VenvPython `
  -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", $HostAddress, "--port", "$ApiPort") `
  -WorkingDirectory $ApiDir `
  -NoNewWindow `
  -PassThru

$webArgs = @("run", "dev", "--", "--host", $HostAddress, "--port", "$WebPort")
$web = Start-Process -FilePath $packageManager `
  -ArgumentList $webArgs `
  -WorkingDirectory $WebDir `
  -NoNewWindow `
  -PassThru

try {
  while (-not $api.HasExited -and -not $web.HasExited) {
    Start-Sleep -Seconds 1
  }
} finally {
  foreach ($process in @($api, $web)) {
    if ($process -and -not $process.HasExited) {
      Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
  }
}
