def find_closest_location(mtn, input_coord):
    # 문자열로 저장된 '좌표' 데이터를 딕셔너리로 변환
    mtn['좌표'] = mtn['좌표'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distance = R * c
        return distance

    # 각 좌표에 대한 거리 계산 후 '거리' 열에 추가
    mtn['거리'] = mtn['좌표'].apply(lambda x: haversine(input_coord['lat'], input_coord['lng'], x['lat'], x['lng']))

    # 가장 거리가 가까운 행 찾기
    closest_location = mtn.loc[mtn['거리'].idxmin()]
    print(closest_location)
    return closest_location
    



