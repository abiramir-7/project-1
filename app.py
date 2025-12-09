import streamlit as st
import psycopg2
import hashlib
import datetime
import pandas as pd

# Database Connection Helper
def get_db_connection():
    return psycopg2.connect(database="PROJECT-1", user="postgres", password="suga7", host="localhost")

# 1. Login Logic
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')
role = st.sidebar.selectbox("Role", ["Client", "Support"])

if st.sidebar.button("Enter"):
    # Hash password for comparison
    h_pass = hashlib.sha256(password.encode()).hexdigest()
    # Logic to verify against 'users' table goes here...
    st.session_state['logged_in'] = True
    st.session_state['role'] = role

# 2. Page Routing
if st.session_state.get('logged_in'):
    if st.session_state['role'] == "Client":
        st.header("Submit Your Query")
        email = st.text_input("Email ID")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        desc = st.text_area("Query Description")
        
        if st.button("Submit"):
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO queries (client_email, client_mobile, query_heading, query_description, status) VALUES (%s, %s, %s, %s, %s)",
                        (email, mobile, heading, desc, 'Open'))
            conn.commit()
            st.success("Query submitted")

    elif st.session_state['role'] == "Support":
        st.header("Support Dashboard")
        conn = get_db_connection()
        # Fetch only Open queries to manage efficiently
        df = pd.read_sql("SELECT * FROM queries WHERE status='Open'", conn)
        st.table(df)
        
        target_id = st.number_input("Enter Query ID to Close", step=1)
        if st.button("Resolve Query"):
            cur = conn.cursor()
            cur.execute("UPDATE queries SET status='Closed', date_closed=%s WHERE query_id=%s", (datetime.now(), target_id))
            conn.commit()
            st.rerun()