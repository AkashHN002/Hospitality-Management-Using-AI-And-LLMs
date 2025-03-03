import streamlit as st
import os
src_dir = os.path.abspath("src")
# Define the pages
sentiment_page = st.Page(
    page="src/Sentiment_model.py",
    title="Sentiment Analysis",
    icon=":material/bar_chart:",
)

recommendation_page = st.Page(
    page="src/Recommendation.py",
    title="Recommendation",
    icon=":material/batch_prediction:"
)

profile_page = st.Page(
    page="src/Profile.py",
    title="Profile Management",
    icon=":material/thumb_up:"
)

alert_page = st.Page(
    page="src/Alert.py",
    title="Send Alert",
    icon=":material/email:",
    default=True
)

# Navigate through the pages
pg = st.navigation(pages=[sentiment_page, recommendation_page, alert_page, profile_page])
pg.run()
