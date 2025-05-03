from App.models import Player
from App.database import db
import numpy as np
import pandas as pd


def get_league_name_id(league_name_string):
    if "(" in league_name_string:
        league_name_id = league_name_string.split('(')[1].split(')')[0].strip()

        league_name_id = league_name_id.lower()
        league_name_id = league_name_id.replace(' ', '')

        return league_name_id


    df['league_name_id'] = df['league_name'].apply(get_league_name_id)

    print(df[['league_name', 'league_name_id']])



def calculate_best_league(attributes, country, career_length, preferred_foot, position):
    df = pd.read_csv('App/data/Final_project_finished_Continents.csv')

    unique_leagues = df['league_name_id'].unique().tolist()
    league_scores = {}

    for league in unique_leagues:
        league_df = df[(df['league_name_id'] == league) & (df[position] == 1)]
        score = {}

        for attr, player_value in attributes.items():
            if league_df[attr].isnull().all():
                continue

            low_percentile = league_df[attr].quantile(0.05) #These are the low tier players, can adjust to suit
            high_percentile = league_df[attr].quantile(0.95) #These would be the best of the best players, adjust to suit
            avg = league_df[attr].mean()
            p40 = league_df[attr].quantile(0.4) #I just picked 40th percentile but can be adjusted to suit
            p70 = league_df[attr].quantile(0.7)
            max_val = league_df[attr].max()
            leeway = 2  #This is basically a constant so that in terms of the max valuje, we give a small amount of tolerance before we penalize for b eing above the max value

            if player_value < low_percentile:
                attr_score = 0.1
            elif player_value >= low_percentile and player_value < avg:
                attr_score = 0.3
            elif p40 <= player_value <= p70:
                attr_score = 0.6
            elif player_value > p70 and player_value <= (max_val + leeway):
                attr_score = 1.0
            elif player_value > high_percentile or player_value > (max_val + leeway):
                attr_score = 0.2
            else:
                attr_score = 0.0  

            score[attr] = attr_score

        total_score = sum(score.values())
        print(f'Total score is: {total_score} for {league}')
        league_scores[league] = total_score

    best_league = max(league_scores, key=league_scores.get)
    best_score = league_scores[best_league]

    print(f"The best league fit is: {best_league} with a score of {best_score}")
    # return league_scores