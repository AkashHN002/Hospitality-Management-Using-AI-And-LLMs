import streamlit as st
import os
import time
import json
from src.Alert import  send_email, send_alert
from src.Sentiment_model import Sentiment_provider, Suggestion_provider, model, get_gemini_response
from src.Recommendation import Recommendation
from dotenv import load_dotenv
load_dotenv()


st.set_page_config( page_title="Staff Alerting System",)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        padding-bottom: 2rem;
    }
    .stSelectbox > label {
        font-size: 1.2rem;
        color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Staff Alerting System")

user_id = st.text_input("Enter User ID")
text = st.text_area("Provide us a feedback")

response_prompt = f"""You are a resturant manager who gives response for the user who entered the feedback based on the sentiment of the feedback.
User has given given the following feedback, Feedback = {text}.\n Plese provide a response.
Start as 'Dear Guest, Thank you for your feedback...' and also include ' will use them to improve our services and address the issues you raised.'
Keep it simple and short, like 3 to 4 sentences."""

sub = st.button("Submit")
llm = model()

if sub:
    response = get_gemini_response(llm, response_prompt)
    print(response_prompt)
    st.write(response)

    sender_email = "akashhntest@gmail.com"
    sender_password = os.getenv('SENDER_PASS')
    receiver_email = "akashhn06@gmail.com"
    
    recommendations = Recommendation()
    recommendations = recommendations.getRecommendations(user_id, 4)

    prompt = f"""You are a recommendation engine suggest users to visit the given areas of hotel like advertising it.
Recommend areas: {recommendations}, to user"
Example: {json.dumps({'Swimming pool': 'You must visit our Swimming Pool, it is the best in the city!'})}
Return the response in JSON format with the structrue: 
*  include the ares as keys and recommendation as values."""
    
    rec_response = get_gemini_response(llm, prompt)
    
    st.write("Here are some recommendations You may like")
    recommendations = json.loads(rec_response.split('```')[-2].replace("json",""))

    container = st.container()
    if len(recommendations) > 0:
        for area, value in recommendations.items():
            with container.expander(area.replace("_"," ").upper(), expanded=True):
                st.write(value)
                
    time1 = time.time()
    sentiment_data = Sentiment_provider(text)
    suggestions = None
    formatted_data = None

    if sentiment_data['Sentiment'] == "Negative":
        suggestions = Suggestion_provider(sentiment_data, text)
    
        formatted_data = "\n".join([f"*{key.upper()}*: {value}" for key, value in suggestions.items()])

    body = (
        f"USER ID: {user_id}\n\n"
        f"SENTIMENT: {'⚠️ '+ sentiment_data['Sentiment'] if sentiment_data['Sentiment'].lower() == 'negative' else sentiment_data['Sentiment'] }\n\n"
        f"FEEDBACK: {text}\n\n"
        f"SUGGESTION: \n\n{formatted_data if formatted_data is not None else 'No Suggestions'}"
    )
    
    send_alert(body)
    print("Alert sent to Slack channel.")
    subject = "Alert for User Feedback"
    send_email(sender_email, sender_password, receiver_email, subject, body)
    print("Aletr Email sent successfully.")

    subject = "Recommendation"

    formated_recs = "Recommended Activities for you based on your interaction:\n"+"\n".join([f"*{key.upper()}*: {value}" for key, value in recommendations.items()])
    send_email(sender_email, sender_password, receiver_email, subject, formated_recs)
    print("Recommendation Email sent successfully.")

    time2 = time.time()
    
    print("Timee taken: ", time2 - time1)


