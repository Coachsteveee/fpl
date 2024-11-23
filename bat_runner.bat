@echo off
setlocal EnableDelayedExpansion

:: Force console window to stay visible
title FPL Scraper Runner

:: Configuration
set "PROJECT_PATH=C:\Users\NUDDY\Documents\GitHub\fpl"
set "PYTHON_SCRIPT=scraper.py"
set "LOG_FILE=scraper_log.txt"

:: Change to project directory
cd /d "%PROJECT_PATH%"

:: Get current date and time for logging
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "TIMESTAMP=%dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%:%dt:~12,2%"

:: Make output more visible
color 0A
cls
echo ========================================
echo          FPL SCRAPER STARTING
echo ========================================
echo Time: %TIMESTAMP%
echo.

:: Log start
echo [%TIMESTAMP%] Starting scraper... >> "%LOG_FILE%"
echo [%TIMESTAMP%] Starting scraper...

:: Single cleanup before starting
echo Cleaning up existing processes...
taskkill /F /IM firefox.exe /T >nul 2>&1
taskkill /F /IM geckodriver.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

:: Run Python script
echo.
echo Running Python scraper...
python "%PYTHON_SCRIPT%"
if errorlevel 1 (
    color 0C
    echo.
    echo [%TIMESTAMP%] Error running scraper >> "%LOG_FILE%"
    echo ERROR: Scraper failed to run correctly
    echo See log file for details: %LOG_FILE%
    echo.
    echo Press any key to close...
    pause > nul
    exit /b 1
)

:: Clean up after script completion
echo.
echo Cleaning up after scraper...
taskkill /F /IM firefox.exe /T >nul 2>&1
taskkill /F /IM geckodriver.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

:: Git operations
echo.
echo Running git operations...
git pull
if errorlevel 1 goto :error
git add fpl_standings.csv
if errorlevel 1 goto :error
git commit -m "Update FPL standings [%TIMESTAMP%]"
if errorlevel 1 goto :error
git push origin main
if errorlevel 1 goto :error

echo.
echo [%TIMESTAMP%] Process completed successfully >> "%LOG_FILE%"
echo ========================================
echo      FPL Scraper Run Complete
echo ========================================
echo Time: %TIMESTAMP%
echo.
echo Results have been saved and pushed to git
echo Check %LOG_FILE% for detailed logs
echo.
echo Window will close in 10 seconds...
timeout /t 10
exit /b 0

:error
color 0C
echo.
echo [%TIMESTAMP%] Error during git operations >> "%LOG_FILE%"
echo ERROR: Git operations failed
echo See log file for details: %LOG_FILE%
echo.
echo Window will close in 10 seconds...
timeout /t 10
exit /b 1