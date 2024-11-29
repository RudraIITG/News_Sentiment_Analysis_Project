        newz_collab.append([newspaperName, newsheadLine, time, clickable_link])
    return newz_collab


def stream_data(welcome):
    for word in welcome.split(" "):
        yield word + "  "  # yield creates a generator function
        time.sleep(0.1)


welcome = "Thank You for using our webapp"


def app():
    st.title("Scraping Data From Multiple Websites")
    st.title("News Sentiment Analyzer")
    Config_topic.topic = st.text_input("Enter the topic to scrape for news:")
    st.write_stream(stream_data(welcome))

    if st.button('Search'):
        if Config_topic.topic:
            news_data = scrape(Config_topic.topic)
            if news_data:
                df = pd.DataFrame(news_data, columns=["newspaperName", "newsheadLine", "time", "link_To_Article"])
                csv_file = '../news_data.csv'
                df.to_csv(csv_file, index=True)

                st.success('Scraping successful! Data saved to news_data.csv.')

                # Display the DataFrame with clickable links
                st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

                Config_topic.news_Number += 1
                st.download_button(label="Download CSV", data=df.to_csv(index=False),
                                   file_name='../news_data_{}.csv'.format(Config_topic.news_Number), mime='text/csv')
            else:
                st.warning('No news found for the given topic.')
        else:
            st.error('Please enter a topic.')


if __name__ == "__app__":
    app()
