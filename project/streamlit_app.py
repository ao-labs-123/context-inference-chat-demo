import streamlit as st
from inference.classify import classify

text = st.text_area("文を入力してください")

if text:
    results = classify(text)
    st.write("分類結果:", results)