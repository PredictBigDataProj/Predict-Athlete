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



