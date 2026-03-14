@echo off
echo ========================================
echo Deploying EXTREME Version to GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo Adding all updated files...
git add .

echo Committing changes...
git commit -m "Upgrade to EXTREME difficulty - 4 salts, 4 layers, decoy flags, precise timing"

echo Pushing to GitHub...
git push

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Render will automatically deploy the new version.
echo Wait ~3 minutes for deployment to complete.
echo.
echo Changes:
echo   - 4 salts instead of 1
echo   - 4-layer HMAC token generation
echo   - 4 required headers (was 2)
echo   - 3 decoy flags
echo   - Even second requirement
echo   - Minute range 5-14 only
echo   - 12 layers base64 + XOR + Base85 + Base32
echo   - 30-second timing window (was 60)
echo.
echo Difficulty: EXTREME (750 points)
echo Solve Time: 4-8 hours
echo.
echo Test with: python solution.py https://your-app.onrender.com
echo (Must run during 2:00-2:20 PM IST)
echo ========================================
pause
