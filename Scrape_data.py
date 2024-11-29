import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
import time
import Config_topic

# Load the pretrained model from Hugging Face for sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis")

def get_sentiment(text):
    # Use Hugging Face's sentiment-analysis pipeline
    result = sentiment_analyzer(text)
    
    sentiment = result[0]['label']  # 'LABEL_0' for negative, 'LABEL_1' for positive
    return sentiment

def scrape_news(topic):
    newz_collab = []
    base_url = 'https://news.google.com/'
    response_ = requests.get(f"https://news.google.com/search?q={topic}&hl=en-IN&gl=IN&ceid=IN%3Aen")
    response = response_.content
    soup = BeautifulSoup(response, "lxml")
    news = soup.find_all("article", class_="IFHyqb DeXSAc")
    
    for newz in news:
        try:
            newspaperName = newz.find("div", class_="vr1PYe").text
            newsheadLine = newz.find("a", class_="JtKRv").text
            time = newz.find("time", class_="hvbAAd").text
            link_to_article = newz.a['href']
            real_link = base_url + link_to_article

            # Make the link clickable in HTML format
            clickable_link = f'<a href="{real_link}" target="_blank">click here</a>'

            sentiment = get_sentiment(newsheadLine)

            newz_collab.append([newspaperName, newsheadLine, sentiment, clickable_link, time])
        except Exception as e:
            print(f"Error processing news article: {e}")
    
    return newz_collab

def main():
    st.title("Analyzing the Sentiment of the Scraped Data")

    query = Config_topic.topic
    st.write("Please click on the below button for sentiment analysis")
    
    if st.button('Analyze Sentiment'):
        if query:
            news_data = scrape_news(query)  # Call the scrape_news function with user input

            if news_data:
                df = pd.DataFrame(news_data,
                                  columns=["Newspaper Name", "News Headline", "Sentiment", "Real Link", "Time"])

                st.success('Analyzed successfully! Displaying results:')
                
                # Display the DataFrame with clickable links
                st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

                st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name='news_data.csv',
                                   mime='text/csv')
            else:
                st.warning('No news found for the given topic.')
        else:
            st.error('Please enter a topic to search for news.')

if __name__ == "__main__":
    main()
