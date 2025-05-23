# Script to install dependencies and run the React application
# Following best practices for Windows environments with path resolution issues
$ErrorActionPreference = "Stop"

# Ensure Node.js is in the path for this session
$nodePath = "C:\Program Files\nodejs"
$env:PATH = "$nodePath;$env:PATH"
$nodeExe = Join-Path -Path $nodePath -ChildPath "node.exe"
$npmExe = Join-Path -Path $nodePath -ChildPath "npm.cmd"

# Check if node is available
try {
    Write-Host "Using Node.js version: $(&$nodeExe --version)" -ForegroundColor Cyan
    Write-Host "Using npm version: $(&$npmExe --version)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Node.js installation not found at $nodePath" -ForegroundColor Red
    Write-Host "Please ensure Node.js is installed and the path is correct" -ForegroundColor Red
    exit 1
}

# Install dependencies safely
Write-Host "Installing dependencies (ignoring scripts)..." -ForegroundColor Cyan
&$npmExe config set ignore-scripts true
&$npmExe install --no-fund

# Check if node_modules\react-scripts exists 
$reactScriptsPath = ".\node_modules\react-scripts\bin\react-scripts.js"
if (-not (Test-Path $reactScriptsPath)) {
    Write-Host "Error: react-scripts not found. Trying to repair installation..." -ForegroundColor Yellow
    &$npmExe install react-scripts@5.0.1 --save-exact --no-fund
    
    if (-not (Test-Path $reactScriptsPath)) {
        Write-Host "Error: Failed to install react-scripts. Please check your npm configuration." -ForegroundColor Red
        exit 1
    }
}

# Start the application with direct node execution to avoid path issues
Write-Host "Starting React application..." -ForegroundColor Green
Write-Host "The application will be available at http://localhost:3000" -ForegroundColor Cyan
&$nodeExe $reactScriptsPath start
