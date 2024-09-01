@echo off

REM Run the scraper
python scraper.py

REM Run the Streamlit app
streamlit run streamlit.py

REM Git commands to push the CSV file
git add fpl_standings.csv
git commit -m "Update FPL standings"
git push origin main

REM Note: Replace 'main' with your branch name if different