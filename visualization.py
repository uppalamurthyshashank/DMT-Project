import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import warnings

# Suppress warnings for future compatibility issues with Pandas
warnings.filterwarnings("ignore", message="When grouping with a length-1 list-like")

# Function to encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load background image
background_image = get_base64_image("visualizationbackground.jpg")  # Replace with your actual image file name

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
        </style>
        """,
        unsafe_allow_html=True
    )

# Set Streamlit page configuration
st.set_page_config(page_title="Health Data Visualizations", layout="wide")

# Apply the background image
apply_background(background_image)

# Load the dataset
data = pd.read_csv('dataset.csv')

# Process Blood Pressure into an average numeric column
data['Blood Pressure Avg'] = data['Blood Pressure'].str.split('/').apply(lambda x: (int(x[0]) + int(x[1])) / 2)

# Title of the app
st.title("Health Data Visualizations")

# 1. Line Plot for Heart Rate and Diabetes
st.subheader("Line Plot For Heart Rate vs Diabetes Status")
fig = px.line(data, y='Heart Rate', color='Diabetes', title='Heart Rate by Diabetes Status')
st.plotly_chart(fig)

# 2. Scatterplot for Cholesterol and Blood Pressure
st.subheader("Scatter Plot For Cholesterol vs Blood Pressure")
fig = px.scatter(data, x='Cholesterol', y='Blood Pressure Avg', title='Cholesterol vs. Blood Pressure')
st.plotly_chart(fig)

# 3. Bar Plot for Diet and BMI
st.subheader("Bar Plot For Diet vs BMI")
fig = px.bar(data, x='Diet', y='BMI', title='Diet vs. BMI')
st.plotly_chart(fig)

# 4. Heatmap for Correlation between Lifestyle Factors
st.subheader("Heat Map For Correlation between Lifestyle Factors")
fig, ax = plt.subplots()
sns.heatmap(data[['Obesity', 'Smoking', 'Heart Attack Risk']].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# 5. Pie Chart for Triglycerides, Stress Level, and Cholesterol
st.subheader("Pie Chart for Distribution of Triglycerides, Stress Level, and Cholesterol")
df_pie = data[['Triglycerides', 'Stress Level', 'Cholesterol']].mean().reset_index()
df_pie.columns = ['Category', 'Average']
fig = px.pie(df_pie, values='Average', names='Category', title='Distribution of Triglycerides, Stress Level, and Cholesterol')
st.plotly_chart(fig)