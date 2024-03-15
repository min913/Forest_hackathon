import numpy as np


def find_closest_calories(way_effect, input_km, input_height, input_weight):
    # 운동거리 차이 계산
    way_effect["운동거리_차이"] = abs(way_effect["운동거리"] - input_km)
    # 운동거리 차이를 기준으로 정렬 후 상위 5개 행 선택
    closest_distances = way_effect.sort_values(by="운동거리_차이").head(5)

    # 키와 체중 차이 계산
    closest_distances["키_체중_차이"] = abs(
        closest_distances["키"] - input_height
    ) + abs(closest_distances["체중"] - input_weight)
    # 키와 체중 차이가 가장 작은 행 찾기
    closest_row = closest_distances.sort_values(by="키_체중_차이").iloc[0]

    # 해당 행의 칼로리 값 반환
    return closest_row["칼로리"]
