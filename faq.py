import streamlit as st
import pandas as pd
import base64
from difflib import get_close_matches
from time import sleep

# Function to encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to apply background image
def apply_background(encoded_image):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        label, h1 {{
            color: black;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load images
login_background_image = get_base64_image("background.jpg")
login_icon_image = get_base64_image("login.jpeg")
predict_background_image = get_base64_image("predictbackground.jpg")
medicines_background_image = get_base64_image("Medicinesbackground.jpg")
faq_background_image = get_base64_image("faqbackground.jpg")

# User session management
if "users" not in st.session_state:
    st.session_state["users"] = {}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None

# Signup functionality
def signup():
    st.markdown("<h1 style='font-weight: bold; color: White;'>Sign Up</h1>", unsafe_allow_html=True)
    username = st.text_input("Choose a Username", label_visibility="visible")
    password = st.text_input("Choose a Password", type="password", label_visibility="visible")
    confirm_password = st.text_input("Confirm Password", type="password", label_visibility="visible")

    if st.button("Sign Up"):
        if username in st.session_state["users"]:
            st.error("Username already exists. Please choose a different one.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            st.session_state["users"][username] = password
            st.success("Signup successful! You can now log in.")
            st.info("Go to the login page to continue.")

# Login functionality
def login():
    st.markdown("<h1 style='font-weight: bold; color: White;'>Login</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{login_icon_image}" width="150" height="150">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        username = st.text_input("Username", label_visibility="visible")
        password = st.text_input("Password", type="password", label_visibility="visible")

        if st.button("Login"):
            if username in st.session_state["users"] and st.session_state["users"][username] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Invalid username or password. Please try again.")

# Logout functionality
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

# Heart Attack Prediction Dashboard
def predict_dashboard():
    apply_background(predict_background_image)
    st.title("Heart Attack Risk Prediction")
    st.write("Enter the Patient ID, Age, Cholesterol, BMI, and Triglycerides to predict heart attack risk.")
    
    data = pd.read_csv('dataset.csv')

    patient_id = st.text_input("Enter Patient ID:")
    age = st.number_input("Enter Age:", min_value=0, max_value=120, step=1)
    cholesterol = st.number_input("Enter Cholesterol Level:", min_value=0)
    bmi = st.number_input("Enter BMI:", min_value=0.0)
    triglycerides = st.number_input("Enter Triglycerides Level:", min_value=0)

    if patient_id and age:
        patient_data = data[(data['Patient ID'] == patient_id) & (data['Age'] == age)]
        if not patient_data.empty:
            st.write("Patient Details:")
            st.write(patient_data)
        else:
            st.write("No patient found with the provided ID and Age.")

    if st.button("Predict Heart Attack Risk"):
        risk = "Low"
        if age > 50 or cholesterol > 240 or bmi > 30 or triglycerides > 200:
            risk = "High"
        st.write(f"Heart Attack Risk Prediction: {risk}")

# Medicines Chatbot Dashboard
def medicines_dashboard():
    apply_background(medicines_background_image)
    data = pd.read_csv("Medicines.csv")

    if 'Disease' in data.columns and 'Medicine' in data.columns:
        st.title("Medicine Chatbot 💊")
        disease_list = data['Disease'].unique()
        user_input = st.text_input("Ask a question about a disease:", placeholder="Type a disease name here...")

        if user_input:
            close_matches = get_close_matches(user_input, disease_list, n=1, cutoff=0.7)
            if close_matches:
                matched_disease = close_matches[0]
                matched_data = data[data['Disease'] == matched_disease]
                st.write(f"Best match: **{matched_disease}** with medicines:")
                for _, row in matched_data.iterrows():
                    st.write(f"- **{row['Disease']}**: {row['Medicine']}")
            else:
                st.write("🤖 Chatbot: No close matches found. Please try another query or check available diseases above.")
    else:
        st.write("Error: The file does not contain the required columns ('Disease' and 'Medicine').")

# FAQ Chatbot Dashboard
def faq_dashboard():
    apply_background(faq_background_image)
    try:
        faq_data = pd.read_csv('FAQ.csv', encoding='ISO-8859-1')
    except Exception as e:
        st.error(f"Error loading FAQ file: {e}")
        return

    st.title("Healthcare FAQ Bot 🩺")
    user_input = st.text_input("Ask your question:", placeholder="Ask me anything...")
    if user_input:
        with st.spinner("Thinking... 🤔"):
            sleep(1.5)
        st.write("🤖 Bot is thinking...")
        faq_response = find_faq_response(user_input, faq_data)
        sleep(1)
        st.write("🤖 Bot:", faq_response)

# Function to find FAQ responses
def find_faq_response(user_input, faq_data):
    user_input = user_input.lower()
    faq_data['Question'] = faq_data['Question'].fillna('')
    best_match = faq_data[faq_data['Question'].str.lower().str.contains(user_input)]
    if not best_match.empty:
        return best_match.iloc[0]['Answer']
    return "I'm sorry, I couldn't find an answer to that question."

# Main Application
if st.session_state["logged_in"]:
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    menu = st.sidebar.radio("Navigate", ["Heart Attack Prediction", "Medicine Chatbot", "FAQ Bot"])
    
    if menu == "Heart Attack Prediction":
        predict_dashboard()
    elif menu == "Medicine Chatbot":
        medicines_dashboard()
    elif menu == "FAQ Bot":
        faq_dashboard()

    if st.sidebar.button("Logout"):
        logout()
else:
    apply_background(login_background_image)
    page = st.radio("Choose a page:", ("Login", "Sign Up"))
    if page == "Sign Up":
        signup()
    else:
        login()
