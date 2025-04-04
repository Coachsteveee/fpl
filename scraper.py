import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

options = Options()
options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Firefox(options=options)
driver.maximize_window()

def start():
    """
    Open the Fantasy Premier League website and close the consent popup.

    This function is used to start the process of scraping the Fantasy Premier
    League website. It opens the website in the Firefox browser and closes the
    consent popup that appears when the website is first opened.
    """
    # Open the Fantasy Premier League website
    driver.get('https://fantasy.premierleague.com/leagues/340359/standings/c')
    time.sleep(1)
    # Close the consent popup
    try:
        consent_popup_element = driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
        consent_popup_element.click()
    except NoSuchElementException:
        pass
    
def scrape():
    """
    Scrape the Fantasy Premier League website for player information.

    This function is used to scrape the Fantasy Premier League website for player
    information. The information scraped includes the player's position, team name,
    and points for the current gameweek.

    The function returns None.
    """

    # Lists to store the player information
    player_pos = []
    team_name = []
    player_name = []
    points_for_gw = []
    links = []

    for i in range(1, 25):
        links.append(driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]/a").get_attribute('href'))
    
    # Iterate over the rows of the table
    for i in range(1, 25):
        # Get the player's position and team name          //div[contains(@class, 'sc-bdnxRM hItLLq')]
        player_pos.append(int(driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]").text.split('\n')[0]))
        team_name.append(driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]").text.split('\n')[1])

        # Get the player's name
        # The name is in the format 'First Name, Last Name'
        # So we need to split the string and join the two parts together with a space in between
        pn = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]').text.split('\n')[2].split(' ')
        player_name.append(pn[0] + ' ' + pn[1])

        
    for i in range(len(links)):
        # Get the player's points for the current gameweek
        driver.get(links[i])
        time.sleep(1)
        points_for_gw.append(int(driver.find_element(By.XPATH, "//div[contains(@class, 'EntryEvent__PrimaryValue-sc-l17rqm-4 jsdnqB')]").text))
        time.sleep(1)    
    return player_pos, team_name, player_name, points_for_gw

def make_df(player_pos, team_name, player_name, points_for_gw):
    """
    Create a DataFrame with the specified columns.

    This function takes four lists as arguments: player_pos, team_name, player_name,
    and points_for_gw. It creates a DataFrame with four columns: Position, Team_name,
    Player_name, and Points. It then fills up the DataFrame using the lists.

    The function returns the DataFrame.
    """
    # Create a DataFrame with the specified columns
    df = pd.DataFrame({
        'Overall Position': [],
        'Team_name': [],
        'Player_name': [],
        'Points': []
    })

    # Fill up the DataFrame using lists
    # For example:
    position_list = player_pos
    team_name_list = team_name
    player_name_list = player_name
    points_list = points_for_gw

    df['Overall Position'] = position_list
    df['Team_name'] = team_name_list
    df['Player_name'] = player_name_list
    df['Points'] = points_list

    # Return the DataFrame
    return df

def run_scraper():
    start()
    player_pos, team_name, player_name, points_for_gw = scrape()
    df = make_df(player_pos=player_pos, team_name=team_name, player_name=player_name, points_for_gw=points_for_gw).sort_values(by='Points', ascending=False)
    # styled_df = sort_df(df)
    print(df)
    df.to_csv('fpl_standings.csv', index=False)

    driver.quit()
    
if __name__ == "__main__":
    run_scraper()