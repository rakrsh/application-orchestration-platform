[CmdletBinding()]
param(
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $repoRoot "backend/fastapi"
$frontendDir = Join-Path $repoRoot "frontend"
$logsDir = Join-Path $repoRoot "logs"

function Require-Command {
    param([string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

function Ensure-PythonVenv {
    param([string]$TargetDir)

    $venvDir = Join-Path $TargetDir ".venv"
    if (-not (Test-Path $venvDir)) {
        Write-Host "Creating Python virtual environment in $venvDir"
        & python -m venv $venvDir
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create Python virtual environment."
        }
    }

    $venvPython = Join-Path $venvDir "Scripts/python.exe"
    if (-not (Test-Path $venvPython)) {
        $venvPython = Join-Path $venvDir "bin/python"
    }

    if (-not (Test-Path $venvPython)) {
        throw "Python virtual environment was not created successfully."
    }

    return $venvPython
}

Push-Location $repoRoot
try {
    Require-Command "docker"
    Require-Command "python"
    Require-Command "npm"

    Write-Host "Using repository root: $repoRoot"

    if ($CheckOnly) {
        Write-Host "Check-only mode enabled. Validating prerequisites and commands without starting services."
        Write-Host "- Docker Compose will start the backing services"
        Write-Host "- FastAPI will run from $backendDir"
        Write-Host "- Angular frontend will run from $frontendDir"
        return
    }

    New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

    Write-Host "Starting shared infrastructure services with Docker Compose..."
    & docker compose up -d postgres keycloak openfga oauth2-proxy
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose failed to start the backing services."
    }

    $backendPython = Ensure-PythonVenv -TargetDir $backendDir

    Write-Host "Installing backend dependencies..."
    & $backendPython -m pip install --upgrade pip
    & $backendPython -m pip install -r (Join-Path $backendDir "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install backend requirements."
    }

    if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
        Write-Host "Installing frontend dependencies..."
        & npm install --prefix $frontendDir --no-audit --no-fund
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install frontend dependencies."
        }
    }

    $backendLog = Join-Path $logsDir "backend.log"
    $frontendLog = Join-Path $logsDir "frontend.log"

    Write-Host "Starting FastAPI backend..."
    $backendProcess = Start-Process -FilePath $backendPython -ArgumentList @("-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000") -WorkingDirectory $backendDir -RedirectStandardOutput $backendLog -RedirectStandardError $backendLog -PassThru

    Write-Host "Starting Angular frontend..."
    $frontendProcess = Start-Process -FilePath (Get-Command npm).Source -ArgumentList @("start") -WorkingDirectory $frontendDir -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru

    Write-Host "Development stack started."
    Write-Host "- Frontend: http://localhost:4200"
    Write-Host "- FastAPI docs: http://localhost:8000/docs"
    Write-Host "- Keycloak: http://localhost:8080"
    Write-Host "- OAuth2 Proxy: http://localhost:4180"
    Write-Host "- Backend logs: $backendLog"
    Write-Host "- Frontend logs: $frontendLog"
    Write-Host "- Backend process id: $($backendProcess.Id)"
    Write-Host "- Frontend process id: $($frontendProcess.Id)"
}
finally {
    Pop-Location
}
