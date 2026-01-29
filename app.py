import streamlit as st
import psycopg2
import hashlib
from datetime import datetime
import pandas as pd

# Initialize session 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Database Connection 
def get_db_connection():
    return psycopg2.connect(database="PROJECT-1", user="postgres", password="suga7", host="localhost")


#LOGGED IN or NOT LOGGED IN


#NOT LOGGED IN: Show Welcome Screen and Login Sidebar
if not st.session_state['logged_in']:
    st.title("Welcome to Client Query Management System")
    

    st.sidebar.title("Login")
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type='password')
    role_input = st.sidebar.selectbox("Role", ["Client", "Support"])

    if st.sidebar.button("Enter"):
        # Hash input password to compare with database
        h_pass = hashlib.sha256(password_input.encode()).hexdigest()
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Verify against 'users' table using the correct column 'hashed_password'
            cur.execute("SELECT username FROM users WHERE username=%s AND hashed_password=%s AND role=%s", 
                        (username_input, h_pass, role_input))
            result = cur.fetchone()
            conn.close()

            if result:
                st.session_state['logged_in'] = True
                st.session_state['role'] = role_input
                st.session_state['username'] = username_input
                st.rerun()
            else:
                st.sidebar.error("Invalid Username, Password, or Role.")
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")

# LOGGED IN: Show the Dashboard and Logout button
else:
    # Sidebar Logout Button
    st.sidebar.title(f"{st.session_state['username']}")
    st.sidebar.write(f"Role: {st.session_state['role']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['username'] = None
        st.rerun()

    # client page 
    if st.session_state['role'] == "Client":
        st.header("Submit Your Query")
        email = st.text_input("Email ID")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        desc = st.text_area("Query Description")
        
        if st.button("Submit"):
            if email and heading:
                conn = get_db_connection()
                cur = conn.cursor()
                # Insert using the schema from MINI_PROJECT.sql
                cur.execute("INSERT INTO queries (client_email, client_mobile, query_heading, query_description, status) VALUES (%s, %s, %s, %s, %s)",
                            (email, mobile, heading, desc, 'Open'))
                conn.commit()
                conn.close()
                st.success("Query submitted successfully!")
            else:
                st.warning("Please fill in at least the Email and Heading.")
    # support page
    elif st.session_state['role'] == "Support":
        st.header("Support Dashboard")
        conn = get_db_connection()
        # Fetch only Open queries to manage efficiently
        df = pd.read_sql("SELECT * FROM queries WHERE status='Open'", conn)
        st.subheader("Open Tickets")
        st.dataframe(df, use_container_width=True) # Dataframe is often cleaner than st.table
        
        st.divider()
        st.subheader("Resolve a Ticket")
        target_id = st.number_input("Enter Query ID to Close", step=1, min_value=1)
        if st.button("Mark as Resolved"):
            cur = conn.cursor()
            # Update using column names from MINI_PROJECT.sql
            cur.execute("UPDATE queries SET status='Closed', date_closed=%s WHERE query_id=%s", 
                        (datetime.now(), target_id))
            conn.commit()
            conn.close()
            st.success(f"Query {target_id} marked as Closed.")
            st.rerun()