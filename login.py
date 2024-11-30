import streamlit as st
import base64

# Function to encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use the encoded image as a string
background_image = get_base64_image("background.jpg")  # Replace "background.jpg" with your actual image file name
icon_image = get_base64_image("login.jpeg")  # Path to the heart icon image

# Function to apply background image directly from base64
def apply_background(encoded_image):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;  /* Ensures full-screen background */
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        label, h1 {{
            color: black;  /* Set label and heading color to black */
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use session_state to store users persistently within a session
if "users" not in st.session_state:
    st.session_state["users"] = {}

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

# Login functionality with icon on the left and form on the right
def login():
    st.markdown("<h1 style='font-weight: bold; color: White;'>Login</h1>", unsafe_allow_html=True)

    # Layout for the icon and form side by side
    col1, col2 = st.columns([1, 2])  # Adjust column ratios as needed

    # Left column with icon
    with col1:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{icon_image}" width="150" height="150">
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Right column with login form
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

# Main application interface after login
def dashboard():
    st.markdown("<h1 style='font-weight: bold; color: white;'>Heart Attack Risk Prediction Dashboard</h1>", unsafe_allow_html=True)

# Initialize logged-in state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Apply background image
apply_background(background_image)

# Display either dashboard or login/signup page based on login state
if st.session_state["logged_in"]:
    dashboard()
    if st.button("Logout"):
        logout()
else:
    page = st.radio("Choose a page:", ("Login", "Sign Up"))
    if page == "Sign Up":
        signup()
    else:
        login()
