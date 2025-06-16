import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai 

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
 
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

gemini_model.temperature = 0.4


def get_gemini_response(user_prompt):
    response = gemini_model.generate_content(user_prompt)
    return response.text


api = "api_key"
url = "url"

def Sentiment_provider(text):
    response = get_gemini_response(f"""Provide the Sentiment and all departments/areas which are related to hotel mentioned in given text.
    Text = {text}.
    Return the response in JSON format with the structrue:
    *  include key `Sentiment` with value as 'Positive' or 'Negative'.
    *  include key `Areas` with value as a list of departments/areas mentioned in the text.""")
    print(response)

    return json.loads(response.split('```')[-2].replace('json',""))


def Suggestion_provider(Sentiment_dict:dict, text):
    
    response = get_gemini_response(
        f"Provide the Suggestion to improve areas :{Sentiment_dict['Areas']}, by analysing review: {text}"
        f"""Return the response in JSON format with the structrue:
            *  include the `Areas` as keys and Suggestion as values.""")
    

    return json.loads(response.split('```')[-2].replace('json',""))

if __name__ == "__main__":
    st.title("Sentiment analysis")
    text = st.text_area("""### Enter the Review""",None)
    b = st.button("Submit")

    if text:
        sentimen_dict = Sentiment_provider(text)
        print(sentimen_dict)
        if b:

            if sentimen_dict['Sentiment'] != "Positive":

                st.markdown(f'''Sentiment of the Provided text is:
                                    **:red[{sentimen_dict['Sentiment']}]**''')
                

            if sentimen_dict['Sentiment'] == "Positive":
                st.markdown(f'''Sentiment of the Provided text is: 
                                    **:green[{sentimen_dict['Sentiment']}]**''')
            suggestion = Suggestion_provider(sentimen_dict, text)
            st.write(suggestion)
