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
    except:
        st.info("Stored articles will be generated soon.")
        return
    
    for _, row in df.groupby(by="duplication_id").agg(func=list).iterrows():
        with st.expander(f"Duplication ID: {row.name}"):
            for idx, article_id in enumerate(row["id"]):
                st.markdown(row["content"][idx])
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
        
        if post != thread[-1]:
            sleep(.2)

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
            
            st.button(
                label="Publish",
                key=uuid4(),
                on_click=lambda: publish_thread(row["thread"]),
            )

StoredArticlesPage = st.Page(stored_articles_page_generator, title="Stored Articles")
ThreadsPage = st.Page(threads_page_generator, title="Threads")

_ = st.navigation(
    [StoredArticlesPage, ThreadsPage],
    position="top",
)

_.run()