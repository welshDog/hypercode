@echo off
echo 🚀 Launching BROski Bot...
echo --------------------------------
if not exist ".env" (
    echo ❌ ERROR: .env file missing!
    echo 📋 Please copy .env.example to .env and add your tokens.
    pause
    exit /b
)

echo 📦 Checking dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERROR: npm install failed.
    pause
    exit /b
)

echo 🤖 Starting Bot...
node src/index.js
pause
