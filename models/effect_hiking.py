import logging
import os
import numpy as np
import pandas as pd
import ast
from fastapi import Depends, FastAPI, HTTPException, Request
from . import effect_exp_healing, effect_forest_hiking

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
hiking_calorie_data = pd.read_csv(
    os.path.join(my_path, "datasets/hiking_calorie_data.csv")
)


def __find_closest_calories(
    df,
    distance,
    gender,
    age_range,
):
    
    # 거리 차이 계산 및 정렬
    df["거리차이"] = abs(df["거리"] - distance)
    sorted_df = df.sort_values(by="거리차이").head(5)

    # 성별과 나이가 모두 일치하는 행 찾기
    exact_match = sorted_df[
        (sorted_df["성별"] == gender) & (sorted_df["나이"] == age_range)
    ]
    if not exact_match.empty:
        

        return exact_match["칼로리"].values[0]

    # 성별이나 나이 중 하나라도 일치하는 행 찾기
    partial_match = sorted_df[
        (sorted_df["성별"] == gender) | (sorted_df["나이"] == age_range)
    ]
    partial_match.reset_index(drop=True, inplace=True)

    if not partial_match.empty:
         return partial_match.iloc[0]["칼로리"]
    
    # 가장 거리 차이가 적은 행의 칼로리 반환
    return sorted_df.iloc[0]["칼로리"]


def run(
    distance,
    gender,
    age_range,
):
    return __find_closest_calories(hiking_calorie_data, distance, gender, age_range)
