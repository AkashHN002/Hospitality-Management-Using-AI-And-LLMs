import streamlit as st
import requests
import json
api = "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"
def Sentiment_provider(text):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api}",
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
            ]
            
        })
        )

    return json.loads(response.json()['choices'][0]['message']['content'])


def Suggestion_provider(Sentiment_dict:dict, text):
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api}"
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
            
        })
    )
    return json.loads(response.json()['choices'][0]['message']['content'])


st.title("Sentiment analysis")
text = st.text_input("""### Enter the Review""",None)
b = st.button("Submit")

if text:
    sentimen_dict = Sentiment_provider(text)
    if b:

        if sentimen_dict['Sentiment'] != "Positive":

            st.markdown(f'''Sentiment of the Provided text is:
                                **:red[{sentimen_dict['Sentiment']}]**''')
            

        if sentimen_dict['Sentiment'] == "Positive":
            st.markdown(f'''Sentiment of the Provided text is: 
                                **:green[{sentimen_dict['Sentiment']}]**''')
        suggestion = Suggestion_provider(sentimen_dict, text)
        st.write(suggestion)
