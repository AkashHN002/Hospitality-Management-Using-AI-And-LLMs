import streamlit as st
import random 
from src.Profile import DataBaseManager

activities = {
        'amenities': ['pool', 'spa', 'gym', 'tennis_court', 'business_center'],
        'dining': ['main_restaurant', 'cafe', 'bar', 'room_service', 'buffet'],
        'activities': ['city_tour', 'beach_activity', 'cooking_class', 'yoga', 'golf']
}

values = list([ i.replace("_"," ").title() for i  in [j for i in activities.values() for j in i]])

database = DataBaseManager()

container = st.container()
with container.expander("Select"):
    st.write("Welcome to the Profile Management System")
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
                user_id="1001", 
                category=choosed[0], 
                preference=selection, 
                rating=rating, 
                time_spent=time_spent
                ):
                st.success("Interaction recorded successfully!")
            else:
                st.error("Failed to record interaction. Please try again.")


                