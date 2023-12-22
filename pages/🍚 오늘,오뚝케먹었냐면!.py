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
st.header("오늘, 오뚝케 먹었냐면!")

## Text
st.text("오늘 무엇을 먹었는지 공유해요!😊")

selected_page = st.sidebar.selectbox("오뚝케 먹었냐면! 메뉴를 선택하세요.", ["게시물 등록하기", "게시물 보기"])

# 선택한 페이지에 따라 내용 표시
if selected_page == "게시물 등록하기":
    st.subheader("게시물 등록 페이지")

    # 텍스트 저장 변수
    title_free = ""
    content_free = ""
    uploaded_image_free = None

    title_free = st.text_input("글의 제목을 입력하세요.", "내용을 입력하세요.")
    content_free = st.text_area("자유롭게 게시물을 작성해주세요.", "내용을 입력하세요.")

    # 사진 업로드 위젯 생성
    uploaded_image_free = st.file_uploader("사진을 업로드하세요 (선택사항)", type=["jpg", "jpeg", "png"])

    # 제출하기 버튼
    if st.button("제출하기"):
     # csv 파일로 저장
        existing_data = pd.read_csv('./pages/db/today.csv', encoding='utf-8')

        new_data = {
            '이름': [title_free],
            '내용': [content_free],
        }
        
        new_df = pd.DataFrame(new_data)  
        
        updated_data = pd.concat([existing_data, new_df], ignore_index=True)
        
        updated_data.to_csv('./pages/db/today.csv', index=False, encoding='utf-8')
        
        if uploaded_image_free is not None:
            # 업로드된 사진을 바이너리 데이터로 읽어옴
            image_data = uploaded_image_free.read()
            
            n = len(updated_data)
    
            # 바이너리 데이터를 파일로 저장
            with open('./pages/db/pic_free{}.png'.format(n), 'wb') as file:
                file.write(image_data)
        
        st.success("게시글이 성공적으로 작성되었습니다.")

elif selected_page == "게시물 보기":
    st.title("게시물 보기 페이지")
    
    read_data = pd.read_csv('./pages/db/today.csv', encoding='utf-8')
    
    # DB 디렉토리 경로
    db_directory = './pages/db/'
    
    # 파일 이름 패턴을 정의합니다. 여기서는 "img"로 시작하고 ".png"로 끝나는 파일을 선택합니다.
    file_pattern = re.compile(r'^pic_free\d+\.png$', re.IGNORECASE)
    
    # DB 디렉토리에서 파일 이름 패턴과 일치하는 파일들만 가져오기
    matching_files = [file for file in os.listdir(db_directory) if file_pattern.match(file)]
    
    # 각 변수를 리스트로 저장
    title = read_data['이름']
    content = read_data['내용']

    # 가져온 파일들의 리스트 저장
    img_files = []
    for matching_file in matching_files:
        img_files.append(os.path.join(db_directory, matching_file))

    # 파일 경로
    logo_path = "./pages/img/logo.png"

    # 파일이 존재하는지 확인
    index = 0
    
    for i in range(len(read_data)):
        
        col1,col2 = st.columns([1,3])
        
        with col1:
            # 리스트의 길이를 벗어나지 않도록 확인
            if index < len(img_files):
                number = re.search(r'pic_free(\d+)', img_files[index]).group()
                    
                if number == "pic_free{}".format(i + 1):
                    # 파일이 존재하는 경우, 이미지 표시
                    st.image(img_files[index], width=300, use_column_width=True)
                    index += 1
                else:
                    # 파일이 존재하지 않는 경우, 기본 이미지 출력
                    st.image(logo_path, width=300, use_column_width=True)
            else:
                # 리스트의 인덱스가 범위를 벗어난 경우, 기본 이미지 출력
                st.image(logo_path, width=300, use_column_width=True)
    
        with col2:
            # 데이터를 2열로 구성한 데이터프레임 생성 (인덱스 열 없음)
            df = pd.DataFrame({
                '작성': ['제목', '내용'],
                '내용': [title[i], content[i]]
            })
        
            df = df.reset_index(drop=True)
            st.dataframe(df, width=700)

    