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
forest_calorie_data = pd.read_csv(os.path.join(my_path, "datasets/forest_calorie_data.csv"))
hiking_calorie_data = pd.read_csv(os.path.join(my_path, "datasets/hiking_calorie_data.csv"))


def __find_closest_calories(calorie_data, input_km, input_height, input_weight):
    # 운동거리 차이 계산
    calorie_data["운동거리_차이"] = abs(calorie_data["운동거리"] - input_km)
    # 운동거리 차이를 기준으로 정렬 후 상위 5개 행 선택
    closest_distances = calorie_data.sort_values(by="운동거리_차이").head(5)

    # 키와 체중 차이 계산
    closest_distances["키_체중_차이"] = abs(
        closest_distances["키"] - input_height
    ) + abs(closest_distances["체중"] - input_weight)
    # 키와 체중 차이가 가장 작은 행 찾기
    closest_row = closest_distances.sort_values(by="키_체중_차이").iloc[0]

    # 해당 행의 칼로리 값 반환
    return closest_row["칼로리"]

def run_forest(input_km, input_height, input_weight):
    __find_closest_calories(forest_calorie_data, input_km, input_height, input_weight)

def run_hikingt(input_km, input_height, input_weight):
    __find_closest_calories(forest_calorie_data, input_km, input_height, input_weight)
