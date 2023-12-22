import streamlit as st
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
import io
import platform
import os
import re

# 페이지 기본 설정
st.set_page_config(
    page_icon="😗",
    page_title="오뚝케먹지?!😋",
    layout="wide",
)

## Title
st.image('./pages/img/banner.png', use_column_width=True)
st.header("🎲오뚝 레시피 테스트")

## Text
st.text("나는 어떤 레시피일까? 🤔")
st.text("")

## 변수 설정
q1 = 0
q2 = 0
q3 = 0

## 테스트 시작
st.subheader("테스트 시작!")
st.text("")

q1_1 = st.radio("1️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q1_2 = st.radio("2️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q1_3 = st.radio("3️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q2_1 = st.radio("4️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q2_2 = st.radio("5️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q2_3 = st.radio("6️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q3_1 = st.radio("7️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q3_2 = st.radio("8️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

q3_3 = st.radio("9️⃣ 질문 블라블라", ("답변1", "답변2"))
st.text("")
st.text("")

if st.button("결과 보기"):

    ## 점수 계산
    if q1_1 == "답변1": q1 = q1 + 1
    else: q1 = q1 - 1

    if q1_2 == "답변1": q1 = q1 + 1
    else: q1 = q1 - 1

    if q1_3 == "답변1": q1 = q1 + 1
    else: q1 = q1 - 1

    if q2_1 == "답변1": q2 = q2 + 1
    else: q2 = q2 - 1

    if q2_2 == "답변1": q2 = q2 + 1
    else: q2 = q2 - 1

    if q2_3 == "답변1": q2 = q2 + 1
    else: q2 = q2 - 1

    if q3_1 == "답변1": q3 = q3 + 1
    else: q3 = q3 - 1

    if q3_2 == "답변1": q3 = q3 + 1
    else: q3 = q3 - 1

    if q3_3 == "답변1": q3 = q3 + 1
    else: q3 = q3 - 1

    ## 결과 가져오기
    data = pd.read_csv('./data/test.csv', encoding='ANSI')

    num = 0

    if q1>0 and q2>0 and q3>0: num = 1
    elif q1<0 and q2>0 and q3>0: num = 2
    elif q1>0 and q2<0 and q3>0: num = 3
    elif q1>0 and q2>0 and q3<0: num = 4
    elif q1<0 and q2<0 and q3>0: num = 5
    elif q1>0 and q2<0 and q3<0: num = 6
    elif q1<0 and q2>0 and q3<0: num = 7
    elif q1<0 and q2<0 and q3<0: num = 8

    st.text("")
    st.subheader(f"당신은 \"{data['name'].iloc[num-1]}\"입니다.")
    st.text("")
    st.text(f"{data['content'].iloc[num-1]}")
    st.text("")
    st.markdown("<h5>당신의 레시피</h3>", unsafe_allow_html=True)
    st.text("")
    st.text(f"{data['recipe'].iloc[num-1]}")
    ## 사진 첨부
    st.text("")
    st.markdown("<h5>찰떡궁합 레시피</h3>", unsafe_allow_html=True)
    st.text("")
    st.text(f"\"{data['good'].iloc[num-1]}\"")
    st.text("")
    st.text(f"{data[data['name'] == data['good'].iloc[num-1]]['recipe'].values[0]}")
    ## 사진 첨부
    st.text("")
