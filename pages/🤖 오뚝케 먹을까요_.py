import streamlit as st
from streamlit_chat import message

import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.prompts.prompt import PromptTemplate

# api key
os.environ["OPENAI_API_KEY"] = "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"

loader = CSVLoader(file_path="./data/total.csv", encoding="utf-8")
data = loader.load()

embeddings = OpenAIEmbeddings()
vectors = FAISS.from_documents(data, embeddings)

custom_template = """
너는 레시피를 찾아주는 AI 봇이야.
행동규칙은 다음과 같아.
csv 파일에서 사용자가 먹고 싶은 음식과 가장 유사한 레시피 하나를 찾아서 그 음식의 이름, 레시피재료, 레시피를 그대로 출력해줘.

- 이름 : 이름
\n\n
- 재료 : 레시피재료
\n\n
- 레시피 : 레시피
"""

CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo-16k'),
                                                                   retriever=vectors.as_retriever(),
                                                                   condense_question_prompt=CUSTOM_QUESTION_PROMPT)

#페이지 기본 설정
st.set_page_config(
    page_icon="😗",
    page_title="오뚝케먹지?!😋",
    layout="wide",
)

## Title
st.image('./pages/img/banner.png', use_column_width = True)
st.header("🤖 오뚝케 먹을까요?")

def conversational_chat(query):

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))

    return result["answer"]

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["안녕하세요! 어떤 음식을 만들고 싶으신가요? 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["👋"]

response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):

        user_input = st.text_input("Query:", placeholder="[메뉴이름] 레시피 찾아줘.", key='input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = conversational_chat(user_input)

        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
            if i != 0:
                message("다른 음식 레시피를 더 알고 싶으시다면, 페이지를 새로고침 해주세요.", avatar_style="thumbs")