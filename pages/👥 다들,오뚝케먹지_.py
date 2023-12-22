import streamlit as st
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import io
import platform
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import re
import os

#페이지 기본 설정
st.set_page_config(
    page_icon="😗",
    page_title="오뚝케먹지?!😋",
    layout="wide",
)

## Title
st.image('./pages/img/banner.png', use_column_width = True)
st.header("다들, 오뚝케 먹지?")

## Text
st.text("요리 레시피를 공유하는 페이지입니다. 자유롭게 공유하고 싶은 레시피를 작성해주세요!😊")

selected_page = st.sidebar.selectbox("오뚝케 먹지? 메뉴를 선택하세요.", ["레시피 등록하기", "레시피 목록보기"])

# 선택한 페이지에 따라 내용 표시
if selected_page == "레시피 등록하기":
    st.subheader("레시피 등록 페이지")

# 텍스트 저장 변수
    title = ""
    content = ""
    uploaded_image = None


    title = st.text_input("레시피 제목을 입력하세요.", "라면 100배로 맛있게 끓이는 법")
    
# 내용 입력
    time = st.text_area("요리 소요시간 작성(분 단위)", "10")
    content = st.text_area("요리에 대해 간단히 소개하세요.", "내용을 입력하세요.")
    level = st.slider("요리 난이도를 선택해주세요.", 1, 5)
    need = st.text_area("필요한 재료를 작성하세요.", "내용을 입력하세요.")
    recipe = st.text_area("구체적인 요리 순서와 방법을 작성해 주세요.", "내용을 입력하세요.")
    tag = st.multiselect("해시태그를 설정해주세요", ("밑반찬",
     "국/탕/찌개",
     "디저트",
     "면/만두",
     "밥/죽/떡",
     "양식"
     "양념/소스/잼"
     "기타"))
    
    # 사진 업로드 위젯 생성
    uploaded_image = st.file_uploader("사진을 업로드하세요 (선택사항)", type=["jpg", "jpeg", "png"])
    
    # "제출하기" 버튼 클릭
    if st.button("제출하기"):
        # csv 파일로 저장
        existing_data = pd.read_csv('./pages/db/db.csv', encoding='utf-8')

        new_data = {
            '이름': [title],
            '소개': [content],
            '난이도': [level],
            '소요시간': [time],
            '재료': [need],
            '레시피': [recipe],
            '해시태그': [','.join(tag)] if tag else ['']
        }
        
        new_df = pd.DataFrame(new_data)  
        
        updated_data = pd.concat([existing_data, new_df], ignore_index=True)
        
        updated_data.to_csv('./pages/db/db.csv', index=False, encoding='utf-8')
        
        if uploaded_image is not None:
            # 업로드된 사진을 바이너리 데이터로 읽어옴
            image_data = uploaded_image.read()
            
            n = len(updated_data)
    
            # 바이너리 데이터를 파일로 저장
            with open('./pages/db/pic{}.png'.format(n), 'wb') as file:
                file.write(image_data)
        
        st.success("게시글이 성공적으로 작성되었습니다.")
    

elif selected_page == "레시피 목록보기":
    st.title("레시피 목록 페이지")
    
    read_data = pd.read_csv('./pages/db/db.csv', encoding='utf-8')
    
    # DB 디렉토리 경로
    db_directory = './pages/db/'
    
    # 파일 이름 패턴을 정의합니다. 여기서는 "img"로 시작하고 ".png"로 끝나는 파일을 선택합니다.
    file_pattern = re.compile(r'^pic\d+\.png$', re.IGNORECASE)
    
    # DB 디렉토리에서 파일 이름 패턴과 일치하는 파일들만 가져오기
    matching_files = [file for file in os.listdir(db_directory) if file_pattern.match(file)]
    
    # 각 변수를 리스트로 저장
    recipe_title = read_data['이름']  # 레시피 제목
    recipe_content = read_data['소개']  # 요리 소요시간
    recipe_level = read_data['난이도']  # 요리 간단 설명
    recipe_time = read_data['소요시간']  # 재료
    recipe_need = read_data['재료']  # 레시피
    recipe_recipe = read_data['레시피'] # 요리 난이도
    recipe_tag = read_data['해시태그']  # 요리 해시태그

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
                number = re.search(r'pic(\d+)', img_files[index]).group()
                    
                if number == "pic{}".format(i + 1):
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
                '작성': ['레시피 제목', '요리 소요시간', '간단한 소개', '재료', '레시피', '요리 난이도', '해시태그'],
                '내용': [recipe_title[i], recipe_time[i], recipe_content[i], recipe_need[i], recipe_recipe[i], recipe_level[i], recipe_tag[i]]
            })
        
            df = df.reset_index(drop=True)
            st.dataframe(df, width=700)

    