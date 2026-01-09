@echo off
REM HyperCode Research Docs Setup Script (Windows)
REM Version 1.0.0

echo 🚀 HyperCode Research Setup Initiated...
echo ----------------------------------------

REM 1. Create Directory
if not exist "docs\RESEARCH" (
    echo 📂 Creating docs\RESEARCH directory...
    mkdir "docs\RESEARCH"
) else (
    echo ✅ Directory docs\RESEARCH exists.
)

REM 2. Check/Move Files
REM Windows batch is simpler - we just try to move if they exist in root.

if exist "HyperCode_Project_Understanding.md" move "HyperCode_Project_Understanding.md" "docs\RESEARCH\"
if exist "HyperCode_DEEP_DIVE.md" move "HyperCode_DEEP_DIVE.md" "docs\RESEARCH\"
if exist "QUANTUM_ALGORITHMS_SUPER_DEEP_DIVE.md" move "QUANTUM_ALGORITHMS_SUPER_DEEP_DIVE.md" "docs\RESEARCH\"
if exist "QUANTUM_QUICK_REFERENCE.md" move "QUANTUM_QUICK_REFERENCE.md" "docs\RESEARCH\"
if exist "GITHUB_SETUP_GUIDE.md" move "GITHUB_SETUP_GUIDE.md" "docs\RESEARCH\"
if exist "INTEGRATION_READY_SUMMARY.md" move "INTEGRATION_READY_SUMMARY.md" "docs\RESEARCH\"
if exist "README_FOR_GITHUB_PUSH.md" move "README_FOR_GITHUB_PUSH.md" "docs\RESEARCH\"

echo ✅ File organization checks complete.

REM 3. Final Verification
echo ----------------------------------------
echo 🔍 Verifying Manifest...
dir "docs\RESEARCH\*.md" /b

echo.
echo 🎉 SETUP COMPLETE! Your research docs are ready.
echo 👉 Next Step: git add docs/RESEARCH/
pause
