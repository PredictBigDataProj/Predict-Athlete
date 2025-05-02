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


def calculate_best_league(player_data):
    df = pd.read_csv('App/data/Final_project_finished_Continents.csv')

    unique_leagues = df['league_name_id'].unique().tolist()

    # score = {
    #     key: {"score": 0} for key in player_data
    # }

    league_scores = {}
    for league in unique_leagues:
        
        league_df = df[df['league_name_id'] == league]
        score = {}


        for key, data in player_data.items():
            #print(f'The keys are: {key}, {data}')
            avg = league_df[key].mean()

            # if abs(avg - data) < 5 or abs(avg - data) < (0.10 * avg):
            #     # print(f'No significant difference in the averange range for the atribute {key}')
            #     league_score = 0.5
            # else:
            #     # print(f'Large difference in average range for the attribute {key}')
            #     league_score = 1

            if data >= avg:
                # Reward: higher the value above avg, higher the score (capped at 1)
                league_score = min(1.0, 0.5 + (data - avg) / avg)
            else:
                # Penalty: lower the value below avg, lower the score
                league_score = max(0.0, 0.5 - (avg - data) / avg)


            score[key] = league_score

        # print("testing score dict from here downwards")
        # print(score)

        total_score = 0

        for key, data in score.items():
            total_score = total_score + float(data)

        print(f'Total score is: {total_score} for {league}')
        total_score = sum(score.values())
        league_scores[league] = total_score


    best_league = max(league_scores, key=league_scores.get)
    best_score = league_scores[best_league]

    print(f"The best league fit is: {best_league} with a score of {best_score}")

    # best_fit = sorted(league_scores.items(), key=lambda x: x[1], reverse=True)
    # return best_fit