import streamlit as st
import pandas as pd
import Config_topic
import requests
from textblob import TextBlob  # or import NLTK for sentiment analysis
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# import numpy as np




# Most frequent word used
def most_used_word(df):
    text = ' '.join(df['News Headline'].tolist())
    wordcloud = WordCloud(width=2000, height=1000,background_color='Black',colormap="Set2").generate(text)

    plt.figure(figsize=(20, 15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # wordcloud.to_file("Freq.png")
    _ = plt.title('Word Frequency in Headlines')
    st.pyplot(plt)


#News Coverage by NewsPaper
def news_Coverages(df):
    newspapers = df['Newspaper Name'].value_counts()

    plt.figure(figsize=(10, 6))
    plt.bar(newspapers.index, newspapers.values)
    plt.xlabel('Newspaper')
    plt.ylabel('Number of Articles')
    plt.title('News Coverage by Newspaper')
    _=plt.xticks(rotation=90)
    # plt.savefig("News Coverage by Newspaper.png")
    st.pyplot(plt)

#Num of positive negative and neutral news
def Num_of_sentiments(df):
    sentiments = df["Sentiment"].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(sentiments.index, sentiments.values)
    plt.xlabel('sentiments')
    plt.ylabel('Num of sentiments')
    plt.title('Sentiments BarPlot')
    _ = plt.xticks(rotation=90)
    # plt.savefig("S.png")
    st.pyplot(plt)
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
        real_link = base_url+link_to_article

        sentiment = get_sentiment(newsheadLine)

        newz_collab.append([newspaperName, newsheadLine, time, real_link, sentiment])

    return newz_collab

def app():
    st.title("Getting Insights from Data")
    query = Config_topic.topic
    df = None
    if query:
        news_data = scrape_news(query)  # Call the scrape_news function with user input

        if news_data:
            df = pd.DataFrame(news_data,
                              columns=["Newspaper Name", "News Headline", "Time", "Real Link", "Sentiment"])

        else:
            st.warning('No news found for the given topic.')
    else:
        st.error('Please enter a topic to search for news.')

    choices = ["Most Frequent word","News Coverage By NewsPapers","Sentiment Stats"]
    option = st.selectbox(
   "what type of Visualization you want to see?",
    options=choices,
    index=None)
    if st.button("Show"):
        if option:
            if option == "Most Frequent word":
                most_used_word(df)
            elif option == "News Coverage By NewsPapers":
                news_Coverages(df)
            elif option == "Num of sentiments":
                Num_of_sentiments(df)
        else:
            st.error("Please select a valid option")

if __name__ == "__app__":
    app()
