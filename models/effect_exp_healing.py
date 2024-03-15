import numpy as np


def find_closest_match(df, height, age, gender, weight):
    # 필터링된 데이터프레임을 가중치로 정렬하는 함수
    def sort_by_weight_difference(filtered_df):
        filtered_df["체중 차이"] = np.abs(filtered_df["체중"] - weight)
        return filtered_df.sort_values(by="체중 차이").iloc[0]["차이"]

    # 키, 나이, 성별이 일치하는 데이터
    match = df[(df["키"] == height) & (df["나이"] == age) & (df["성별"] == gender)]
    if not match.empty:
        return sort_by_weight_difference(match)

    # 키와 나이가 일치하는 데이터
    match = df[(df["키"] == height) & (df["나이"] == age)]
    if not match.empty:
        return sort_by_weight_difference(match)

    # 키가 동일한 데이터에서 나이와 체중 차이가 최소인 데이터
    match = df[df["키"] == height]
    if not match.empty:
        match["나이 차이"] = np.abs(match["나이"] - age)
        match = match.sort_values(by=["나이 차이", "체중 차이"])
        if not match.empty:
            return match.iloc[0]["차이"]

    return 50.12
