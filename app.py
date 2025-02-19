import streamlit as st
import yaml
import pandas as pd
import hashlib
from yaml.loader import SafeLoader
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists("user.yaml"):
        with open("user.yaml", "r") as file:
            users = yaml.load(file, Loader=SafeLoader)
        return users['users']
    return []

def save_new_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return False
    hashed_password = hash_password(password)
    users.append({'username': username, 'password': hashed_password})
    with open("user.yaml", "w") as file:
        yaml.dump({'users': users}, file)
    return True

def check_credentials(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == hash_password(password):
            return True
    return False

def store_data_in_excel(data):
    file_path = "user_data.xlsx"
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Email", "Message"])

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(file_path, index=False)

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        page = st.sidebar.selectbox("Select a page", ["Login", "Sign Up"])

        if page == "Login":
            st.subheader("Login")
            username = st.text_input("Username", autocomplete="off")
            password = st.text_input("Password", type="password", autocomplete="off")

            if st.button("Login"):
                if check_credentials(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        elif page == "Sign Up":
            st.subheader("Sign Up")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Sign Up"):
                if new_password == confirm_password:
                    if save_new_user(new_username, new_password):
                        st.success("Account created successfully! You can now log in.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.error("Passwords do not match.")
    else:
        st.subheader(f"Welcome {st.session_state.username}!")
        st.title("Submit Your Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        message = st.text_area("Message")

        if st.button("Submit"):
            data = {"Name": name, "Email": email, "Message": message}
            store_data_in_excel(data)
            st.success("Data submitted successfully!")

if __name__ == "__main__":
    main()
