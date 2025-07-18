import streamlit as st
import pandas as pd

# Replace with your Google Sheet export link
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/edit?usp=sharing&ouid=115455914725839001108&rtpof=true&sd=true"

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

data = load_data()

# Title
st.title("¡Revisa si tu voto fue registrado!")

# Input field for ID number
user_id = st.text_input("Ingresa tu RUT:")

# Check the status
if user_id:
    result = data[data["RUN"].astype(str) == user_id]
    if not result.empty:
        status = result.iloc[0]["Status"]
        st.success(f"Status: {status}")
    else:
        st.error("Su RUT no fue encontrado en nuestros registros.")
