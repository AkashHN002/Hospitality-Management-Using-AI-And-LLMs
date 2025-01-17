import MySQLdb
import random

db = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    database = 'mydemo'      
)

cursor = db.cursor()

activities = {
        'amenities': ['pool', 'spa', 'gym', 'tennis_court', 'business_center'],
        'dining': ['main_restaurant', 'cafe', 'bar', 'room_service', 'buffet'],
        'activities': ['city_tour', 'beach_activity', 'cooking_class', 'yoga', 'golf']
}

user_id = input("Enter user Id:- ")



while(True):
    exist = cursor.execute("SELECT * FROM interaction WHERE User_id = %s", (user_id,))
    if exist:
        print(f"1-->{list(activities.keys())[0]}\n2-->{list(activities.keys())[1]}\n3-->{list(activities.keys())[2]}\n4--> Exit\n")
        c = int(input("Choose the Category visited: "))

        if c == 4:
            break
        else:
            cat = list(activities.keys())[c-1]
            for i in range(len(activities[cat])):
                print(f"{i+1}--> {activities[cat][i]} ")
            try:
                n = int(input(f"""Choose any Preferances:  """))
                pref = activities[cat][n-1]
                rating = int(input("Privide the rating for activity (0-5): "))
                time_spent = random.randint(30, 180)

                print(f"Choosed Category {cat}\nChoosed Activity {pref}")
                cursor.execute("INSERT INTO interaction VALUES(%s, %s, %s, %s, %s)", (user_id, cat, pref, rating, time_spent))
                if cursor.rowcount:
                    db.commit()
            except:
                print("Enter the correct number")
    else:
        print("\nData Not Found\nPlease give the following details: ")
        print(f"1-->{list(activities.keys())[0]}\n2-->{list(activities.keys())[1]}\n3-->{list(activities.keys())[2]}\n4--> Exit\n")
        x = int(input("Choose the Category visited: "))
        if x!=4:
            cat = list(activities.keys())[x-1]
            for i in range(len(activities[cat])):
                print(f"{i+1}--> {activities[cat][i]}")
            x = int(input("enter the Activity: "))
            pref = activities[cat][x-1]
            rating = int(input("Privide the rating for activity (0-5): "))
            time_spent = random.randint(30, 180)
            print(f"\nChoosed Category {cat}\nChoosed Activity {pref}")
            
            cursor.execute("INSERT INTO interaction VALUES(%s, %s, %s, %s, %s)", (user_id, cat, pref, rating, time_spent))
            if cursor.rowcount:
                print("Data Added")
                db.commit()
        else:
            break
       