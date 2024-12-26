import pandas as pd
import random
import datetime

name_data = pd.read_csv(r"D:\Dataset\customers-100000.csv")
feedback_data =  pd.read_parquet(r"D:\Dataset\\train-00000-of-00001-0e99e58b23dccc25.parquet")


dept = ['Accounting', 'Advertising', 'Banking', 'Customer Service', 'E-commerce', 'Entertainment', 'Food', 'Gym', 'Healthcare' 'Help Desk',
 'Hospitality', 'Housekeeping', 'Laundry', 'Maintenance', 'Photography', 'Dining', 'Reception', 'Spa']

wellness_activities = [ "Spa Treatment","Massage Therapy","Yoga Sessions","Meditation Classes","Facials","Sauna","Steam Room","Body Scrubs",
    "Herbal Baths", "Fitness Classes", "Beauty Treatments", "Personal Training", "Herbal Therapy", "Skin Care Treatments",]

cust_sport = [ "Tennis", "Swimming", "Yoga", "Golf", "Runnin", "Gym Workout", "Aerobics", "Volleyball", "Badminton", "Table Tennis",
    "Basketball","Soccer","Rugby""Cycling"]

pricing_patterns = [ "Budget", "Mid-range", "Luxury", "All-inclusive", "Per-night rate", "Weekly discount", "Seasonal pricing", "Last-minute deals",
    "Member-exclusive rates", "Kids stay free", "Senior discounts", "Military discounts", "Package deals",]

data = {
    "Cust_name":name_data['First Name'].iloc[:10000],
    'Cust_email':[i.lower()+str(random.randint(1000,9000))+'@example.com' for i in name_data['First Name'].iloc[:10000]],
    'Feedback':feedback_data['text'].iloc[:10000],
    'Date':[datetime.date(random.randint(2000, 2025),random.randint(1,12), random.randint(1,28)) for _ in range(10000)],
    'Care_Taker':name_data['Last Name'].iloc[:10000],
    'Emp_id':['EMP'+str(random.randint(1000,3000)) for _ in range(10000)],
    'Age':[random.randint(20,90) for _ in range(10000)],
    'Contact':[str(random.choice([6,9,8,7]))+str(random.randint(10000000, 999999999)) for _ in range(10000)],
    'Department':[random.choice(dept) for _ in range(10000)],
    'Customer Stay Duration (hrs)':[round(random.uniform(1.0, 10.0), 1) for _ in range(10000)],
    'Customer_N_visit':[random.randint(1,10) for _ in range(10000)],
    'Cust amount to be paid':[round(random.uniform(0.0, 500.0), 2) for _ in range(10000)],
    'Nps':[random.randint(-100, 100) for _ in range(10000)],
    'Dining':[random.choice(['Vegetaion', 'Non-Vegetarion', 'Vegan']) for _ in range(10000)],
    'Room Preference':[random.choice(['Single', 'Double', 'Twin','King','Suite','Family']) for _ in range(10000)],
    'Sport Activities':[random.choice(cust_sport) for _ in range(10000)],
    'Wellness':[random.choice(wellness_activities) for _ in range(10000)],
    'Pricing':[random.choice(pricing_patterns) for _ in range(10000)]
}
df = pd.DataFrame(data)
df.to_csv('Sentiment_data.csv', index = False)
print('Data Saved Successfully')



