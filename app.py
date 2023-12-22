import streamlit as st
import streamlit as st
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import io

#페이지 기본 설정
st.set_page_config(
    page_icon="😗",
    page_title="오뚝케먹지?!😋",
    layout="wide",
)

## Title
st.image('./pages/img/banner.png', use_column_width = True)
st.header("오뚝케먹지?🤔😋")

## Text
st.text("오뚜기 좋아하는 사람은 다 모였다, 소비자가 선택한 오뚜기 커뮤니티 사이트!")
## 좌측 탐색기 > 새 폴더 > pages 만들고 우클릭해서 '새 파일' 눌러서 "1_🤨오뚝케 먹을까요?.py" > 마찬가지로 4개 만들면 됨

st.header(" ")


# 4개의 컬럼 생성
col1, col2 = st.columns([3, 3])

# 첫 번째 컬럼
with col1:
    st.markdown("<h3>📖 금주의 레시피</h3>", unsafe_allow_html=True)
    st.text('데이터 분석으로 추천해주는 오늘의 레시피')

# 두 번째 컬럼
with col2:
    st.markdown("<h3>🤖 오뚝케 먹을까요?</h3>", unsafe_allow_html=True)
    st.text("챗봇이 레시피를 추천해요!")

col3, col4 = st.columns([3, 3])

# 세 번째 컬럼
with col3:
    st.markdown("<h3>👥 다들, 오뚝케먹지?</h3>", unsafe_allow_html=True)
    st.text("나만의 레시피를 공유해요!")

# 네 번째 컬럼
with col4:
    st.markdown("<h3>🍚 오늘, 오뚝케먹었냐면! </h3>", unsafe_allow_html=True)
    st.text("오늘 무엇을 먹었는지 공유해요!")

#-------------여까지 첫화면