import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def check_status():
    options = Options()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    driver.get("https://1kgang.streamlit.app")
    time.sleep(10)
    
    driver.get("https://bookies.streamlit.app")        
    time.sleep(10)

    driver.quit()
        
check_status()
