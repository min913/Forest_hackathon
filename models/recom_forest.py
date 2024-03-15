import logging
import os
import numpy as np
import pandas as pd
import ast

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
program_list_data = pd.read_csv(os.path.join(my_path, "datasets/program_list.csv"))
forest_list_df = program_list_data.loc[program_list_data["category"] == "숲길", :].reset_index(drop=True)

def __find_closest_location(mtn = pd.DataFrame, input_coord=dict[str, float]):
    # 문자열로 저장된 'coordinate' 데이터를 딕셔너리로 변환
    mtn['coordinate'] = mtn['coordinate'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c
        return distance

    # 각 coordinate에 대한 거리 계산 후 '거리' 열에 추가
    mtn['거리'] = mtn['coordinate'].apply(lambda x: haversine(input_coord['lat'], input_coord['lng'], x['lat'], x['lng']))


    mtn.sort_values(by='거리')
    mtn.reset_index(drop=True)
    mtn.drop(columns=["거리"], inplace=True)

    # 가장 거리가 가까운 행 찾기

    return mtn[:5]
    



# 함수 호출 예제
input_coord = {'lat': 128.950001, 'lng': 37.600002} #사용자 위치

def run():
    closest_location = __find_closest_location(forest_list_df, input_coord) #함수 부르기
    print(closest_location)
    return closest_location

