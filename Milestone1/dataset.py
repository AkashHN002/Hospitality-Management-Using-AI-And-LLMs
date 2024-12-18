import pandas as pd

name_data = pd.read_csv(r"D:\Dataset\customers-100000.csv")
import random
import datetime

# Define lists of feedback phrases for each sentiment
feedback_LS = [
    "Great service, friendly staff!",
    "Food was delicious!",
    "Excellent atmosphere!",
    "Highly recommend!",
    "Best service ever!",
    "Very impressed!",
    "Exceeded expectations!",
    "Will definitely be back!",
    "Amazing experience!",
    "Loved the food!",
    "Great value for money!",
    "Staff was very attentive!",
    "Clean and comfortable environment!",
    "Enjoyed the music!",
    "Perfect for a special occasion!",
    "Food was fresh and tasty!",
    "Quick and efficient service!",
    "Excellent value for the price!",
    "Very relaxing atmosphere!",
    "Staff was very helpful!",
    "Food was beautifully presented!",
    "Loved the ambiance!",
    "Great for a casual meal!",
    "Service was impeccable!",
    "Food was cooked to perfection!",
    "Highly recommend this place!",
    "Very friendly and welcoming staff!",
    "Excellent customer service!",
    "One of the best meals I've had!",
    "Great for a night out!",
    "Long wait time.",
    "Food was cold.",
    "Poor service.",
    "Disappointed with the experience.",
    "Rude staff.",
    "Overpriced for the quality.",
    "Uncomfortable atmosphere.",
    "Food was not tasty.",
    "Slow service.",
    "Not worth the money.",
    "Unfriendly staff.",
    "Disappointing experience.",
    "Food was not fresh.",
    "Poor value for the price.",
    "Uncomfortable seating.",
    "Loud and noisy environment.",
    "Food was not cooked properly.",
    "Disappointed with the food.",
    "Poor customer service.",
    "Would not recommend.",
    "Food was okay.",
    "Service was average.",
    "Nothing special.",
    "Mixed experience.",
    "Could be better.",
    "Not bad, not great.",
    "Met expectations.",
    "Decent experience.",
    "Average food.",
    "Service was okay.",
    "Nothing special to report.",
    "Mixed feelings about the experience.",
    "Could use some improvement.",
    "Not bad, but not memorable.",
    "Met my expectations."
]
dept = ['Accounting',
 'Advertising',
 'Banking',
 'Customer Service',
 'E-commerce',
 'Entertainment',
 'Food'
 'Gym',
 'Healthcare',
 'Help Desk',
 'Hospitality',
 'Housekeeping',
 'Laundry',
 'Maintenance',
 'Photography',
 'Dining',
 'Reception',
 'Spa']
date_ls = []
emp_id = []
age_ls =[]
contact_ls = []
sentiment_ls = []
department_ls = []
customer_stay_duration=[]
customer_visit= []
customer_amt_to_be_paid= []
NPS = []

cust_name = name_data['First Name']
cust_email = name_data['Email']
feedback = [random.choice(feedback_LS) for _ in range(100000)]
date_ls = [datetime.date(random.randint(2000, 2025),random.randint(1,12), random.randint(1,28)) for _ in range(100000)]
care_taker = name_data['Last Name']
emp_id = ['EMP'+str(random.randint(1000,3000)) for _ in range(100000)]

age_ls= [random.randint(20,90) for _ in range(100000)]
contact_ls = [str(random.choice([6,9,8,7]))+str(random.randint(10000000, 999999999)) for _ in range(100000)]

sentiment = [random.choice(['Positive', 'Neutral', 'Negative']) for _ in range(100000)]
department_ls = [random.choice(dept) for _ in range(100000)]
customer_stay_duration = [round(random.uniform(1.0, 10.0), 1) for _ in range(100000)]
customer_visit = [random.randint(1,10) for _ in range(100000)]
customer_amt_to_be_paid = [round(random.uniform(0.0, 500.0), 2) for _ in range(100000)]
NPS = [random.randint(-100, 100) for _ in range(100000)]

df = pd.DataFrame({
    "Cust_name":cust_name,
    'Cust_email':cust_email,
    'Feedback':feedback,
    'Date':date_ls,
    'Care_Taker':care_taker,
    'Emp_id':emp_id,
    'Age':age_ls,
    'Contact':contact_ls,
    'Sentiment':sentiment,
    'Department':department_ls,
    'Customer Stay Duration':customer_stay_duration,
    'Customer_N_visit':customer_visit,
    'Cust amount to be paid':customer_amt_to_be_paid,
    'Nps':NPS
})
df.to_csv('Sentiment_data.csv')