get_ipython().system('pip install sentence-transformers')

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
import time


#데이터 불러오기
prefer_exp =  pd.read_csv(r"C:\Users\user\Desktop\산림데이터 공모전\데이터\전처리완료\체험프로그램_선호정보.csv")
program_exp = pd.read_csv(r"C:\Users\user\Desktop\산림데이터 공모전\데이터\전처리완료\산림체험프로그램목록.csv")
prgm=list(program_exp['제목'])

#유저 정보 입력 및 유저와 유사한 기존 검색 사용자 찾기
def user_info(df):
    gender = input("성별을 입력해주세요: ")
    job = input("직업을 입력해주세요: ")
    kids = input("자녀 여부를 입력해주세요: ")
    age = input("연령대를 입력해주세요: ")
    df['matching_count'] = df.apply(lambda row: sum([
        row['성별'] == gender,
        row['직업'] == job,
        row['자녀여부'] == kids,
        row['연령대'] == age
    ]), axis=1)
    top_matches = df.sort_values(by='matching_count', ascending=False).head(10)
    top_indexes = top_matches.index.tolist()
    df.drop(columns=['matching_count'], inplace=True)
    selected_preferences = [prefer_exp['제목'][i] for i in top_indexes]
    return selected_preferences
    


#문장 유사도 계산 -> 프로그램 간 유사도 계산산
def calculate_similarity(sentence1, sentence2):
    # 모델 로드 (예: 'all-MiniLM-L6-v2')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 문장을 임베딩으로 변환
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # 코사인 유사도 계산
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)

    return cosine_similarity.item()


#최대 유사도 찾아서 index 계산
def max_similarity(sentence, sentence_list):
    similarities = []
    
    # 각 선호도 항목과의 유사도 계산
    for index, p in enumerate(sentence_list):    
        similarity = calculate_similarity(sentence, p)
        similarities.append((similarity, index, p))
    
    # 유사도 기준으로 내림차순 정렬 후 상위 8개 선택
    top_8_similarities = sorted(similarities, reverse=True)[:8]
    index_list=[]
    for sim, index, pref in top_8_similarities:
        print(f"Index: {index}, Similarity: {sim}, Preference: {pref}")
        index_list.append(index)
    
    return index_list
    
    


# 최종 추출 함수
def recommend():
    start_time = time.time()
    selected_preferences =user_info(prefer_exp)
    outputs=[]
    for u in selected_preferences:
        # 각 선호도에 대한 가장 유사한 프로그램 인덱스 찾기
        output_indexes = max_similarity(u, prgm)
        # 가장 유사한 프로그램의 인덱스를 사용하여 프로그램 선택
        for index in output_indexes:
            outputs.append(prgm[index])
    end_time = time.time()  # 함수 실행 후 현재 시간 측정
    execution_time = end_time - start_time
    
    print(outputs) 
    print(f"Execution time: {execution_time} seconds")
    return outputs
    
