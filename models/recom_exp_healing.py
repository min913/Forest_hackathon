from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os
from datetime import datetime
import math
import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 데이터 불러오기
prefer_exp_data = pd.read_csv(os.path.join(my_path, "datasets/exp_preference_data.csv"))
prefer_healing_data = pd.read_csv(
    os.path.join(my_path, "datasets/healing_preference_data.csv")
)
program_list_data = pd.read_csv(os.path.join(my_path, "datasets/program_list.csv"))

model = SentenceTransformer("all-MiniLM-L6-v2")


def __get_embedding(sentence):
    return model.encode(sentence)


exp_list_df = program_list_data.loc[program_list_data["category"] == "숲 체험", :].reset_index(drop=True)
healing_list_df = program_list_data.loc[program_list_data["category"] == "산림 치유원", :].reset_index(drop=True)

print(exp_list_df)
print(healing_list_df)

exp_list_df["name_embedding"] = exp_list_df.apply(lambda x: __get_embedding(x["name"]), axis=1)
healing_list_df["name_embedding"] = exp_list_df.apply(lambda x: __get_embedding(x["name"]), axis=1)


# 유저 정보 입력 및 유저와 유사한 기존 검색 사용자 찾기
def __get_selected_preferences(prefer_df, birth_year, gender, job, has_children):
    age = datetime.today().year - birth_year
    age_range = str(math.floor(age / 10) * 10) + "대"
    prefer_df["matching_count"] = prefer_df.apply(
        lambda row: sum(
            [
                row["성별"] == gender,
                row["직업"] == job,
                row["자녀여부"] == has_children,
                row["연령대"] == age_range,
            ]
        ),
        axis=1,
    )
    top_matches = prefer_df.sort_values(by="matching_count", ascending=False).head(10)
    top_indexes = top_matches.index.tolist()
    prefer_df.drop(columns=["matching_count"], inplace=True)
    selected_preferences = [prefer_df["제목"][i] for i in top_indexes]
    return selected_preferences


# 문장 유사도 계산 -> 프로그램 간 유사도 계산산
def __calculate_similarity(embedding1, embedding2):
    # 코사인 유사도 계산
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_similarity.item()


# 최대 유사도 찾아서 index 계산
def __max_similarity(
    embedding,
    embeddingList,
):
    similarities = []

    # 각 선호도 항목과의 유사도 계산
    for index, e in enumerate(embeddingList):
        similarity = __calculate_similarity(embedding, e)
        similarities.append(
            (
                similarity,
                index,
            )
        )

    # 유사도 기준으로 내림차순 정렬 후 상위 8개 선택
    top_8_similarities = sorted(similarities, reverse=True)[:8]
    index_list = []
    for __sim__, index in top_8_similarities:
        index_list.append(index)

    return index_list


# 최종 추출 함수
def __get_outputs(prefer_df, list_data, birth_year, gender, job, has_children):
    selected_preferences = __get_selected_preferences(
        prefer_df, birth_year, gender, job, has_children
    )
    all_indexes = []
    for u in selected_preferences:
        embedding = __get_embedding(u)
        # 각 선호도에 대한 가장 유사한 프로그램 인덱스 찾기
        output_indexes = __max_similarity(embedding, list_data["name_embedding"])
        # 가장 유사한 프로그램의 인덱스를 사용하여 프로그램 선택

        for index in output_indexes:
            all_indexes.append(index)
    return list_data.loc[all_indexes, :].reset_index(drop=True)


def run(birth_year, gender, job, has_children):
    exp_outputs = __get_outputs(
        prefer_exp_data, exp_list_df, birth_year, gender, job, has_children
    )
    healing_outputs = __get_outputs(
        prefer_healing_data, healing_list_df, birth_year, gender, job, has_children
    )

    return pd.concat([exp_outputs, healing_outputs]).reset_index(drop=True)
