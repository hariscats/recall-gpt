@echo off
:: Script to reliably install dependencies and run the React application
:: Following best practices for Windows environments with path issues

echo ===== AI Learning Assistant Frontend Startup =====

:: Set variables for Node.js paths
set NODE_PATH=C:\Program Files\nodejs
set PATH=%NODE_PATH%;%PATH%
set NODE_EXE="%NODE_PATH%\node.exe"
set NPM_EXE="%NODE_PATH%\npm.cmd"

:: Verify Node.js installation
echo Checking Node.js installation...
%NODE_EXE% --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js not found at %NODE_PATH%
    echo Please ensure Node.js is installed correctly
    exit /b 1
)

:: Display versions
echo Using Node.js version:
%NODE_EXE% --version
echo Using npm version:
%NPM_EXE% --version

:: Install dependencies safely
echo Installing dependencies (ignoring scripts)...
%NPM_EXE% config set ignore-scripts true
%NPM_EXE% install --no-fund

:: Verify react-scripts installation
if not exist "node_modules\react-scripts\bin\react-scripts.js" (
    echo react-scripts not found. Attempting to repair installation...
    %NPM_EXE% install react-scripts@5.0.1 --save-exact --no-fund
    
    if not exist "node_modules\react-scripts\bin\react-scripts.js" (
        echo Error: Failed to install react-scripts. Please check your npm configuration.
        exit /b 1
    )
)

:: Start the application with direct node execution
echo Starting React application...
echo The application will be available at http://localhost:3000
%NODE_EXE% node_modules\react-scripts\bin\react-scripts.js start
