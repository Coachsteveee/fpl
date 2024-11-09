from scraper import sort_df
import pandas as pd
import streamlit as st

def load_data():
    # Load the data from the CSV file or database
    df = pd.read_csv('fpl_standings.csv')
    return df


def main():
    """
    The main entry point of the script.

    This function displays the DataFrame in a Streamlit web page.
    """
    # Display the title of the web page
    st.title('1K FPL Standings for Current Gameweek')
    
    # Load the data from the CSV file or database
    data = load_data()
    
    # Sort and style the DataFrame
    styled_data = sort_df(data)

    # Display the DataFrame in a Streamlit web page
    st.dataframe(styled_data, hide_index=True, height=900, use_container_width=True)
    
if __name__ == "__main__":
    main()