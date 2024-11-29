import streamlit as st

from streamlit_option_menu import option_menu


import Scrape_data, Sentiment_Analysis, Data_Visualization
with st.sidebar:
    selected = option_menu(
        menu_title="NewsSuggestion",
        options=["Scrape Data", "View Articles by Sentiment", "Related Data"],
        icons=["database", "emoji-smile","bar-chart-line-fill"],
        menu_icon="newspaper",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "black"},
            "icons": {"color": "orange", "font-size": "15px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "red",
            },
            "nav-link-selected": {"background-color": "blue"},
        },
    )

if selected == "Scrape Data":
    # st.title(f"You entered {selected}")
    Scrape_data.app()
if selected == "Analyze Sentiment":
    # st.title(f"You entered {selected}")
    Sentiment_Analysis.main()
if selected == "Data Visualization":
    # st.title(f"You entered {selected}")
    Data_Visualization.app()
