# Forest_hackathon

## Healing effect prediction:

1. 운동효과_산림체험,치유:
   -input_df: result_df(최종/산림체험효과.csv)
   
   -input_parameter: 사용자 정보(height_input, age_input, weight_input, gender_input)
   -input_parameter 형식: height_input = float, age_input = float, weight_input =float, gender_input = 'F' or 'M'

   -사용 예시) # input 예시
            height_input = 160
            age_input = 20
            weight_input = 54
            gender_input = 'F'

            # 함수 실행 및 결과 출력
            difference = find_closest_match(result_df,height_input, age_input, gender_input,weight_input )
            difference=difference.round(2)
            print(f"찾은 '차이' 값: {difference}")

 
   
   -output: float
 


## Recommendation:
1. 산림체험 및 치유
- 사용 모델: all-MiniLM-L6-v2
- input_df
