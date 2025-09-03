"""
Streamlit interface.
"""

from config import STORED_ARTICLES_FILE_NAME, THREADS_FILE_NAME, X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
import json
import pandas as pd
import streamlit as st
from time import sleep
import tweepy
from uuid import uuid4

X = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_KEY_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

def stored_articles_page_generator():
    st.title("Stored Articles")
    
    try:
        df = pd.read_csv(STORED_ARTICLES_FILE_NAME)
        if len(df) == 0:
            raise BaseException()
    except:
        st.info("Stored articles will be generated soon.")
        return
    
    st.text(f"Total {len(df)} articles.")
    for _, row in df.groupby(by="duplication_id").agg(func=list).iterrows():
        with st.expander(f"Duplication ID: {row.name}"):
            for idx, article_id in enumerate(row["id"]):
                st.text(row["content"][idx].strip("-"))
                if article_id != row["id"][-1]:
                    st.divider()

def publish_thread(thread):
    prev = None
    for post in thread:
        if prev is None:
            prev = X.create_tweet(
                text=post
            )
        else:
            prev = X.create_tweet(
                text=post,
                in_reply_to_tweet_id=prev.data["id"]
            )

def generate_thread_delete_handler(idx):
    def _():
        try:
            df = pd.read_csv(THREADS_FILE_NAME)
            if len(df) == 0:
                raise BaseException()
        except:
            return
        
        df = df.drop(index=idx, axis=1)
        df.to_csv(THREADS_FILE_NAME, index=False)
    
    return _

def generate_thread_publish_handler(idx):
    def _():
        try:
            df = pd.read_csv(THREADS_FILE_NAME)
            if len(df) == 0:
                raise BaseException()
        except:
            print("H")
            return
        
        publish_thread(json.loads(df.at[idx, "thread"]))
        
    return _

def threads_page_generator():
    st.title("Threads")
    
    try:
        df = pd.read_csv(THREADS_FILE_NAME)
        if len(df) == 0:
            raise BaseException()
        df["thread"] = df["thread"].map(json.loads)
    except BaseException as e:
        st.info("Threads will be generated soon.")
        return
    
    for _, row in df.iterrows():
        with st.expander(row['title']):
            for x in row["thread"]:
                st.text(x)
                if x != row["thread"][-1]:
                    st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.button(
                    label="Publish",
                    key=uuid4(),
                    on_click=generate_thread_publish_handler(_),
                )
            
            with col2:
                st.button(
                    label="Delete",
                    key=uuid4(),
                    on_click=generate_thread_delete_handler(_), 
                )

StoredArticlesPage = st.Page(stored_articles_page_generator, title="Stored Articles")
ThreadsPage = st.Page(threads_page_generator, title="Threads")

_ = st.navigation(
    [StoredArticlesPage, ThreadsPage],
    position="top",
)

_.run()