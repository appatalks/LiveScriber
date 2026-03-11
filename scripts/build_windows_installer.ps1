param(
    [string]$PythonExe = ".\.venv\Scripts\python.exe"
)

$ErrorActionPreference = "Stop"

function Write-Info($Message) {
    Write-Host "[INFO]  $Message" -ForegroundColor Cyan
}

function Write-Ok($Message) {
    Write-Host "[OK]    $Message" -ForegroundColor Green
}

function Write-Warn($Message) {
    Write-Host "[WARN]  $Message" -ForegroundColor Yellow
}

function Fail($Message) {
    Write-Host "[FAIL]  $Message" -ForegroundColor Red
    exit 1
}

function Resolve-Python {
    param([string]$Candidate)

    if ($Candidate -and (Test-Path $Candidate)) {
        return (Resolve-Path $Candidate).Path
    }

    $command = Get-Command py -ErrorAction SilentlyContinue
    if ($command) {
        return "py -3.11"
    }

    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    Fail "Python 3.11 was not found. Run scripts/install.ps1 first."
}

function Invoke-Python {
    param(
        [string]$PythonCommand,
        [string[]]$Arguments
    )

    if ($PythonCommand -eq "py -3.11") {
        & py -3.11 @Arguments
        return
    }

    & $PythonCommand @Arguments
}

function Get-IsccPath {
    $command = Get-Command iscc -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
    )

    foreach ($path in $commonPaths) {
        if ($path -and (Test-Path $path)) {
            return $path
        }
    }

    return $null
}

function Get-AppVersion {
    param([string]$PythonCommand)

    $output = Invoke-Python $PythonCommand @("-c", "import livescriber; print(livescriber.__version__)")
    return ($output | Select-Object -Last 1).Trim()
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$python = Resolve-Python $PythonExe
$version = Get-AppVersion $python
$iconPath = Join-Path $projectRoot "assets\livescriber.ico"

if (-not (Test-Path $iconPath)) {
    Fail "App icon was not found at assets\livescriber.ico"
}

Write-Info "Using Python: $python"
Write-Info "Building LiveScriber $version"

Invoke-Python $python @("-m", "pip", "install", "-e", ".[dev]")

$distDir = Join-Path $projectRoot "dist"
$buildDir = Join-Path $projectRoot "build"
if (Test-Path $distDir) {
    Remove-Item $distDir -Recurse -Force
}
if (Test-Path $buildDir) {
    Remove-Item $buildDir -Recurse -Force
}

Write-Info "Running PyInstaller"
Invoke-Python $python @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", "LiveScriber",
    "--icon", $iconPath,
    "--add-data", ".\assets\livescriber.ico;assets",
    "--hidden-import", "sounddevice",
    "--hidden-import", "llama_cpp.llama_chat_format",
    "--hidden-import", "llama_cpp.llama_tokenizer",
    "--collect-submodules", "faster_whisper",
    "--collect-data", "huggingface_hub",
    "--collect-data", "tokenizers",
    "--collect-binaries", "av",
    "--collect-binaries", "ctranslate2",
    "--collect-binaries", "llama_cpp",
    "--collect-binaries", "onnxruntime",
    "--exclude-module", "PyQt6.Qt3DAnimation",
    "--exclude-module", "PyQt6.Qt3DCore",
    "--exclude-module", "PyQt6.Qt3DExtras",
    "--exclude-module", "PyQt6.Qt3DInput",
    "--exclude-module", "PyQt6.Qt3DLogic",
    "--exclude-module", "PyQt6.Qt3DRender",
    "--exclude-module", "PyQt6.QtBluetooth",
    "--exclude-module", "PyQt6.QtCharts",
    "--exclude-module", "PyQt6.QtDataVisualization",
    "--exclude-module", "PyQt6.QtMultimediaQuick",
    "--exclude-module", "PyQt6.QtNetworkAuth",
    "--exclude-module", "PyQt6.QtNfc",
    "--exclude-module", "PyQt6.QtPdf",
    "--exclude-module", "PyQt6.QtPdfWidgets",
    "--exclude-module", "PyQt6.QtPositioning",
    "--exclude-module", "PyQt6.QtQml",
    "--exclude-module", "PyQt6.QtQuick",
    "--exclude-module", "PyQt6.QtQuick3D",
    "--exclude-module", "PyQt6.QtQuickWidgets",
    "--exclude-module", "PyQt6.QtRemoteObjects",
    "--exclude-module", "PyQt6.QtSensors",
    "--exclude-module", "PyQt6.QtSerialPort",
    "--exclude-module", "PyQt6.QtSpatialAudio",
    "--exclude-module", "PyQt6.QtSql",
    "--exclude-module", "PyQt6.QtStateMachine",
    "--exclude-module", "PyQt6.QtSvg",
    "--exclude-module", "PyQt6.QtSvgWidgets",
    "--exclude-module", "PyQt6.QtTextToSpeech",
    "--exclude-module", "PyQt6.QtWebChannel",
    "--exclude-module", "PyQt6.QtWebSockets",
    "--exclude-module", "onnxruntime.quantization",
    "--exclude-module", "onnxruntime.tools",
    "--exclude-module", "onnxruntime.transformers",
    "--exclude-module", "openai.cli",
    "--exclude-module", "openai.resources.beta.realtime",
    "--exclude-module", "openai.resources.realtime",
    "--paths", $projectRoot,
    ".\scripts\windows_launcher.py"
)

Write-Info "Running PyInstaller for transcription helper"
Invoke-Python $python @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--onefile",
    "--console",
    "--name", "LiveScriberTranscriber",
    "--icon", $iconPath,
    "--distpath", ".\dist\LiveScriber",
    "--workpath", ".\build\LiveScriberTranscriber",
    "--specpath", ".\build",
    "--hidden-import", "sounddevice",
    "--collect-submodules", "faster_whisper",
    "--collect-data", "huggingface_hub",
    "--collect-data", "tokenizers",
    "--collect-binaries", "av",
    "--collect-binaries", "ctranslate2",
    "--collect-binaries", "numpy",
    "--collect-binaries", "onnxruntime",
    "--exclude-module", "openai",
    "--exclude-module", "llama_cpp",
    "--exclude-module", "PyQt6",
    "--paths", $projectRoot,
    ".\scripts\windows_transcriber_helper.py"
)

$bundleExe = Join-Path $projectRoot "dist\LiveScriber\LiveScriber.exe"
if (-not (Test-Path $bundleExe)) {
    Fail "PyInstaller did not produce dist\LiveScriber\LiveScriber.exe"
}

$helperExe = Join-Path $projectRoot "dist\LiveScriber\LiveScriberTranscriber.exe"
if (-not (Test-Path $helperExe)) {
    Fail "PyInstaller did not produce dist\LiveScriber\LiveScriberTranscriber.exe"
}

Write-Ok "Built app bundle: $bundleExe"
Write-Ok "Built transcription helper: $helperExe"

$iscc = Get-IsccPath
if (-not $iscc) {
    Write-Warn "Inno Setup was not found. Install Inno Setup 6 to build the .exe installer."
    Write-Warn "The app bundle is ready in dist\LiveScriber"
    exit 0
}

Write-Info "Building installer with Inno Setup"
& $iscc "/DAppVersion=$version" ".\installer\LiveScriber.iss"

$installerDir = Join-Path $projectRoot "dist\installer"
Write-Ok "Installer build complete: $installerDir"