import streamlit as st
import pandas as pd

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel("voting_status.xlsx")

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
        st.error("ID number not found.")
