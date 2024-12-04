import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from gensim.models import Word2Vec
import joblib
import numpy as np
import Config_topic


def load_models():
    # Load the Word2Vec model (ensure it's in the correct directory)
    word2vec_model = Word2Vec.load("word2vec.model")  # Adjust the path as necessary
    
    # Load the sentiment model
    sentiment_model = joblib.load("sentiment_model.joblib")
    
    return word2vec_model, sentiment_model


def get_word2vec_embedding(text, word2vec_model):
    # Tokenize the text into words and get embeddings
    words = text.split()
    embeddings = []

    for word in words:
        if word in word2vec_model.wv:
            embeddings.append(word2vec_model.wv[word])
    
    # Average the embeddings to represent the sentence
    if embeddings:
        sentence_embedding = np.mean(embeddings, axis=0)
        return sentence_embedding
    else:
        # Return a zero vector if no words have embeddings
        return np.zeros(word2vec_model.vector_size)


def get_sentiment(text, word2vec_model, sentiment_model):
    # Get the embedding for the text
    embedding = get_word2vec_embedding(text, word2vec_model)
    
    # Predict the sentiment using the trained sentiment model
    sentiment = sentiment_model.predict([embedding])
    
    # Map model's prediction to sentiment label
    if sentiment == 1:
        return 'Positive'
    elif sentiment == 0:
        return 'Neutral'
    else:
        return 'Negative'


def scrape_news(topic, word2vec_model, sentiment_model):
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
        real_link = base_url + link_to_article

        # Make the link clickable in HTML format
        clickable_link = f'<a href="{real_link}" target="_blank">click here</a>'

        sentiment = get_sentiment(newsheadLine, word2vec_model, sentiment_model)

        newz_collab.append([newspaperName, newsheadLine, sentiment, clickable_link, time])

    return newz_collab


def main():
    st.title("Analyzing the Sentiment of the Scraped Data")

    # Load the models
    word2vec_model, sentiment_model = load_models()

    query = Config_topic.topic
    st.write("Please click on the below button for sentiment analysis")
    
    if st.button('Analyze Sentiment'):
        if query:
            news_data = scrape_news(query, word2vec_model, sentiment_model)  # Call the scrape_news function with user input

            if news_data:
                df = pd.DataFrame(news_data,
                                  columns=["Newspaper Name", "News Headline", "Sentiment", "Real Link", "Time"])

                st.success('Analyzed successfully! Displaying results:')
                
                # Display the DataFrame with clickable links
                st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

                st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name='../news_data.csv',
                                   mime='text/csv')
            else:
                st.warning('No news found for the given topic.')
        else:
            st.error('Please enter a topic to search for news.')


if __name__ == "__main__":
    main()
