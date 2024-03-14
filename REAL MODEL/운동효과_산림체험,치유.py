#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os


# In[91]:


hth_sp = pd.read_csv(r"C:\Users\user\Desktop\산림데이터 공모전\데이터\건강효과_측정.csv")


# In[61]:


hth_sp


# In[92]:


col=['대상자키','대상자성별코드','대상자연령','대상자최소체지방량','대상자최대체지방량','대상자체중']


# In[93]:


hth_sp=hth_sp[col]


# In[94]:


hth_sp = hth_sp.iloc[1:]


# In[95]:


hth_sp


# In[96]:


hth_sp['대상자최소체지방량'] = pd.to_numeric(hth_sp['대상자최소체지방량'])
hth_sp['대상자최대체지방량'] = pd.to_numeric(hth_sp['대상자최대체지방량'])
hth_sp['대상자연령'] = pd.to_numeric(hth_sp['대상자연령'])
hth_sp['대상자키'] = pd.to_numeric(hth_sp['대상자키'])
hth_sp['대상자체중'] = pd.to_numeric(hth_sp['대상자체중'])
hth_sp['체지방량_차이'] = hth_sp['대상자최대체지방량'] - hth_sp['대상자최소체지방량']


# In[97]:


hth_sp=hth_sp.drop(columns=['대상자최소체지방량','대상자최대체지방량'])


# In[98]:


hth_sp


# In[99]:


hth_sp.columns  = ['키','성별','나이','체중','차이']


# In[100]:


hth_sp=hth_sp.drop_duplicates()


# In[101]:


result_df = hth_sp.groupby(['키', '나이', '성별','체중'], as_index=False).agg({'차이':'mean'})


# In[102]:


result_df['차이']=result_df['차이']*7.8


# In[107]:


result_df['차이'].round(2)


# In[110]:


result_df['차이']


# In[104]:


type(result_df['체중'][0])


# In[111]:


def find_closest_match(df, height, age, gender, weight):
    # 필터링된 데이터프레임을 가중치로 정렬하는 함수
    def sort_by_weight_difference(filtered_df):
        filtered_df['체중 차이'] = np.abs(filtered_df['체중'] - weight)
        return filtered_df.sort_values(by='체중 차이').iloc[0]['차이']
    
    # 키, 나이, 성별이 일치하는 데이터
    match = df[(df['키'] == height) & (df['나이'] == age) & (df['성별'] == gender)]
    if not match.empty:
        return sort_by_weight_difference(match)
    
    # 키와 나이가 일치하는 데이터
    match = df[(df['키'] == height) & (df['나이'] == age)]
    if not match.empty:
        return sort_by_weight_difference(match)
    
    # 키가 동일한 데이터에서 나이와 체중 차이가 최소인 데이터
    match = df[df['키'] == height]
    if not match.empty:
        match['나이 차이'] = np.abs(match['나이'] - age)
        match = match.sort_values(by=['나이 차이', '체중 차이'])
        if not match.empty:
            return match.iloc[0]['차이']
    
    return 50.12


# 사용자 입력 예시
height_input = 160
age_input = 20
weight_input = 54
gender_input = 'F'

# 함수 실행 및 결과 출력
difference = find_closest_match(result_df,height_input, age_input, gender_input,weight_input )
difference=difference.round(2)
print(f"찾은 '차이' 값: {difference}")


# In[ ]:




