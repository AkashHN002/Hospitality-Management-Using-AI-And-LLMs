import random
import pandas as pd

data = pd.read_csv(r"Notebook\Sentiment_data.csv")

activities = {
        'amenities': ['pool', 'spa', 'gym', 'tennis_court', 'business_center'],
        'dining': ['main_restaurant', 'cafe', 'bar', 'room_service', 'buffet'],
        'activities': ['city_tour', 'beach_activity', 'cooking_class', 'yoga', 'golf']
}

def getUserData(data):
    user_data = []
    for id in data.User_Id:
        for i in range(random.randint(10,20)):
            category = random.choice(list(activities.keys()))
            activity = random.choice(activities[category])
            rating = random.randint(1, 5)
            time_spent = random.randint(30, 180)
            user_data.append({
                "User_ID":id,
                "Category":category,
                "Activity":activity,
                "Rating":rating,
                "Time_Spent":time_spent
            })
            
    return pd.DataFrame(user_data)

user = getUserData(data)
user.to_csv(r"Notebook/Interaction.csv")
print("Recommendation data saved Successfully")