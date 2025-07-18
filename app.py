import streamlit as st
import pandas as pd

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Voting Status Checker", layout="centered")

# ---- HEADER: LOGO + ORG NAME ----
col1, col2 = st.columns([1, 4])  # Adjust width ratio if needed

with col1:
    st.image("logo.png", width=100)  # Make sure logo.png is in the same folder

with col2:
    st.markdown(
        "<h1 style='margin-top: 20px; font-size: 32px;'>Sindicato Interempresa Salud UC</h1>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ---- CUSTOM TITLES ----
st.markdown(
    """
    <h2 style='text-align: center; font-size: 36px;'>Oferta del Empleador - 20 de julio</h2>
    <p style='text-align: center; font-size: 20px;'>¡Revisa si tu voto fue registrado!</p>
    """,
    unsafe_allow_html=True
)

# ---- LOAD VOTING DATA FROM GOOGLE SHEETS ----
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

data = load_data()

# ---- USER INPUT ----
user_id = st.text_input("Ingresa tu RUT:")

# ---- CHECK VOTING STATUS ----
if user_id:
    result = data[data["RUT"].astype(str) == user_id]
    if not result.empty:
        status = result.iloc[0]["Status"]
        st.success(f"Estado: {status}")
    else:
        st.error("Su RUT no fue encontrado en nuestros registros.")
