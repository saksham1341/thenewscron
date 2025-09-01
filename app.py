"""
Streamlit interface.
"""

from config import STORED_ARTICLES_FILE_NAME, THREADS_FILE_NAME
import json
import pandas as pd
import streamlit as st

def stored_articles_page_generator():
    st.title("Stored Articles")
    
    try:
        df = pd.read_csv(STORED_ARTICLES_FILE_NAME)
    except:
        st.info("Stored articles will be generated soon.")
        return
    
    for _, row in df.groupby(by="duplication_id").agg(func=list).iterrows():
        with st.expander(f"Duplication ID: {row.name}"):
            for idx, article_id in enumerate(row["id"]):
                st.markdown(f"#### {row['title'][idx]}")
                st.markdown(row["content"][idx])
                if article_id != row["id"][-1]:
                    st.divider()

def threads_page_generator():
    st.title("Threads")
    
    try:
        df = pd.read_csv(THREADS_FILE_NAME)
        df["thread"] = df["thread"].map(json.loads)
    except:
        st.info("Threads will be generated soon.")
        return
    
    for _, row in df.iterrows():
        with st.expander(row['title']):
            for x in row["thread"]:
                st.text(x)
                if x != row["thread"][-1]:
                    st.divider()

StoredArticlesPage = st.Page(stored_articles_page_generator, title="Stored Articles")
ThreadsPage = st.Page(threads_page_generator, title="Threads")

_ = st.navigation(
    [StoredArticlesPage, ThreadsPage],
    position="top",
)

_.run()