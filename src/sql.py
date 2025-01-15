import streamlit as st
import MySQLdb

db = MySQLdb.connect(
    host = 'localhost',
    id = 'root',
    database = 'mydemo'      # Name of the database
)

cursor = db.cursor()


st.title("Sentiment analysis")
id = st.text_input("""### Enter the ID""",None)
name = st.text_input("""### Enter Name""",None)
pref = st.text_input("""### Enter the Preferance""",None)

b = st.button("Submit")
if id and name and pref:
    if b:
        is_exists = cursor.execute("SELECT * FROM student2 WHERE std_id = %s", (id,))
        cursor.execute("select Preferance from student2 where std_id = %s",(id,))
        st = cursor.fetchone()[0]
        pref_ls = st.split(", ")
        if is_exists:

            cursor.execute("select Preferance from student2 where std_id = %s",(id,))
            current_prefs = cursor.fetchone()[0]
            st = current_prefs + ', ' + pref
            cursor.execute("UPDATE student2 SET Preferance = %s WHERE std_id = %s", (st, id))
            db.commit()
        else :
            cursor.execute("Insert into student2 values(%s, %s, %s)", (id, name, pref))
            db.commit()

