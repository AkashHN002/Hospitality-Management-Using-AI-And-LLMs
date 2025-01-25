import streamlit as st

st.set_page_config(
    page_title = "Stock Price Page",
    page_icon= "💲"
)

sentiment_page = st.Page(
    page = "src/Sentiment_model.py",
    title = "Sentiment Analysis",
    icon = ":material/bar_chart:",
    default = True,
)

recommendation_page = st.Page(
    page = "src/Recommendation.py",
    title = "Recommendation",
    icon = ":material/batch_prediction:"
)


profile_page = st.Page(
    page = "src/Profile.py",
    title = "Profile Management",
    icon = ":material/thumb_up:"
)

alert_page = st.Page(
    page = "src/Alert.py",
    title = "Send Alert",
    icon = ":material/email:"

)

pg = st.navigation(pages = [sentiment_page,recommendation_page, profile_page, alert_page])
pg.run()

