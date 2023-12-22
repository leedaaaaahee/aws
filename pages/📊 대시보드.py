import platform
import seaborn as sns
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud
from konlpy.tag import Okt

font_manager.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
font_name = font_manager.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)

plt.rcParams['font.size'] = 16

# Streamlit 앱 제목 설정
st.title('데이터 시각화')

# 파일 업로드 위젯
uploaded_file = st.file_uploader("상품 판매 데이터 파일 업로드", type=["csv"], key=1)

if uploaded_file is not None:
    # 업로드한 파일을 DataFrame 으로 변환
    df = pd.read_csv(uploaded_file)
    
    # 데이터 프로파일링
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df.replace('[OTTOGI] Delicious COOKED RICE, Gluten free, Microwavable instant cooked rice, Precooked ready to eat container (7.40oz., 12 count)', '오뚜기밥', inplace=True)
    df.replace('[OTTOGI] Jin Ramen, Mild Flavor - Korean Instant Ramen Noodle, Best Tasting Soup Traditional Instant Ramen (120g) -18 Pack', '진라면 순한맛', inplace=True)
    df.replace('[OTTOGI] Jin Ramen, Spicy Flavor - Korean Instant Ramen Noodle, Best Tasting Soup Traditional Instant Ramen (120g) -18 Pack', '진라면 매운맛', inplace=True)
    df.replace('[OTTOGI] Premium Roasted Sesame Oil, 100% Pure Sesame Oil, Tradtional Korean Style oil (10.82 fl oz. 320ml)', '고소한 참기름', inplace=True)
    df.replace('[OTTOGI] JIN RAMEN KOREAN STYLE INSTANT NOODLE, RICH SPICY FLAVOR, Instant Cup Ramen, Best tasting soup ramen, traditional gourmet taste & easy to coo', '진라면컵 매운맛', inplace=True)
    df.replace('[OTTOGI] Jin Ramen Mild, KOREAN STYLE INSTANT CUP NOODLE, (65g) -6 Pack', '진라면컵 순한맛', inplace=True)
    
    # 'DESCRIPTION' 열에서 가장 빈도수가 높은 N개 상품 찾기
    top_n_products = df['DESCRIPTION'].value_counts().nlargest(5)
    top = top_n_products.index[-5]
    
    # 가장 많이 판매된 상품 표시
    st.write("가장 많이 판매된 상품:", top_n_products.index[-1])  # 가장 마지막 상품이 가장 많이 판매된 상품
    
    # 데이터를 내림차순으로 정렬
    top_n_products = top_n_products.iloc[::-1]
    
    with open('./pages/db/top.txt', 'w', encoding='utf-8') as file:
        file.write(top)
    
    # 고유한 색상 생성
    num_colors = len(top_n_products)
    colors = sns.color_palette('viridis', num_colors)
    
    # 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(top_n_products.index, top_n_products.values, color=colors)
    ax.set_xlabel('판매 갯수')
    ax.set_title('판매 갯수가 많은 상품 상위 5개')
    ax.set_yticklabels([])
    plt.tight_layout()
    
    # 색상 범례 추가 (역순으로 출력)
    legend_labels = [plt.Rectangle((0, 0), 1, 1, color=colors[i], label=top_n_products.index[i]) for i in range(num_colors)][::-1]
    ax.legend(legend_labels, top_n_products.index[::-1], loc='lower right')  # 아래로 내리기
    
    
    # Matplotlib 그래프를 Streamlit 앱에 표시
    st.pyplot(fig)

st.write("---")

# Streamlit 앱 제목 설정
st.title('유튜브 데이터 텍스트마이닝')

uploaded_file2 = st.file_uploader("유튜브 데이터 파일 업로드", type=["csv"], key=2)

if uploaded_file2 is not None:
    
    # wordcloud
    # 업로드된 파일을 Pandas DataFrame으로 읽어옴
    df = pd.read_csv(uploaded_file2)

    text = df['0'].astype(str).str.cat(sep=' ')
    
    if text:
        okt = Okt()
        nouns = okt.nouns(text)
        nouns = [word for word in nouns if len(word) > 1]  # 한 글자 단어 제외
        words = " ".join(nouns)
    
        wordcloud = WordCloud(font_path='C:/Windows/Fonts/NanumGothic.ttf', background_color='white', width=800, height=600).generate(words)
    
        # Word Cloud 그리기
        st.image(wordcloud.to_array())    

st.write("---")

# Streamlit 앱 제목 설정
st.title('상품별 Sentiment 원 그래프')

# CSV 파일 업로드 위젯 추가
uploaded_file3 = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"], key=3)

# CSV 파일 업로드 여부 확인 및 데이터프레임으로 읽어오기
if uploaded_file3 is not None:
    # 업로드한 CSV 파일을 Pandas 데이터프레임으로 읽어오기
    df = pd.read_csv(uploaded_file3)

    # 각 상품(product_name)별 Sentiment 결과 비율 계산
    sentiment_ratio = df.groupby("product_name")["sentiment"].value_counts(normalize=True).unstack(fill_value=0)

    # 원 그래프를 저장할 이미지 파일
    output_image_path = "./data/imgsentiment_pie_charts.png"

    # 이미지 그릴 캔버스 생성
    num_rows = (len(sentiment_ratio) + 1) // 2  # 행 수 계산 (한 줄에 두 개씩)
    fig, axs = plt.subplots(nrows=num_rows, ncols=2, figsize=(12, 4 * num_rows))

    # 색상 설정
    colors = ['#ff6666', '#66b3ff']  # 연한 빨간색, 연한 파란색

    # 각 상품별로 원 그래프 그리기
    for i, (product_name, row) in enumerate(sentiment_ratio.iterrows()):
        ax = axs[i // 2, i % 2]  # 서브플롯 위치 선택
        ax.pie(row, autopct='%1.1f%%', startangle=90, labels=None, colors=colors)
        ax.set_title(product_name, fontsize=14)  # 그래프 제목 상단에 위치
        ax.legend(["Negative", "Positive"], loc="upper right", fontsize=10, bbox_to_anchor=(1.2, 1))  # 범례 그래프 우측 상단에 위치

    # 이미지로 저장
    plt.tight_layout()
    plt.savefig(output_image_path, bbox_inches="tight")

    # 이미지를 화면에 표시
    st.image(output_image_path, use_column_width=True)

    # 이미지 확인
    plt.show()