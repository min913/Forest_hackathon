# Forest_hackathon

## Healing effect prediction:

1. 운동효과_산림체험:

   -input_df: result_df(최종/산림체험효과.csv)
   
   -input_parameter: 사용자 정보(height_input, age_input, weight_input, gender_input)
   
   -input_parameter 형식: height_input = float, age_input = float, weight_input =float, gender_input = 'F' or 'M'

   -사용 예시)

   input 예시
            height_input = 160
            age_input = 20
            weight_input = 54
            gender_input = 'F'

   함수 실행 및 결과 출력
            difference = find_closest_match(result_df,height_input, age_input, gender_input,weight_input )
            difference=difference.round(2)
            print(f"찾은 '차이' 값: {difference}")

3. 숲길, 등산로 운동량
    
    -숲길_input_df: result_df(최종/숲길 칼로리.csv)
   
    -등산로_input_df: result_df(최종/등산로 칼로리.csv) *아직 업로드x
   
    -input_parameter: 등산로 거리(input_km), 사용자 정보(input_height, input_weight)
   
    -input_parameter 형식: 모두 float
   
    -output: float

    -사용 예시_숲길

   함수 사용 예시 인풋
   input_km = 0.2
   input_height = 177
   input_weight = 65

   함수 호출
   calories = find_closest_calories(way_effect, input_km, input_height, input_weight)
   print(calories)
 
 -사용 예시_산


#함수 호출 예제

input_coord = {'lat': 128.950001, 'lng': 37.600002} #사용자 위치

closest_location = find_closest_location(mtn, input_coord) #함수 부르기


## Recommendation:
1. 산림체험 및 치유
- 사용 모델: all-MiniLM-L6-v2
- input_df


2. 등산로,숲길 추천:
- input_df_등산로: mtn(최종/산목록.csv)

- input_df_숲길: *미업로드

- input_parameter: input_coord(사용자 거리)

- 함수 호출 예시:

  #input: input_coord = {'lat': 128.950001, 'lng': 37.600002}

  #함수 호출: closest_location = find_closest_location(mtn, input_coord)

- ouput: 해당하는 산이 있는 mtn의 행 추출 
