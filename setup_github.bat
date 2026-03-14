@echo off
echo ========================================
echo Setting up GitHub Repository
echo ========================================
echo.

cd /d "%~dp0"

echo Creating README.md...
echo # love-pagal-haiiiiiii > README.md

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Committing files...
git commit -m "first commit"

echo Setting main branch...
git branch -M main

echo Adding remote origin...
git remote add origin https://github.com/love-is-fakebau/love-pagal-haiiiiiii.git

echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Done! Repository pushed to GitHub
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://render.com
echo 2. Click "New +" -^> "Blueprint"
echo 3. Connect your GitHub repo
echo 4. Render will auto-detect render.yaml
echo 5. Click "Apply"
echo.
echo Your app will be live in ~3 minutes!
echo ========================================
pause
