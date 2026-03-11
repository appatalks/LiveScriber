$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir
$venvDir = Join-Path $projectDir ".venv"

function Write-Info($message) {
    Write-Host "[INFO]  $message" -ForegroundColor Cyan
}

function Write-Ok($message) {
    Write-Host "[OK]    $message" -ForegroundColor Green
}

function Write-Warn($message) {
    Write-Host "[WARN]  $message" -ForegroundColor Yellow
}

function Fail($message) {
    Write-Host "[FAIL]  $message" -ForegroundColor Red
    exit 1
}

function Find-Python {
    $commands = @(
        @{ Exe = "py"; Args = @("-3.12") },
        @{ Exe = "py"; Args = @("-3.11") },
        @{ Exe = "py"; Args = @("-3.10") },
        @{ Exe = "python"; Args = @() }
    )

    foreach ($candidate in $commands) {
        $cmd = Get-Command $candidate.Exe -ErrorAction SilentlyContinue
        if (-not $cmd) {
            continue
        }

        try {
            $versionOutput = & $candidate.Exe @($candidate.Args + @("-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")) 2>$null
        }
        catch {
            continue
        }

        if ($LASTEXITCODE -ne 0) {
            continue
        }

        $parts = $versionOutput.Trim().Split('.')
        if ([int]$parts[0] -gt 3 -or ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 10)) {
            return $candidate
        }
    }

    return $null
}

function Test-CommandAvailable($name) {
    return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

function Install-LocalRuntime {
    param(
        [string]$PythonExe
    )

    Write-Info "Installing embedded local summarization runtime..."

    & $PythonExe -m pip install --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu llama-cpp-python
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "Embedded local summarization runtime installed"
        return
    }

    $hasCompiler = (Test-CommandAvailable "cl") -and (Test-CommandAvailable "nmake")
    if (-not $hasCompiler -and (Test-CommandAvailable "winget")) {
        Write-Warn "Prebuilt llama.cpp wheel was not available. Installing Visual Studio Build Tools for a local build..."

        winget install --id Microsoft.VisualStudio.2022.BuildTools --silent --accept-package-agreements --accept-source-agreements --override "--wait --quiet --norestart --nocache --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Build Tools installation did not complete successfully. The embedded local backend will remain unavailable until C++ build tools are installed."
            return
        }

        Write-Info "Retrying embedded local summarization runtime install..."
        & $PythonExe -m pip install llama-cpp-python
        if ($LASTEXITCODE -eq 0) {
            Write-Ok "Embedded local summarization runtime installed"
            return
        }
    }

    Write-Warn "Could not install llama-cpp-python automatically. The app will still work, but the embedded local summarizer will stay unavailable until its runtime is installed."
}

$python = Find-Python
if (-not $python) {
    Fail "Python 3.10+ is required. Install it first."
}

$pythonVersion = & $python.Exe @($python.Args + @("--version"))
Write-Info "Using $($python.Exe) $($python.Args -join ' ') ($pythonVersion)"

if (-not (Test-Path $venvDir)) {
    Write-Info "Creating virtual environment..."
    & $python.Exe @($python.Args + @("-m", "venv", $venvDir))
}
Write-Ok "Virtual environment: $venvDir"

$venvPython = Join-Path $venvDir "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Fail "Virtual environment Python was not created correctly."
}

Write-Info "Upgrading pip..."
& $venvPython -m pip install --upgrade pip

Write-Info "Installing LiveScriber..."
& $venvPython -m pip install -e $projectDir

if ($LASTEXITCODE -ne 0) {
    Fail "LiveScriber installation failed."
}

Install-LocalRuntime -PythonExe $venvPython

$appDir = Join-Path $HOME ".livescriber"
$recordingsDir = Join-Path $appDir "recordings"
New-Item -ItemType Directory -Force -Path $recordingsDir | Out-Null

Write-Host ""
Write-Host "LiveScriber installed successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Activate the environment:"
Write-Host "  $venvDir\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run LiveScriber:"
Write-Host "  livescriber" -ForegroundColor Cyan
Write-Host ""
Write-Host "If PowerShell blocks script execution, run this once in your user scope:" -ForegroundColor Yellow
Write-Host "  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned" -ForegroundColor Cyan