import requests
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import smtplib
from email.message import EmailMessage
import ssl
import os
import time
from src.Sentiment_model import Sentiment_provider, Suggestion_provider
from src.Recommendation import Recommendation
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
 
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

gemini_model.temperature = 0.4


def get_gemini_response(user_prompt):
    response = gemini_model.generate_content(user_prompt)
    return response.text


def send_email(sender_email, sender_password, receiver_email, subject, body):
    
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as sm:
            sm.login(sender_email, sender_password)
            sm.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        

st.set_page_config(layout="wide", page_title="Data Transformation Tool")


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

if sub:
    response = get_gemini_response(response_prompt)
    print(response_prompt)
    st.write(response)

    sender_email = "akashhntest@gmail.com"
    sender_password = "vizj akfu qhol mggj"
    receiver_email = "akashhn06@gmail.com"
    
    recommendations = Recommendation()
    recommendations = recommendations.getRecommendations(user_id, 4)

    rec_response = get_gemini_response(f"You are a recommendation engine suggest users to visit the given areas of hotel like advertising it."
                                f"Recommend areas: {recommendations}, to user"
                                "Example: {'Swimming pool': 'You must visit our Swimming Pool, it is the best in the city!'}"
                                "Return the response in JSON format with the structrue: "
                                "*  include the ares as keys and recommendation as values."
                                )
    
    st.write("Here are some recommendations You may like")
    recommendations = json.loads(rec_response.split('```')[-2].replace("json",""))
    print(recommendations)
    container = st.container()
    if len(recommendations) > 0:
        for area, value in recommendations.items():
            with container.expander(area.replace("_","").upper(), expanded=True):
                st.write(value)
    time1 = time.time()
    sentiment_data = Sentiment_provider(text)
    suggestions = None
    formatted_data = None

    if sentiment_data['Sentiment'] == "Negative":
        suggestions = Suggestion_provider(sentiment_data, text)
    
        formatted_data = "\n".join([f"*{key.upper()}*: {value}" for key, value in suggestions.items()])

    body = f"USER ID: {user_id}\n\nSENTIMENT: {sentiment_data['Sentiment']}\n\nFEEDBACK: {text}\n\nSUGGESTION: \n\n{formatted_data if formatted_data is not None else 'No Suggestions'}"
    subject = "Alert for User Feedback"
    send_email(sender_email, sender_password, receiver_email, subject, body)

    subject = "Recommendation"
    send_email(sender_email, sender_password, receiver_email, subject, rec_response)
    
    # Slcak Chanel
    # slack_data = {
    #     'text':body
    #     }
    # response = requests.post(
    #     webhook_url, data=json.dumps(slack_data),
    #     headers={'Content-Type': 'application/json'}
    # )

    time2 = time.time()
    
    print("Timee taken: ", time2 - time1)
    print('Alerts sent successfully.')

