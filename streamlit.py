import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import streamlit as st

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome()

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
    consent_popup_element = driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
    consent_popup_element.click()

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

    # Iterate over the rows of the table
    for i in range(1, 25):
        # Get the player's position and team name
        player_pos.append(int(driver.find_element(By.XPATH, f'//div[5]/table/tbody/tr[{i}]').text.split('\n')[0]))
        team_name.append(driver.find_element(By.XPATH, f'//div[5]/table/tbody/tr[{i}]').text.split('\n')[1])

        # Get the player's name
        # The name is in the format 'First Name, Last Name'
        # So we need to split the string and join the two parts together with a space in between
        pn = driver.find_element(By.XPATH, f'//div[5]/table/tbody/tr[{i}]').text.split('\n')[2].split(' ')
        player_name.append(pn[0] + ' ' + pn[1])

        # Get the player's points for the current gameweek
        points_for_gw.append(driver.find_element(By.XPATH, f'//div[5]/table/tbody/tr[{i}]').text.split('\n')[2].split(' ')[-2])
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

def sort_df(df) -> None:
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
    
def main():
    try:
        # time.sleep()
        start()
        player_pos, team_name, player_name, points_for_gw = scrape()
        df = make_df(player_pos=player_pos, team_name=team_name, player_name=player_name, points_for_gw=points_for_gw)
        styled_df = sort_df(df)
        
        st.title('1K FPL Standings for Current Gameweek')
        
        st.dataframe(styled_df, hide_index=True, width=800, height=900, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
if __name__ == "__main__":
    main()