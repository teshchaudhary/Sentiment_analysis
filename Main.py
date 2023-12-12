import pickle
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import joblib

RF_model = pickle.load(open('D:\Project_Sem\Techniques\RF.pkl', 'rb'))
SVM_model = joblib.load('D:\Project_Sem\Techniques\SVM_')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

main_icon = load_lottieurl("https://lottie.host/3a2793d6-4e67-4144-8223-ee2bdce42702/QNT6Uuxk1f.json")

lottie_coding = load_lottieurl(
    "https://assets7.lottiefiles.com/datafiles/B7iUeqzD4KNoXPu/data.json")

with st.sidebar:
    st_lottie('lottie_coding', height = 120, key = "coding")
    selected = option_menu('Choose a Model',

                           ['Random Forest Model',
                            'SVM Model',
                            'BERT Model'],
                           icons = ['bi bi-tree', 'bi bi-distribute-vertical', 'bi bi-robot'],
                           default_index = 0)

col1, col2 , col3 = st.columns([1,3,1])
with col1:
    st_lottie(main_icon, height=99)
with col2:
    st.markdown("<h1 style='font-size:45px;'>Sentiment Analysis</h1>", unsafe_allow_html=True)
with col3:
    pass

if (selected == "Random Forest Model"):
    st.success("You are using Random Forest Model now.")
    st.title("Enter your review")
    review_rf = st.text_area("")
    submit_rf = st.button('Analyze')

    if submit_rf:
        start_rf = time.time()
        prediction_rf = RF_model.predict([review_rf])
        end_rf = time.time()
        st.write('Time taken for Analysis: ', round(end_rf - start_rf, 2), 'seconds')

        res_rf = prediction_rf[0]

        if res_rf == "Positive":
            st.success(f"This is a {res_rf} comment")
        
        elif res_rf == "Negative":
            st.error(f"This is a {res_rf} comment")
        
        elif res_rf == "Neutral":
            st.warning(f"This is a {res_rf} comment")
        
        else:
            st.info(f"This is a {res_rf} comment")

if (selected == 'SVM Model'):
    st.success("You are using SVM Model now.")
    st.title("Enter your review")
    review_svm = st.text_area('')
    submit_svm = st.button('Analyze')

    if submit_svm:
        start_svm = time.time()
        prediction_svm = SVM_model.predict([review_svm])
        end_svm = time.time()
        st.write('Time taken for Analysis: ', round(end_svm - start_svm, 2), 'seconds')

        res_svm = prediction_svm[0]

    if submit_svm:
        if res_svm == 'Positive':
            st.success(f"This is a {res_svm} comment")
        elif res_svm == 'Negative':
            st.error(f"This is a {res_svm} comment")
        elif res_svm == 'Neutral':
            st.warning(f"This is a {res_svm} comment")

if (selected == "BERT Model"):

    st.success("You are using BERT Model now.")
    @st.cache_data()
    def sentiment_score(review):
        tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        tokens = tokenizer.encode(review, return_tensors='pt')
        result = model(tokens)
        score = int(torch.argmax(result.logits)) + 1

        if score < 3:
            return "Negative"
        elif score == 3:
            return "Neutral"
        else:
            return "Positive"
        
    st.title("Enter your review")
    user_input = st.text_area('')
    button = st.button("Analyze")

    if user_input and button :
        res_bert = sentiment_score(user_input)

        if res_bert == "Positive":
            st.success(f"This is a {res_bert} comment")
        
        elif res_bert == "Negative":
            st.error(f"This is a {res_bert} comment")
        
        elif res_bert == "Neutral":
            st.warning(f"This is a {res_bert} comment")