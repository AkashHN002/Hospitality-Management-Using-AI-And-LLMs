import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv(r"Notebook\Interaction.csv")

rating_matrix = data.pivot_table(index='User_ID', columns="Activity", values="Rating").fillna(0)
time_matrix = data.pivot_table(index='User_ID', columns="Activity", values="Time_Spent").fillna(0)
matrix = ( rating_matrix * 0.7) + (time_matrix * 0.3)

def getSimilarUser(user_id, matrix, k = 3):
    # Getting data of user
    user_data = matrix[matrix.index == user_id]

    # Getting data of other users
    other_user = matrix[matrix.index != user_id]

    # Calculating the similarity between one user and every other user
    similar_matrix = cosine_similarity(user_data, other_user)[0].tolist()


    user_indices = dict(zip(other_user.index, similar_matrix))
    similar_user = sorted(user_indices.items(), key = lambda x: x[1], reverse = True)

    # Selecting top K users
    top_similar_user = similar_user[:k]
    users = [u[0] for u in top_similar_user]
    return users


def getRecommendations(user_id, matrix, similar_user_indices, k = 3):
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


st.title("Sentiment analysis")
user_id = st.text_input("""### Enter the User Id""",None)
b = st.button("Submit")
s = False
if user_id:
    similar_users = getSimilarUser(user_id, matrix)
    
    if b:
       recommendations = getRecommendations(user_id, matrix, similar_users)
       for area in recommendations:
           st.write(area)