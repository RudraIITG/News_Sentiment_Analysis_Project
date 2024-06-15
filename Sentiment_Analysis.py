import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob  # or import NLTK for sentiment analysis
import time
import Config_topic

def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


def scrape_news(topic):
    newz_collab = []
    base_url = 'https://news.google.com/'
    response_ = requests.get(f"https://news.google.com/search?q={topic}&hl=en-IN&gl=IN&ceid=IN%3Aen")
    response = response_.content
    soup = BeautifulSoup(response, "lxml")
    news = soup.find_all("article", class_="IFHyqb DeXSAc")
    for newz in news:
        newspaperName = newz.find("div", class_="vr1PYe").text
        newsheadLine = newz.find("a", class_="JtKRv").text
        time = newz.find("time", class_="hvbAAd").text
        link_to_article = newz.a['href']
        real_link = base_url+ link_to_article

        sentiment = get_sentiment(newsheadLine)

        newz_collab.append([newspaperName, newsheadLine, time, real_link, sentiment])

    return newz_collab

