import streamlit as st
import pandas as pd


# ---- HEADER ----
# Page config
st.set_page_config(page_title="Voting Status Checker", layout="centered")

# --- HEADER with logo and organization name ---
col1, col2 = st.columns([1, 4])  # Adjust width ratio as needed

with col1:
    st.image("logo.png", width=100)  # Use your local logo image

with col2:
    st.markdown(
        "<h1 style='margin-top: 20px; font-size: 32px;'>Sindicato Interempresa Salud UC</h1>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ---- DATA LOADING ----

# Replace with your Google Sheet export link
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/export?format=csv"

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
    result = data[data["RUT"].astype(str) == user_id]
    if not result.empty:
        status = result.iloc[0]["Status"]
        st.success(f"Status: {status}")
    else:
        st.error("Su RUT no fue encontrado en nuestros registros.")
