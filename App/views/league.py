from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    send_from_directory,
    flash,
    redirect,
    url_for,
)
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import StandardScaler
from App.database import db


from .index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players,
    load_models,
    get_user,
    get_user_by_username,
    get_league_name_id,
)


player_attributes = [
    "height_cm",
    "weight_kg",
    "crossing",
    "finishing",
    "heading_accuracy",
    "short_passing",
    "volleys",
    "dribbling",
    "curve",
    "fk_accuracy",
    "long_passing",
    "ball_control",
    "acceleration",
    "sprint_speed",
    "agility",
    "reactions",
    "balance",
    "shot_power",
    "jumping",
    "stamina",
    "strength",
    "long_shots",
    "aggression",
    "interceptions",
    "positioning",
    "vision",
    "penalties",
    "composure",
    "defensive_awareness",
    "standing_tackle",
    "sliding_tackle",
    "gk_diving",
    "gk_handling",
    "gk_kicking",
    "gk_positioning",
    "gk_reflexes",
    "age",
    "speed_strength_ratio",
    "agility_height_ratio",
    "jumping_height_ratio",
    "stamina_weight_ratio",
    "offensive_skills",
    "defensive_skills",
    "playmaking_skills",
    "physical_dominance",
    "technical_ability",
    "speed_composite",
    "goalkeeper_skills",
    "offensive_defensive_diff",
    "offensive_defensive_ratio",
    "technical_physical_ratio",
    "pressure_handling",
]

player_attributes_1 = [
    "height_cm",
    "weight_kg",
    "crossing",
    "finishing",
    "heading_accuracy",
    "short_passing",
    "volleys",
    "dribbling",
    "curve",
    "fk_accuracy",
    "long_passing",
    "ball_control",
    "acceleration",
    "sprint_speed",
    "agility",
    "reactions",
    "balance",
    "shot_power",
    "jumping",
    "stamina",
    "strength",
    "long_shots",
    "aggression",
    "interceptions",
    "positioning",
    "vision",
    "penalties",
    "composure",
    "defensive_awareness",
    "standing_tackle",
    "sliding_tackle",
    "gk_diving",
    "gk_handling",
    "gk_kicking",
    "gk_positioning",
    "gk_reflexes",
]

positions = [
    "ST",
    "RWB",
    "RW",
    "RM",
    "RB",
    "LWB",
    "LW",
    "LM",
    "LB",
    "GK",
    "CM",
    "CF",
    "CDM",
    "CB",
    "CAM",
]


df = pd.read_csv("App/data/Final_project_finished_Continents.csv")


league_views = Blueprint("league_views", __name__, template_folder="../templates")


@league_views.route("/league/<league_id>-<country>", methods=["GET"])
def get_league_page(league_id, country):
    df["league_name_id"] = df["league_name"].apply(get_league_name_id)

    league_info = df[df["league_name_id"] == league_id]
    league_df = df[df["league_name_id"] == league_id]

    group_counts = league_df["age_group"].value_counts(normalize=True) * 100

    avg_age = league_df["age"].mean()
    min_age = league_df["age"].min()
    max_age = league_df["age"].max()
    max_career = league_df["league_Career_length"].max()
    min_career = league_df["league_Career_length"].min()
    avg_career = league_df["league_Career_length"].mean()
    age_counts = league_df["age"].value_counts()

    position_stats = []

    for pos in positions:
        pos_df = league_df[league_df[pos] == 1]
        group_counts_pos = pos_df["age_group"].value_counts(normalize=True) * 100
        age_total_count = pos_df.shape[0]

        if pos_df.empty:
            print(f"No players in this position: {pos}")
            print("\n")
        else:

            pos_data = {
                "position": pos,
                "avg_age": pos_df["age"].mean(),
                "min_age": pos_df["age"].min(),
                "max_age": pos_df["age"].max(),
                "avg_career": pos_df["league_Career_length"].mean(),
                "min_career": pos_df["league_Career_length"].min(),
                "max_career": pos_df["league_Career_length"].max(),
                "pos_age_groups": group_counts_pos.to_dict(),
                "age_total_count": age_total_count,
            }
            position_stats.append(pos_data)

    avg_age = df[df["league_name_id"] == league_id]["age"].mean()
    nation_df = df[df["league_name_id"] == league_id]

    unique_nations = nation_df["nation_Nation"].unique().tolist()
    unique_regions = nation_df["nation_region"].unique().tolist()

    total_count = nation_df.shape[0]  #
    nation_count = nation_df["nation_Nation"].value_counts()
    region_count = nation_df["nation_region"].value_counts()

    max_nation_name = nation_count.idxmax()
    max_nation_num = nation_count.max()

    max_region_name = region_count.idxmax()
    max_region_num = region_count.max()

    nation_max_by_position = {pos: {"count": 0, "nation": None} for pos in positions}

    region_max_by_position = {
        pos: {"region_count": 0, "region": None} for pos in positions
    }

    distribution = []
    region_distribution = []

    for nation in unique_nations:
        spec_count = nation_df[nation_df["nation_Nation"] == nation].shape[0]
        percentage_count = (spec_count / total_count) * 100

        nation_data = {
            "nation": nation,
            "percentage": round(percentage_count, 2),
            "count": spec_count,
            "positions": {},
        }

        for pos in positions:
            pos_df = nation_df[
                (nation_df[pos] == 1) & (nation_df["nation_Nation"] == nation)
            ]
            count_pos = pos_df.shape[0]

            nation_data["positions"][pos] = count_pos

            if count_pos > nation_max_by_position[pos]["count"]:
                nation_max_by_position[pos]["count"] = count_pos
                nation_max_by_position[pos]["nation"] = nation

                nation_max_by_position[pos] = {"count": count_pos, "nation": nation}

        distribution.append(nation_data)

    nation_results = {
        "total_players": total_count,
        "most_common_nation": max_nation_name,
        "most_common_nation_count": max_nation_num,
        "unique_nations": unique_nations,
        "distribution": distribution,
        "max_by_position": nation_max_by_position,
    }

    for region in unique_regions:
        region_spec_count = nation_df[nation_df["nation_region"] == region].shape[0]
        region_percentage_count = (region_spec_count / total_count) * 100

        region_data = {
            "region": region,
            "region_percentage": round(region_percentage_count, 2),
            "region_count": region_spec_count,
            "positions": {},
        }

        for pos in positions:
            pos_df = nation_df[
                (nation_df[pos] == 1) & (nation_df["nation_region"] == region)
            ]
            region_count_pos = pos_df.shape[0]

            region_data["positions"][pos] = region_count_pos

            if region_count_pos > region_max_by_position[pos]["region_count"]:
                region_max_by_position[pos]["region_count"] = region_count_pos
                region_max_by_position[pos]["region"] = region

                region_max_by_position[pos] = {
                    "region_count": region_count_pos,
                    "region": region,
                }

        region_distribution.append(region_data)

    region_results = {
        "region_total_players": total_count,
        "most_common_region": max_region_name,
        "most_common_region_count": max_region_num,
        "unique_regions": unique_regions,
        "region_distribution": region_distribution,
        "region_max_by_position": region_max_by_position,
    }
    final_df = df[df["league_name_id"] == league_id]
    attr_max = {}
    attr_min = {}
    attr_avg = {}

    left_df = final_df[final_df["preferred_foot_Left"] == 1]
    right_df = final_df[final_df["preferred_foot_Right"] == 1]

    count_left_total = left_df.shape[0]
    count_right_total = right_df.shape[0]

    total_ovr = count_left_total + count_right_total

    attribute_data = []

    for attr in player_attributes_1:
        total_attr_max = final_df[attr].max()
        total_attr_min = final_df[attr].min()
        total_attr_avg = final_df[attr].mean()
        attri_data = {
            "attribute": attr,
            "avg_score": final_df[attr].mean(),
            "min_score": final_df[attr].min(),
            "max_score": final_df[attr].max(),
        }
        attribute_data.append(attri_data)

    pos_attribute_data = []

    for pos in positions:
        pos_df = final_df[final_df[pos] == 1]

        left_df = pos_df[pos_df["preferred_foot_Left"] == 1]
        right_df = pos_df[pos_df["preferred_foot_Right"] == 1]

        count_left = left_df.shape[0]
        count_right = right_df.shape[0]
        pos_total = count_left + count_right

        pos_attri_data = {
            "position": pos,
            "count_left": count_left,
            "count_right": count_right,
            "pos_total": pos_total,
            "attributes": {},
        }

        if abs(count_left - count_right) < 5 or abs(count_left - count_right) < (
            0.10 * pos_total
        ):
            print(
                f"Not really a better chance if you are left footed or right footed as a {pos} in {league_id}"
            )
        else:

            if count_left > count_right:
                print(f"Better chance if you are left footed as a {pos} in {league_id}")
            else:
                print(
                    f"Better chance if you are right footed as a {pos} in {league_id}"
                )
        if pos not in attr_max:
            attr_max[pos] = {}
            attr_min[pos] = {}
            attr_avg[pos] = {}
        for attr in player_attributes_1:
            attr_max[pos][attr] = pos_df[attr].max()
            attr_min[pos][attr] = pos_df[attr].min()
            attr_avg[pos][attr] = pos_df[attr].mean()

            pos_attr_max = attr_max[pos][attr]
            pos_attr_min = attr_min[pos][attr]
            pos_attr_avg = attr_avg[pos][attr]
            pos_attri_data["attributes"][attr] = {
                "pos_attr_max": pos_attr_max,
                "pos_attr_min": pos_attr_min,
                "pos_attr_avg": pos_attr_avg,
            }
        pos_attribute_data.append(pos_attri_data)
    for position in pos_attribute_data:
        if position["pos_total"] == 0:
            for attr, values in position["attributes"].items():
                for key in ["pos_attr_max", "pos_attr_min", "pos_attr_avg"]:
                    values[key] = 0

    league_names = df[df["league_name_id"] == league_id]["league_name"].unique()
    nav_name = league_names[0] if len(league_names) > 0 else "League"

    return render_template(
        "league.html",
        league_id=league_id,
        country=country,
        league_info=league_info.to_dict(orient="records"),
        avg_age=avg_age,
        min_age=min_age,
        max_age=max_age,
        avg_career=avg_career,
        min_career=min_career,
        max_career=max_career,
        position_stats=position_stats,
        age_groups=group_counts.to_dict(),
        age_counts=age_counts.to_dict(),
        nav_name=nav_name,
        nation_results=nation_results,
        region_results=region_results,
        left_footed_players=count_left_total,
        right_footed_players=count_right_total,
        total_players=total_ovr,
        attribute_data=attribute_data,
        pos_attribute_data=pos_attribute_data,
    )
