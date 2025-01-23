import streamlit as st

s1 = st.button("First")

# Initialize s2 and s3 to None
s2 = None
s3 = None

if s1:
    s2 = st.button("Second", key= 1)
    s3 = st.button("Third", key = 2)
    if s2:
        s4 = st.button("Four", key=4)

