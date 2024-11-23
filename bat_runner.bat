@echo off
setlocal EnableDelayedExpansion

:: Set paths
set "PROJECT_PATH=C:\Users\NUDDY\Documents\GitHub\fpl"
set "PYTHON_SCRIPT=scraper.py"
set "LOG_FILE=scraper_log.txt"

:: Change to project directory
cd /d "%PROJECT_PATH%"

:: Get current date and time for logging
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "TIMESTAMP=%dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%:%dt:~12,2%"

:: Log start
echo [%TIMESTAMP%] Starting scraper... >> "%LOG_FILE%"

:: Kill any existing Firefox processes
taskkill /F /IM firefox.exe /T 2>nul
taskkill /F /IM geckodriver.exe /T 2>nul

:: Run Python script
python "%PYTHON_SCRIPT%"
if errorlevel 1 (
    echo [%TIMESTAMP%] Error running scraper >> "%LOG_FILE%"
    exit /b 1
) else (
    echo [%TIMESTAMP%] Scraper completed successfully >> "%LOG_FILE%"
)

:: Kill Firefox processes again after completion
timeout /t 5 /nobreak
taskkill /F /IM firefox.exe /T 2>nul
taskkill /F /IM geckodriver.exe /T 2>nul

:: Git operations
git pull
git add fpl_standings.csv
git commit -m "Update FPL standings [%TIMESTAMP%]"
git push origin main

echo [%TIMESTAMP%] Process completed >> "%LOG_FILE%"
exit /b 0