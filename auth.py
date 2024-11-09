import streamlit as st
import pandas as pd
import hashlib

# Function to hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user data from CSV
def load_users():
    try:
        users = pd.read_csv("users.csv")
    except FileNotFoundError:
        # If file doesn't exist, create an empty DataFrame
        users = pd.DataFrame(columns=["username", "password"])
    return users

# Save user data to CSV
def save_user(username, password):
    users = load_users()
    new_user = pd.DataFrame({"username": [username], "password": [hash_password(password)]})
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv("users.csv", index=False)

# Authenticate user
def authenticate(username, password):
    users = load_users()
    if username in users["username"].values:
        stored_password = users.loc[users["username"] == username, "password"].values[0]
        return stored_password == hash_password(password)
    return False

# Display Login or Sign-up Form based on user choice
def login_or_signup():
    # Set up session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    # Display login or signup form based on user choice
    if st.session_state.logged_in:
        st.sidebar.write(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.sidebar.write("You have logged out.")
            st.rerun()

    else:
        option = st.sidebar.selectbox("Login or Sign up", ["Login", "Sign up"])

        if option == "Login":
            st.sidebar.write("## Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                if authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.sidebar.success("Login successful!")
                else:
                    st.sidebar.error("Incorrect username or password.")
                st.rerun()

        elif option == "Sign up":
            st.sidebar.write("## Sign up")
            new_username = st.sidebar.text_input("Create a Username")
            new_password = st.sidebar.text_input("Create a Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            if st.sidebar.button("Sign up"):
                if new_password == confirm_password:
                    save_user(new_username, new_password)
                    st.sidebar.success("Account created successfully! You can now log in.")
                else:
                    st.sidebar.error("Passwords do not match.")
                st.rerun()
