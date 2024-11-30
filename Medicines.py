import streamlit as st
import pandas as pd
from difflib import get_close_matches
import base64

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
            background-size: cover;  /* Ensures full-screen background */
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load the background image
background_image = get_base64_image("Medicinesbackground.jpg")  # Replace with your actual image file name
apply_background(background_image)

# Load the CSV file
data = pd.read_csv("Medicines.csv")

# Assuming the CSV has columns named 'Disease' and 'Medicine'
if 'Disease' in data.columns and 'Medicine' in data.columns:
    st.title("Medicine Chatbot 💊")
    
    # Display list of diseases for user's reference
    disease_list = data['Disease'].unique()
    
    # Input field for user question with placeholder text
    user_input = st.text_input("Ask a question about a disease:", placeholder="Type a disease name here...")

    # Search and display relevant medicine
    if user_input:
        # Use difflib to find close matches
        close_matches = get_close_matches(user_input, disease_list, n=1, cutoff=0.7)  # cutoff sets the similarity threshold
        
        if close_matches:
            matched_disease = close_matches[0]
            matched_data = data[data['Disease'] == matched_disease]
            # Display chatbot thinking icon
            #st.write("🤖 Chatbot is thinking...")
            st.write(f"Best match: **{matched_disease}** with medicines:")
            for _, row in matched_data.iterrows():
                st.write(f"- **{row['Disease']}**: {row['Medicine']}")
        else:
            st.write("🤖 Chatbot: No close matches found. Please try another query or check available diseases above.")
else:
    st.write("Error: The file does not contain the required columns ('Disease' and 'Medicine').")
