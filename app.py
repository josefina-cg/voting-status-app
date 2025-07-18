import streamlit as st
import pandas as pd

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Voting Status Checker", layout="centered")

# ---- HEADER: LOGO + ORG NAME (Mobile-friendly Flexbox) ----
st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: nowrap;
    }
    .header-container img {
        width: 60px;
        height: auto;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }
    @media (max-width: 768px) {
        .header-container {
            flex-wrap: wrap;
            justify-content: center;
            text-align: center;
        }
        .header-container img {
            margin-bottom: 10px;
        }
    }
    </style>

    <div class="header-container">
        <img src="https://raw.githubusercontent.com/josefina-cg/voting-status-app/main/logo.png" alt="Logo">
        <p class="header-title">Sindicato Interempresa Salud UC</p>
    </div>
    <hr>
""", unsafe_allow_html=True)  # ← Correct closing here

# ---- MAIN TITLE + SUBTITLE ----
st.markdown(
    """
    <h2 style='text-align: center; font-size: 36px;'>Votación Oferta del Empleador - 20 de julio</h2>
    <p style='text-align: center; font-size: 20px;'>¡Confirme si tu voto fue registrado!</p>
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
    <p style='font-size:14px; margin-top: 2px; color: gray;'>Sin puntos y con guión</p>
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

# ---- FOOTER: CONTACT INFO ----
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        background-color: #f9f9f9;
        padding: 10px 15px;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        color: #333;
        z-index: 9999;
    }
    .footer img {
        width: 30px;
        height: auto;
    }
    .footer a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        <img src="https://raw.githubusercontent.com/josefina-cg/voting-status-app/main/BallotBox%20Logo.png" alt="Logo">
        <span>¿Necesitas ayuda? Contáctanos al Whatsapp: <a href="https://wa.me/56923987722" target="_blank">+56 9 2398 7722</a></span>
    </div>
""", unsafe_allow_html=True)


