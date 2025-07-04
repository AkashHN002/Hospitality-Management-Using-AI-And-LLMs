import streamlit as st
import os
import time
import json

from src.Alert import  send_email, send_alert
from src.Sentiment_model import Sentiment_provider, Suggestion_provider, model, get_gemini_response
from src.Recommendation import Recommendation
from src.Profile import DataBaseManager

import random
from dotenv import load_dotenv
load_dotenv()



st.set_page_config(
    page_title="Staff Alerting System",
    page_icon="🏨",
    initial_sidebar_state="collapsed"
)

# Enhanced custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .stTitle {
        color: #2c3e50;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        font-style: italic;
    }
    
    .feedback-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #3498db;
    }
    
    .recommendation-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border-left: 5px solid #27ae60;
    }
    
    .response-section {
        background: #ecf0f1;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #e74c3c;
    }
    
    .stTextInput > label, .stTextArea > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #bdc3c7;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #bdc3c7;
        padding: 0.75rem;
        font-size: 1rem;
        min-height: 120px;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;

    }
    
    .response-card{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
            
    .recommendation-card {
        background: #ffffff;
        border: 1px solid #ecf0f1;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
        font-size: 1rem;
    }
    
    .section-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .processing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #7f8c8d;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

activities = {
        'amenities': ['pool', 'spa', 'gym', 'tennis_court', 'business_center'],
        'dining': ['main_restaurant', 'cafe', 'bar', 'room_service', 'buffet'],
        'activities': ['city_tour', 'beach_activity', 'cooking_class', 'yoga', 'golf']
}

values = list([ i.replace("_"," ").title() for i  in [j for i in activities.values() for j in i]])

database = DataBaseManager()
llm = model()
recommendations = Recommendation()


st.title("🛎️Staff Alerting System")

user_id = st.text_input(
    "User ID", 
    placeholder="Enter user identification number",
    help="Unique identifier for the user providing feedback"
)


text = st.text_area(
    "Feedback Details", 
    placeholder="Please share your experience with us in detail...",
    help="Provide comprehensive feedback about your experience"
)


response_prompt = f"""You are a resturant manager who gives response for the user who entered the feedback based on the sentiment of the feedback.
User has given given the following feedback, Feedback = {text}.\n Plese provide a response.
Start as 'Dear Guest, Thank you for your feedback...' and also include ' will use them to improve our services and address the issues you raised.'
Keep it simple and short, like 3 to 4 sentences."""


container = st.container()
with container.expander("Please prvide rating for the activities you have visited"):
    st.write("Please select the activity you have visited ")
    selection = st.selectbox(
        "Select the file to be processed:",
        options=values,
        # format_func=lambda x: options[x],
        index=None,
        label_visibility='collapsed' 
    )

    if selection is not None:

        selection = selection.replace(" ", "_").lower()
        choosed = [ i for i in activities.keys() if selection in activities[i] ]

        rating = st.slider("Rate the activity (0-5):", 0, 5, 3)
        time_spent = random.randint(30, 180)  # Random time spent between
        if st.button("Done"):
            if database.add_interaction(
                user_id=user_id, 
                category=choosed[0], 
                preference=selection, 
                rating=rating, 
                time_spent=time_spent
                ):
                st.success("Thank you for the response✨!")
                st.empty()
                
            else:
                st.error("Something went wrong. Please try again later.")
sub = st.button("Submit")

if sub:
    # Response to user feedback
    response = get_gemini_response(llm, response_prompt)


    st.markdown("<div class='section-header'>💬 Management Response</div>", unsafe_allow_html=True)
    st.markdown(f"""
            <div class="response-card">
                <p style="color: #2c3e50; margin-bottom: 1rem;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
   

    sender_email = "hospitality716@gmail.com"
    sender_password = os.getenv('SENDER_PASS')
    receiver_email = "akashhntest@gmail.com"

    # Generating Recommendation for the user_id
    recommendations = recommendations.getRecommendations(user_id, 4)

    # improving the recommendation
    prompt = f"""You are a recommendation engine. suggest users to visit the given areas of hotel like advertising it.
Areas: {recommendations}.

Example: 
    Areas= ['Swimming pool']
    Response:
    {json.dumps({'Swimming pool': 'You must visit our Swimming Pool, it is the best in the city!'})}
Return the response in JSON format with the structrue: 
*  include the Areas as keys and recommendation as values."""
    
    rec_response = get_gemini_response(llm, prompt)
    print("Recommendations: ", recommendations)

    # Providing recommendation
    recommendations = json.loads(rec_response.split('```')[-2].replace("json",""))
    # container = st.container()
    # if len(recommendations) > 0:
    #     for area, value in recommendations.items():
    #         with container.expander(area.replace("_"," ").upper(), expanded=True):
    #             st.write(value)
    st.markdown("<div class='section-header'>🌟 Activites you may also like</div>", unsafe_allow_html=True)

    for i,( area, value )in enumerate(recommendations.items()):
        st.markdown(f"""
        <hr style='border: none; border-top: 1px solid #ccc; margin: 1rem 0;'/>
        <h4>{area.replace('_',' ').title()} </h4>
        <div class='recommendation-card'>
            <p style='margin: 0; font-size: 1.1rem; line-height: 1.6;'>{value}</p>
        </div>
        """, unsafe_allow_html=True)
        if i == len(recommendations.values()) - 1:
            st.markdown("<hr style='border: none; border-top: 1px solid #ccc; margin: 1rem 0;'/>", unsafe_allow_html=True)
            
    time1 = time.time()
    # Analysing the sentiment  of the feedback and the areas mentioned by the user in feedback
    sentiment_data = Sentiment_provider(text)
    suggestions = None
    formatted_data = None

    if sentiment_data['Sentiment'] == "Negative":
        # Getting suggestion for the areas by the help of feedback
        suggestions = Suggestion_provider(sentiment_data, text)
        
        formatted_data = "\n".join([f"*{key.upper()}*: {value}" for key, value in suggestions.items()])
    # Preparing the mail for alert
    body = (
        f"USER ID: {user_id}\n\n"
        f"SENTIMENT: {'⚠️ '+ sentiment_data['Sentiment'] if sentiment_data['Sentiment'].lower() == 'negative' else sentiment_data['Sentiment'] }\n\n"
        f"FEEDBACK: {text}\n\n"
        f"SUGGESTION: \n\n{formatted_data if formatted_data is not None else 'No Suggestions'}"
    )

    # sending Alert
    send_alert(body)
    print("Alert sent to Slack channel.")
    subject = "Alert for User Feedback"
    send_email(sender_email, sender_password, receiver_email, subject, body)
    print("Aletr Email sent successfully.")

    subject = "Recommended Activities for you based on your interaction"
    # Sending Recommendation
    formated_recs = "Activites recommended just for you:\n"+"\n".join([f"{key.upper()}: \n{value}" for key, value in recommendations.items()])
    send_email(sender_email, sender_password, receiver_email, subject, formated_recs)
    print("Recommendation Email sent successfully.")

    time2 = time.time()
    
    print("Timee taken: ", time2 - time1)

    
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
    <p>🏨 <strong>Staff Alerting System</strong> | Powered by AI-driven Customer Experience Management</p>
    <p style='font-size: 0.9rem;'>Ensuring exceptional service through intelligent feedback analysis</p>
</div>
""", unsafe_allow_html=True)

