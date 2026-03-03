import streamlit as st
import pandas as pd

st.title("📊 Team Performance Analysis")

# Load dataset
matches = pd.read_csv("data/matches.csv")

st.success("Dataset Loaded Successfully!")

# Basic Info
st.subheader("Basic IPL Dataset Information")

total_matches = matches.shape[0]
teams = matches['team1'].unique()

st.write("Total Matches Played:", total_matches)
st.write("Total Teams:", len(teams))

# Show first few rows
st.subheader("Preview of Matches Dataset")
st.dataframe(matches.head())
# Team wins count
st.subheader("🏆 Team Wins Count")

wins = matches['winner'].value_counts()
st.bar_chart(wins)
st.subheader("🔍 Team Detailed Analysis")

selected_team = st.selectbox(
    "Select a Team",
    sorted(matches['team1'].unique())
)
team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

st.write("Total Matches Played:", team_matches.shape[0])
team_wins = team_matches[team_matches['winner'] == selected_team]

st.write("Total Wins:", team_wins.shape[0])
win_percentage = (team_wins.shape[0] / team_matches.shape[0]) * 100

st.write("Win Percentage:", round(win_percentage, 2), "%")
st.subheader("📊 Advanced Team Analysis")

selected_team = st.selectbox(
    "Select Team",
    sorted(matches['team1'].unique())
)
team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]
selected_venue = st.selectbox(
    "Select Venue",
    ["All"] + sorted(team_matches['venue'].dropna().unique())
)

if selected_venue != "All":
    team_matches = team_matches[team_matches['venue'] == selected_venue]
toss_option = st.selectbox(
    "Toss Result",
    ["All", "Won Toss", "Lost Toss"]
)

if toss_option == "Won Toss":
    team_matches = team_matches[team_matches['toss_winner'] == selected_team]

elif toss_option == "Lost Toss":
    team_matches = team_matches[team_matches['toss_winner'] != selected_team]
total_matches = team_matches.shape[0]

total_wins = team_matches[team_matches['winner'] == selected_team].shape[0]

if total_matches > 0:
    win_percentage = (total_wins / total_matches) * 100
    st.success(f"Winning Percentage: {round(win_percentage, 2)} %")
    st.write("Matches Considered:", total_matches)
    st.write("Wins:", total_wins)
else:
    st.warning("No matches found for selected filters.")
st.subheader("🤝 Head-to-Head Comparison with Toss Analysis")

team1 = st.selectbox("Select Team 1", sorted(matches['team1'].unique()), key="team1")
team2 = st.selectbox("Select Team 2", sorted(matches['team1'].unique()), key="team2")

# Filter matches between two teams
h2h_matches = matches[
    ((matches['team1'] == team1) & (matches['team2'] == team2)) |
    ((matches['team1'] == team2) & (matches['team2'] == team1))
]
venue_option = st.selectbox(
    "Select Venue (Optional)",
    ["All"] + sorted(h2h_matches['venue'].dropna().unique()),
    key="h2h_venue"
)

if venue_option != "All":
    h2h_matches = h2h_matches[h2h_matches['venue'] == venue_option]
toss_option = st.selectbox(
    "Toss Result",
    ["All", f"{team1} Won Toss", f"{team2} Won Toss"],
    key="h2h_toss"
)

if toss_option == f"{team1} Won Toss":
    h2h_matches = h2h_matches[h2h_matches['toss_winner'] == team1]

elif toss_option == f"{team2} Won Toss":
    h2h_matches = h2h_matches[h2h_matches['toss_winner'] == team2]
team1_wins = h2h_matches[h2h_matches['winner'] == team1].shape[0]
team2_wins = h2h_matches[h2h_matches['winner'] == team2].shape[0]

total_h2h = h2h_matches.shape[0]
st.write("Total Matches:", total_h2h)
st.write(f"{team1} Wins:", team1_wins)
st.write(f"{team2} Wins:", team2_wins)

if total_h2h > 0:
    team1_pct = (team1_wins / total_h2h) * 100
    team2_pct = (team2_wins / total_h2h) * 100

    st.success(f"{team1} Win %: {round(team1_pct,2)}%")
    st.success(f"{team2} Win %: {round(team2_pct,2)}%")
else:
    st.warning("No matches found for selected filters.")
st.subheader("📅 Season Wise Performance")

season_data = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

# Total matches per season
season_matches = season_data.groupby('season').size()

# Wins per season
season_wins = season_data[season_data['winner'] == selected_team] \
    .groupby('season').size()

# Combine into dataframe
season_performance = season_matches.to_frame(name='Total Matches')
season_performance['Wins'] = season_wins
season_performance = season_performance.fillna(0)

# Calculate win percentage
season_performance['Win %'] = (
    season_performance['Wins'] / season_performance['Total Matches']
) * 100

st.line_chart(season_performance['Win %'])
