import requests
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

data = pd.read_csv(r"Notebook/Interaction.csv")
rating_matrix = data.pivot_table(index='User_ID', columns="Activity", values="Rating").fillna(0)
time_matrix = data.pivot_table(index='User_ID', columns="Activity", values="Time_Spent").fillna(0)
matrix = ( rating_matrix * 0.7) + (time_matrix * 0.3)

webhook_url = "https://hooks.slack.com/services/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"
# webhook_url = "https://hooks.slack.com/services/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"


def Sentiment_provider(text):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
        },

        data=json.dumps({
            "model": "openai/gpt-3.5-turbo", 
            "messages": [
            {
                "role":"system",
                "content":"You are a sentiment analysist who outputs the sentiment and the departments/areas mentioned in review in JSON."
                f"The JSON object must use the schema : {json.dumps({'Sentiment':'Positive/Negative', "Areas":[]})}"
            },
            {
                "role": "user",
                "content": f"Provide the Sentiment of {text}",
            }
            ],
            "response_format":{"type": "json_object"}

        })
        )

    Sentiment_dict =  json.loads(response.json()['choices'][0]['message']['content'])
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
        },

        data=json.dumps({
            "model": "openai/gpt-3.5-turbo",
            "messages":[
                {
                    "role":"system",
                    "content":f"You are a suggestion provider who gives suggestion imporve areas mentioned by the help of review text and return area name and suggestion in JSON.\n"
                    f"The JSON object must use the schema : {json.dumps({'Area':'Suggestion'})}"
                },
                {
                    "role": "user",
                    "content": f"Provide the Suggestion  to improve areas :{Sentiment_dict['Areas']} by analysing {text}",
                }
            ],
            "response_format":{"type": "json_object"}
            
        })
    )
    return json.loads(response.json()['choices'][0]['message']['content']), Sentiment_dict['Sentiment']



def getRecommendations(user_id, matrix, k = 3):
    user_data = matrix[matrix.index == user_id]
    other_user = matrix[matrix.index != user_id]
    similar_matrix = cosine_similarity(user_data, other_user)[0].tolist()


    user_indices = dict(zip(other_user.index, similar_matrix))
    similar_user = sorted(user_indices.items(), key = lambda x: x[1], reverse = True)
    top_similar_user = similar_user[:k]
    users = [u[0] for u in top_similar_user]

    similar_user_indices= users
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    similar_users = similar_users.mean(axis = 0)
    similar_users_df = pd.DataFrame(similar_users, columns = ['mean'])

    user_df = matrix[matrix.index == user_id].T
    user_df.columns = ['ratings']
    user_df = user_df[user_df['ratings'] == 0]

    unseen_data = user_df.index.tolist()
    similar_user_data = similar_users_df[similar_users_df.index.isin(unseen_data)].sort_values(by = 'mean', ascending = False)

    recommonded_activity = similar_user_data.head(k)

    return recommonded_activity.index.tolist()

def send_email(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        
        server = smtplib.SMTP('smtp.mailtrap.io', 2525)  
        server.starttls()  
        server.login(sender_email, sender_password)  
        server.send_message(msg)
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")
        

activities = {
        'amenities': ['pool', 'spa', 'gym', 'tennis_court', 'business_center'],
        'dining': ['main_restaurant', 'cafe', 'bar', 'room_service', 'buffet'],
        'activities': ['city_tour', 'beach_activity', 'cooking_class', 'yoga', 'golf']
}

details = {}
user_id = st.text_input("Enter User ID")
text = st.text_input("Provide us a feedback")
sub = st.button("Submit")
if sub:
    st.write(f"Hello {user_id}")

    sender_email = "f99464769a8706"
    sender_password = "c09e4af96bb041"
    receiver_email = "akashhn06@gmail.com"
    subject = "Test Email"

    recommendations = getRecommendations(user_id, matrix)
    # formated_recs = "You may also like :\n" + "\n".join(recommendations["Recommondations"])

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },

    data=json.dumps({
        "model": "openai/gpt-3.5-turbo",
        "messages":[
            {
                "role":"system",
                                "content":f"You are a recommondation provider who suggest user to visit the areas mentioned as an advertisement"

            },
            {
                "role": "user",
                "content": f"Recommend {recommendations} to user"
            }
        ],
    })
    )
    body = response.json()['choices'][0]['message']['content']

    send_email(sender_email, sender_password, receiver_email, subject, body)


    output, sentiment = Sentiment_provider(text)

    formatted_data = "\n".join([f"*{key.upper()}*: {value}" for key, value in output.items()])
    slack_data = {
        'text':f'*USER ID*: {user_id}\n\n*SENTIMENT*: {sentiment}\n\n*FEEDBACK*: {text}\n\n*SUGGESTION*: \n\n{formatted_data}'
        }
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}'
        )
    else:
        print('Alerts sent successfully.')

    
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },

    data=json.dumps({
        "model": "openai/gpt-3.5-turbo",
        "messages":[
            {
                "role":"system",
                "content":f"You are a resturant manager who gives response for the user who entered the feedback based on the sentiment of the feedback"
            },
            {
                "role": "user",
                "content": f"Give response to {text}"
            }
        ],
    })
    )
    st.write(response.json()['choices'][0]['message']['content'])
    

    