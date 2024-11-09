from scraper import sort_df
import pandas as pd
import streamlit as st
import plotly.express as px
import os

def load_data():
    """Load the data from the CSV file and preprocess it"""
    df = pd.read_csv('fpl_standings.csv')
    return df

def add_analytics(data):
    """Create analytics visualizations"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Points Distribution
        fig_points = px.bar(data, 
                           x='Team_name', 
                           y='Points',
                           title='Points Distribution',
                           color='Points',
                           color_continuous_scale='Viridis')
        fig_points.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        # Points vs Average
        avg_points = data['Points'].mean()
        data['Points_vs_avg'] = data['Points'] - avg_points
        fig_vs_avg = px.bar(data,
                           x='Team_name',
                           y='Points_vs_avg',
                           title='Points Above/Below Average',
                           color='Points_vs_avg',
                           color_continuous_scale='RdBu')
        fig_vs_avg.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_vs_avg, use_container_width=True)

# def compare_teams(data):
#     """Team comparison feature"""
#     col1, col2 = st.columns(2)
    
#     with col1:
#         team1 = st.selectbox("Select First Team", data['Team_name'].unique(), key='team1')
#     with col2:
#         team2 = st.selectbox("Select Second Team", data['Team_name'].unique(), key='team2')
    
#     if team1 and team2:
#         team1_data = data[data['Team_name'] == team1].iloc[0]
#         team2_data = data[data['Team_name'] == team2].iloc[0]
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric(
#                 team1, 
#                 f"{team1_data['Points']} pts",
#                 f"Rank: {team1_data['Overall Position']}"
#             )
#         with col2:
#             st.metric(
#                 team2, 
#                 f"{team2_data['Points']} pts",
#                 f"Rank: {team2_data['Overall Position']}"
#             )
        
#         points_diff = abs(team1_data['Points'] - team2_data['Points'])
#         st.info(f"Points Difference: {points_diff}")

def compare_teams(data):
    """Team comparison feature with squad screenshots"""
    col1, col2 = st.columns(2)
    
    with col1:
        team1 = st.selectbox("Select First Team", data['Team_name'].unique(), key='team1')
    with col2:
        team2 = st.selectbox("Select Second Team", data['Team_name'].unique(), key='team2')
    
    if team1 and team2:
        team1_data = data[data['Team_name'] == team1].iloc[0]
        team2_data = data[data['Team_name'] == team2].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                team1, 
                f"{team1_data['Points']} pts",
                f"Rank: {team1_data['Overall Position']}"
            )
            # Display team1's squad
            squad_path = f"squads/{team1.replace(' ', '_')}.png"
            if os.path.exists(squad_path):
                st.image(squad_path, caption=f"{team1}'s Squad")
            
        with col2:
            st.metric(
                team2, 
                f"{team2_data['Points']} pts",
                f"Rank: {team2_data['Overall Position']}"
            )
            # Display team2's squad
            squad_path = f"squads/{team2.replace(' ', '_')}.png"
            if os.path.exists(squad_path):
                st.image(squad_path, caption=f"{team2}'s Squad")
        
        points_diff = abs(team1_data['Points'] - team2_data['Points'])
        st.info(f"Points Difference: {points_diff}")

def add_sidebar_stats(data):
    """Add statistics to sidebar"""
    st.sidebar.header("League Statistics")
    
    # League Stats
    with st.sidebar.expander("Current Gameweek Stats"):
        st.write(f"Average Points: {data['Points'].mean():.1f}")
        st.write(f"Highest Points: {data['Points'].max()}")
        st.write(f"Lowest Points: {data['Points'].min()}")
        st.write(f"Points Spread: {data['Points'].max() - data['Points'].min()}")
    
    # Weekly Achievements
    with st.sidebar.expander("Weekly Achievements"):
        # Get weekly winner
        winner = data.loc[data['Points'].idxmax()]
        st.write(f"🏆 Weekly Winner: {winner['Team_name']}")
        
        # Biggest gap to next position
        data['Points_diff'] = data['Points'].diff()
        biggest_gap = data.loc[data['Points_diff'].abs().idxmax()]
        st.write(f"📊 Biggest Gap: {biggest_gap['Team_name']}")

def main():
    """Main application function that displays the FPL standings with enhanced features."""
    st.set_page_config(layout="wide", page_title="1K FPL Standings")
    
    st.title('Standings for Current Gameweek')
    
    # Load and sort data
    data = load_data()
    styled_data = sort_df(data)
    
    # Add sidebar statistics
    add_sidebar_stats(data)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Standings", "Analytics", "Head-to-Head"])
    
    with tab1:
        # Display weekly winners and losers
        col1, col2 = st.columns(2)

        with col1:
            # Display weekly winner
            weekly_winner = data.loc[data['Points'].idxmax()]
            st.success(f"🏆 Oga at the Top: {weekly_winner['Player_name']} ({weekly_winner['Points']} points)")

        with col2:
            # Display weekly loser
            weekly_loser = data.loc[data['Points'].idxmin()]
            st.error(f"😭 Back Bencher: {weekly_loser['Player_name']} ({weekly_loser['Points']} points)")
        
        # Display main standings
        st.dataframe(styled_data, hide_index=True, height=900, use_container_width=True)
    
    with tab2:
        add_analytics(data)
    
    with tab3:
        compare_teams(data)
    
    # Add footer with timestamp
    st.markdown("---")
    st.caption("Last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()