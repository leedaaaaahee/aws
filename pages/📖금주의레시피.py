import streamlit as st
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import io
import platform
import matplotlib.pyplot as plt
import random

#페이지 기본 설정
st.set_page_config(
    page_icon="😗",
    page_title="오뚝케먹지?!😋",
    layout="wide",
)

## Title
st.image('./pages/img/banner.png', use_column_width = True)
st.header("📖 금주의 레시피")

## Text
st.text("금주의 추천 레시피는 무엇일까요? 제품 판매량을 통해 가장 인기있던 제품을 소개하고,")
st.text("제품과 관련된 오키친 레시피를 추천해 줄게요.")

with open('./pages/db/top.txt', 'r', encoding='utf-8') as file:
    # 파일 내용 읽기
    file_contents = file.read()

total_df = pd.read_csv("./data/total.csv")

total_df['레시피재료'].fillna('', inplace=True)

# '진라면 순한맛'을 포함한 행을 찾을 때 대소문자를 무시하도록 설정합니다.
filtered_df = total_df[total_df['레시피재료'].str.contains(file_contents, case=False)]


# 랜덤하게 하나의 행을 선택
random_row_index = random.randint(0, len(filtered_df) - 1)  # 랜덤 인덱스 선택

# 선택된 행을 새로운 데이터프레임으로 저장
random_row_df = pd.DataFrame(filtered_df.iloc[random_row_index])

# 선택된 데이터프레임을 표로 표시
#st.table(random_row_df)

# '이름' 열의 값을 'name' 변수에 저장
name = random_row_df.loc['이름'].values[0]
need = random_row_df.loc['레시피재료'].values[0]
recipe = random_row_df.loc['레시피'].values[0]
kind = random_row_df.loc['종류'].values[0]
needspecific = random_row_df.loc['재료'].values[0]
how  = random_row_df.loc['방법'].values[0]
temma = random_row_df.loc['테마'].values[0]
anniv = random_row_df.loc['기념일'].values[0]
equipment = random_row_df.loc['도구'].values[0]

st.header(" ")
st.header(name)
st.header(" ")
st.subheader("준비물")
st.text(need)
st.header(" ")
st.subheader("소개 및 레시피")
st.text(recipe)
st.header(" ")
st.subheader("테마")
st.text(temma)
st.header(" ")
st.subheader("도구")
st.text(equipment)