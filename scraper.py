import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

options = Options()
# options.add_argument("--headless")
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
    Scrape the Fantasy Premier League website for player information and take squad screenshots.
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
        # Get the player's position and team name
        player_pos.append(int(driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]").text.split('\n')[0]))
        current_team = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]").text.split('\n')[1]
        team_name.append(current_team)

        # Get the player's name
        pn = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]').text.split('\n')[2].split(' ')
        player_name.append(pn[0] + ' ' + pn[1])
        
    # Create squads directory if it doesn't exist
    import os
    if not os.path.exists('squads'):
        os.makedirs('squads')
        
    for i in range(len(links)):
        # Get the player's points and take screenshot
        driver.get(links[i])
        time.sleep(1)
        
        # Get points
        points_for_gw.append(int(driver.find_element(By.XPATH, "//div[contains(@class, 'EntryEvent__PrimaryValue-sc-l17rqm-4 jsdnqB')]").text))
        
        # Take screenshot of the squad
        try:
            squad_element = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div')
            filename = f"squads/{team_name[i].replace(' ', '_')}.png"
            squad_element.screenshot(filename)
            print(f"Saved squad screenshot for {team_name[i]}")
        except Exception as e:
            print(f"Error taking screenshot for {team_name[i]}: {e}")
            
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

def take_squad_screenshot(driver, team_name):
    """
    Take a screenshot of a team's squad
    
    Args:
        driver: Selenium webdriver instance
        team_name: Name of the team for the filename
    """
    try:
        # The squad section XPath in FPL
        squad_xpath = "//div[contains(@class, 'Pitch__PitchElementWrap-sc-1mctasb-4 bWWBeZ')]"
        squad_element = driver.find_element(By.XPATH, squad_xpath)
        
        # Take screenshot and save with team name
        filename = f"squads/{team_name.replace(' ', '_')}.png"
        
        # Create squads directory if it doesn't exist
        import os
        if not os.path.exists('squads'):
            os.makedirs('squads')
            
        # Take and save screenshot
        squad_element.screenshot(filename)
        print(f"Saved squad screenshot: {filename}")
        
    except Exception as e:
        print(f"Error taking screenshot for {team_name}: {e}")

def sort_df(df):
    """
    Sort the DataFrame on the 'Points' column in descending order.

    This function is used to sort the DataFrame on the 'Points' column in
    descending order. The function takes no arguments and returns None.
    """

    # Sort the DataFrame on the 'Points' column in descending order
    df = df.sort_values(by='Points', ascending=False)

    # Create a style function to highlight the highest and lowest points
    def highlight_points(x):
        max_points = df['Points'].max()
        min_points = df['Points'].min()
        return ['background-color: green' if x['Points'] == max_points else 'background-color: red' if x['Points'] == min_points else '' for i in x]

    # Apply the style function to the DataFrame
    styled_df = df.style.apply(highlight_points, axis=1)

    # Print the styled DataFrame
    return styled_df

def run_scraper():
    start()
    player_pos, team_name, player_name, points_for_gw = scrape()
    df = make_df(player_pos=player_pos, team_name=team_name, player_name=player_name, points_for_gw=points_for_gw)
    styled_df = sort_df(df)
    styled_df.data.to_csv('fpl_standings.csv', index=False)

    driver.quit()
if __name__ == "__main__":
    run_scraper()