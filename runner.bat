@echo off

REM #---------------------Running the scraper
python scraper.py
REM #---------------------finished running scraper

REM #---------------------Running the Streamlit app
streamlit run streamlit.py

REM #---------------------Git commands to push the CSV file
git add fpl_standings.csv
git commit -m "Update FPL standings"
git push origin main

