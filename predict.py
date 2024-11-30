import streamlit as st
import pandas as pd
import base64

# Function to encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load background image
background_image = get_base64_image("predictbackground.jpg")  # Replace with your actual image file name

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

# Apply the background image
apply_background(background_image)

# Load data
data = pd.read_csv('dataset.csv')

# Title and description
st.title('Heart Attack Risk Prediction')
st.write("Enter the Patient ID, Age, Cholesterol, BMI, and Triglycerides to predict heart attack risk.")

# Input fields for Patient ID, Age, Cholesterol, BMI, and Triglycerides
patient_id = st.text_input("Enter Patient ID:")
age = st.number_input("Enter Age:", min_value=0, max_value=120, step=1)
cholesterol = st.number_input("Enter Cholesterol Level:", min_value=0)
bmi = st.number_input("Enter BMI:", min_value=0.0)
triglycerides = st.number_input("Enter Triglycerides Level:", min_value=0)

# Check for existing patient details
if patient_id and age:
    patient_data = data[(data['Patient ID'] == patient_id) & (data['Age'] == age)]
    
    if not patient_data.empty:
        st.write("Patient Details:")
        st.write(patient_data)
    else:
        st.write("No patient found with the provided ID and Age.")

# Predict heart attack risk based on input values
if st.button("Predict Heart Attack Risk"):
    # Basic prediction logic (adjust thresholds as needed)
    risk = "Low"
    
    if age > 50 or cholesterol > 240 or bmi > 30 or triglycerides > 200:
        risk = "High"
    
    st.write(f"Heart Attack Risk Prediction: {risk}")

# Display a message if all inputs are not provided
if not (patient_id and age):
    st.write("Please enter both Patient ID and Age to view the details.")
