echo "#=============== Starting Scraper ===============#"

# Change to the directory where the script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptPath

# Run the scraper
python scraper.py

# Push the CSV file
git pull
git add fpl_standings.csv
git commit -m "Update FPL standings"
git push origin main

# Pause to keep the window open (optional)
pause