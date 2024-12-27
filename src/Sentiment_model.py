import streamlit as st
import os
import json
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def Sentiment_provider(text):
    chat_completion = client.chat.completions.create(
        messages=[
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
        model="llama3-8b-8192",
        response_format={"type": "json_object"}
    )

    return json.loads((chat_completion.choices[0].message.content))


def Suggestion_provider(Sentiment_dict:dict, text):
    chat_completion = client.chat.completions.create(
    messages=[
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
    model="llama3-8b-8192",
    response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)


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
