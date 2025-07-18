import streamlit as st
import pandas as pd

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Voting Status Checker", layout="centered")

# ---- HEADER: LOGO + ORG NAME ----
col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png", width=100)  # Make sure logo.png is in the same folder or repo

with col2:
    st.markdown(
        "<h1 style='margin-top: 20px; font-size: 32px;'>Sindicato Interempresa Salud UC</h1>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ---- MAIN TITLE + SUBTITLE ----
st.markdown(
    """
    <h2 style='text-align: center; font-size: 36px;'>Oferta del Empleador - 20 de julio</h2>
    <p style='text-align: center; font-size: 20px;'>¡Revisa si tu voto fue registrado!</p>
    """,
    unsafe_allow_html=True
)

# ---- LOAD DATA FROM GOOGLE SHEETS ----
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

data = load_data()

# ---- STYLES FOR BIG INPUT FIELD ----
st.markdown("""
    <style>
    .big-input input {
        font-size: 20px !important;
        height: 50px !important;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- RUT INPUT SECTION ----
st.markdown("""
    <p style='font-size:22px; margin-bottom: 0;'>Ingresa tu RUT:</p>
    <p style='font-size:14px; margin-top: 2px; color: gray;'>sin puntos y con guión</p>
""", unsafe_allow_html=True)

user_id = st.text_input(label="", key="rut_input", placeholder="Ej: 12345678-9", label_visibility="collapsed")
st.markdown('<div class="big-input"></div>', unsafe_allow_html=True)

# ---- CHECK VOTING STATUS ----
if user_id:
    result = data[data["RUT"].astype(str) == user_id]
    if not result.empty:
        status = result.iloc[0]["Status"]
        st.success(f"Estado: {status}")
    else:
        st.error("Su RUT no fue encontrado en nuestros registros.")
