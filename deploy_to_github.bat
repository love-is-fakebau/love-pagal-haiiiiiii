@echo off
echo ========================================
echo Deploy "Love Is Simple" to GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Initialize Git Repository
git init

echo.
echo Step 2: Add all files
git add .

echo.
echo Step 3: Create initial commit
git commit -m "Initial commit - Love Is Simple CTF Challenge by MD"

echo.
echo Step 4: Set main branch
git branch -M main

echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Name it: love-is-simple-ctf
echo.
echo 3. Run this command (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/love-is-simple-ctf.git
echo.
echo 4. Push to GitHub:
echo    git push -u origin main
echo.
echo 5. Then deploy on Render.com:
echo    - Go to https://render.com
echo    - Click "New +" -^> "Web Service"
echo    - Connect your GitHub repository
echo    - Configure and deploy!
echo.
echo See DEPLOY_RENDER.md for detailed instructions.
echo.
pause
