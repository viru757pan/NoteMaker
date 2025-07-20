import streamlit as st
import requests
import time
import pandas as pd
import numpy as np
from utils.signup_validation import is_valid_email, is_strong_password, get_user_id

# ----- Config -----
st.set_page_config(page_title="NotesMaker", layout="centered")

# Initialize view state
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

def go_to(page, user_id=None):
    st.session_state.page = page
    if user_id is not None:
        st.session_state.user_id = user_id
    st.rerun()

# Sign Up View
def signup_view():
    st.title("👤 Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        # Empty field check
        if not username or not email or not password:
            st.error("All fields are required!")
        elif not is_valid_email(email.strip()):
            st.error("Invalid email format.")
        elif not is_strong_password(password):
            st.error("Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.")
        else:
            response = requests.post("http://127.0.0.1:5000/user/SignUp", json={
                "username": username.strip(),
                "email": email.strip(),
                "password": password
            })

            if response.status_code == 200:
                st.success("User creation successful! Redirecting to login...")
                time.sleep(1)  # ⏳ wait for 0.6 seconds
                go_to("login")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
    
    if st.button("Already have an account? Login"):
        go_to("login")


# Login View
def login_view():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not email or not password:
            st.error("All fields are required!")
        else:
            response = requests.post("http://127.0.0.1:5000/user/Login", json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                st.success("Login successful!")
                user_data = response.json()
                # print('User data: ', user_data)
                user_id = user_data.get("user_id")

                st.session_state.jwt_token = response.json().get("token")
                st.session_state.is_logged_in = True
                st.session_state.user_id = user_id
                time.sleep(1)
                go_to("fetch_note", user_id)
            else:
                st.error("Login failed.")
    
    if st.button("Don't have an account? Sign Up"):
        go_to("signup")


# Create Notes View
def create_notes_view():
    if not st.session_state.is_logged_in:
        st.warning("You must log in to access this page.")
        if st.button("Go to Login"):
            go_to("login")
        return
    
    headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}

    st.title("📝 Create Note")

    if st.button("View Notes"):
        go_to("fetch_note", st.session_state.user_id)

    title = st.text_input("Title")
    description = st.text_input("Description")
    if st.button("Create Note"):
        response = requests.post(f"http://127.0.0.1:5000/user/notes/", json={
            "user_id": st.session_state.user_id,
            "title": title,
            "description": description
        }, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            st.success("Note created!")
            go_to("fetch_note", st.session_state.user_id)
        else:
            st.error("Note creation failed.")

def fetch_notes_view():
    if not st.session_state.is_logged_in:
        st.warning("You must log in to access this page.")
        if st.button("Go to Login"):
            go_to("login")
        return

    headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}
    
    st.title("📒 Your Notes")

    if st.button("Logout"):
        print("logout id: ", st.session_state.user_id)
        st.session_state.is_logged_in = False
        st.session_state.user_id = None
        go_to("login")
    if st.button("Create Note"):
        go_to("create_note", st.session_state.user_id)

    # print('id: ', st.session_state.user_id)

    response = requests.get(f"http://127.0.0.1:5000/user/notes/", headers=headers)

    if response.status_code == 200:
        raw_notes = response.json()

        if not raw_notes:
            st.info("No notes found.")
            return

        df = pd.DataFrame(raw_notes, columns=["note_id", "user_id", "title", "description"])

        # st.subheader(f"Found {len(df)} note(s)")
        # st.dataframe(df[["title", "description"]])

        # Headers
        col1, col2, col3, col4 = st.columns([3, 5, 2, 2], vertical_alignment="center", border=True)
        col1.markdown("**Title**")
        col2.markdown("**Description**")
        col3.markdown("**Edit**")
        col4.markdown("**Delete**")

        # Render rows with buttons
        for idx, row in df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 5, 2, 2], vertical_alignment="center")
            col1.markdown(row["title"])
            col2.markdown(row["description"])

            # Edit button
            if col3.button("✏️", key=f"edit_{row['note_id']}"):
                st.session_state.editing_note = row
                st.session_state.page = "edit_note"
                st.rerun()

            # Delete button
            if col4.button("🗑️", key=f"delete_{row['note_id']}"):
                delete_response = requests.delete(f"http://127.0.0.1:5000/user/notes/{row['note_id']}", headers=headers)
                if delete_response.status_code == 201:
                    st.success("Note deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete note.")

    else:
        st.error(f"Error fetching notes. Status: {response.status_code}, Detail: {response.text}")
        print("Error fetching notes:", response.status_code, response.text)

def edit_note_view():
    if not st.session_state.is_logged_in:
        st.warning("You must log in to access this page.")
        if st.button("Go to Login"):
            go_to("login")
        return
    
    headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}
    
    note = st.session_state.get("editing_note")
    if note is None or note.empty:
        st.error("No note selected for editing.")
        return

    st.title("✏️ Edit Note")
    title = st.text_input("Title", value=note["title"])
    description = st.text_input("Description", value=note["description"])

    if st.button("Update Note"):
        response = requests.put(f"http://127.0.0.1:5000/user/notes/{note['note_id']}", json={
            "title": title,
            "description": description
        }, headers=headers)
        if response.status_code == 201:
            st.success("Note updated successfully!")
            st.session_state.page = "fetch_note"
            st.rerun()
        else:
            st.error("Failed to update note.")


# 🚦 Page Routing
if st.session_state.page == "signup":
    signup_view()
elif st.session_state.page == "login":
    login_view()
elif st.session_state.page == "create_note":
    create_notes_view()
elif st.session_state.page == "fetch_note":
    fetch_notes_view()
elif st.session_state.page == "edit_note":
    edit_note_view()