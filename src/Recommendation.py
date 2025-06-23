import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
class Recommendation:
    def __init__(self):
        self.data = pd.read_csv(r"Notebook\Interaction.csv")

        self.rating_matrix = self.data.pivot_table(index='User_ID', columns="Activity", values="Rating").fillna(0)
        self.time_matrix = self.data.pivot_table(index='User_ID', columns="Activity", values="Time_Spent").fillna(0)
        self.matrix = ( self.rating_matrix * 0.7) + (self.time_matrix * 0.3)

    def getSimilarUser(self, user_id, k = 3):

        matrix = self.matrix
        
        user_data = matrix[matrix.index == user_id]
        other_user = matrix[matrix.index != user_id]


        if user_data.shape[0]<1 or other_user.shape[0]<1:
            return []
        
        similar_matrix = cosine_similarity(user_data, other_user)[0].tolist()


        user_indices = dict(zip(other_user.index, similar_matrix))
        similar_user = sorted(user_indices.items(), key = lambda x: x[1], reverse = True)

        top_similar_user = similar_user[:k]
        users = [u[0] for u in top_similar_user]
        return users


    def getRecommendations(self, user_id, k = 3):
        matrix = self.matrix

        similar_user_indices = self.getSimilarUser(user_id)
        if len(similar_user_indices) < 1:
            return []
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

if __name__ == "__main__":
    st.title("Recommendation ")
    user_id = st.text_input("""### Enter the User Id""",None)
    b = st.button("Submit")

    s = False

    obj = Recommendation()

    if user_id:
        
        if b:
            recommendations = obj.getRecommendations(user_id)
            st.write(f"Recommondations for {user_id}: ")
            container = st.container()
            if len(recommendations) > 0:
                for i, area in enumerate(recommendations):
                    with container.expander(f"Recommondation {i+1}", expanded=True):
                        st.write(area.replace('_', ' ').title())
            else:
                with container.expander(f"", expanded=True):
                    st.write("No Recommendations Found")