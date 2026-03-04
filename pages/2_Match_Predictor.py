import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

st.title("🏏 IPL Match Win Predictor")

# -----------------------------
# Load Dataset
# -----------------------------
matches = pd.read_csv("data/matches.csv")

# Remove matches without winner
matches = matches.dropna(subset=['winner'])

# Select required columns
data = matches[['team1', 'team2', 'venue', 'toss_winner', 'winner']].copy()

# -----------------------------
# Create Label Encoders
# -----------------------------
le_team = LabelEncoder()
le_venue = LabelEncoder()
le_winner = LabelEncoder()

# Fit encoders
le_team.fit(pd.concat([data['team1'], data['team2'], data['toss_winner']]))
le_venue.fit(data['venue'])
le_winner.fit(data['winner'])

# Transform dataset
data['team1'] = le_team.transform(data['team1'])
data['team2'] = le_team.transform(data['team2'])
data['toss_winner'] = le_team.transform(data['toss_winner'])
data['venue'] = le_venue.transform(data['venue'])
data['winner'] = le_winner.transform(data['winner'])

# -----------------------------
# Train Model
# -----------------------------
X = data[['team1', 'team2', 'venue', 'toss_winner']]
y = data['winner']

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# User Input Section
# -----------------------------
st.subheader("Enter Match Details")

team_list = sorted(matches['team1'].unique())
venue_list = sorted(matches['venue'].unique())

team1 = st.selectbox("Team 1", team_list)
team2 = st.selectbox("Team 2", team_list)
venue = st.selectbox("Venue", venue_list)
toss_winner = st.selectbox("Toss Winner", [team1, team2])

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Winner"):

    input_data = pd.DataFrame({
        'team1': [le_team.transform([team1])[0]],
        'team2': [le_team.transform([team2])[0]],
        'venue': [le_venue.transform([venue])[0]],
        'toss_winner': [le_team.transform([toss_winner])[0]]
    })

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)

    predicted_team = le_winner.inverse_transform(prediction)[0]

    predicted_class_index = prediction[0]
    win_probability = probabilities[0][predicted_class_index] * 100

    st.success(f"🏆 Predicted Winner: {predicted_team}")
    st.info(f"📊 Winning Probability: {round(win_probability, 2)}%")

    st.progress(int(win_probability))
