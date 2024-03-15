import random
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from datetime import datetime
import math
import os.path
from . import schemas, models
import logging

my_path = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
# 데이터 불러오기
prefer_exp_path = os.path.join(my_path, "datasets/program_preferences.csv")
prefer_exp = pd.read_csv(prefer_exp_path)

program_df_path = os.path.join(my_path, "datasets/programs.csv")
program_df = pd.read_csv(program_df_path)
prgm = list(program_df["제목"])

sentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")


# 유저 정보 입력 및 유저와 유사한 기존 검색 사용자 찾기
def __user_info(df, user=models.User):
    age = datetime.today().year - user.birth_year
    age_range = str(math.floor(age / 10) * 10) + "대"
    df["matching_count"] = df.apply(
        lambda row: sum(
            [
                row["성별"] == user.gender,
                row["직업"] == user.job,
                row["자녀여부"] == user.has_children,
                row["연령대"] == age_range,
            ]
        ),
        axis=1,
    )
    top_matches = df.sort_values(by="matching_count", ascending=False).head(10)
    top_indexes = top_matches.index.tolist()
    df.drop(columns=["matching_count"], inplace=True)
    selected_preferences = [prefer_exp["제목"][i] for i in top_indexes]
    return selected_preferences


# 문장 유사도 계산 -> 프로그램 간 유사도 계산산
def __calculate_similarity(embedding1, embedding2):    
    # 코사인 유사도 계산
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_similarity.item()

def get_embedding(sentence):
    return sentenceTransformer.encode(sentence)

program_df["제목_임베딩"] = program_df.apply(lambda x: get_embedding(x["제목"]), axis=1)


# 최대 유사도 찾아서 index 계산
def __max_similarity(sentence,):
    similarities = []

    sentence_embed = get_embedding(sentence)

    # 각 선호도 항목과의 유사도 계산
    for index, e in enumerate(program_df["제목_임베딩"]):
        similarity = __calculate_similarity(sentence_embed, e)
        similarities.append((similarity, index, e))

    # 유사도 기준으로 내림차순 정렬 후 상위 8개 선택
    top_8_similarities = sorted(similarities, reverse=True)[:8]
    index_list = []
    for sim, index, pref in top_8_similarities:
        print(f"Index: {index}")
        index_list.append(index)

    return index_list


# 최종 추출 함수
def recommend(user=models.User, ):
    selected_preferences = __user_info(prefer_exp, user)
    outputs = []
    for u in selected_preferences:
        # 각 선호도에 대한 가장 유사한 프로그램 인덱스 찾기
        output_indexes = __max_similarity(u)
        # 가장 유사한 프로그램의 인덱스를 사용하여 프로그램 선택

        for index in output_indexes:
            program_row = program_df.loc[index,:]
            program = schemas.ProgramMini(id=index, name=program_row["제목"], rate=round(random.random()*6), category="등산로")
            outputs.append(program)

    return outputs
