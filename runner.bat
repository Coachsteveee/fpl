@echo off

REM #---------------------Running the scraper
python scraper.py
REM #---------------------finished running scraper

REM push the CSV file
git pull
git add fpl_standings.csv
git commit -m "Update FPL standings"
git push origin main