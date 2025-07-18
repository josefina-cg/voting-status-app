import streamlit as st
import pandas as pd

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Sindicato Interempresa Salud UC", layout="centered")

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
    <p style='text-align: center; font-size: 20px;'>¡Confirma si tu voto fue registrado!</p>
    """,
    unsafe_allow_html=True
)

# ---- LOAD DATA FROM GOOGLE SHEETS ----
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)  # Make sure header is row 2

data = load_data()
data.columns = data.columns.str.strip()  # Remove trailing spaces

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
    # Clean column and input: trim, remove non-breaking spaces, and make uppercase
    clean_ruts = data["RUT"].astype(str).str.strip().str.replace(u'\xa0', '', regex=True).str.upper()
    input_rut = user_id.strip().replace('\u00a0', '').upper()

    result = data[clean_ruts == input_rut]

    if not result.empty:
        status = result.iloc[0][0].strip().lower()

        if status == "votó":
            st.markdown("""
                <div style="background-color:#d4edda; padding:20px; border-radius:8px; color:#155724; font-size:22px; font-weight:bold;">
                    ✅ Estado: Votó
                </div>
            """, unsafe_allow_html=True)
        elif status == "no ha votado":
            st.markdown("""
                <div style="background-color:#f8d7da; padding:20px; border-radius:8px; color:#721c24; font-size:22px; font-weight:bold;">
                    ❌ Estado: No ha Votado
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Estado: {status}")
    else:
        st.markdown("""
    <div style="background-color:#000000; padding:20px; border-radius:8px; color:#ffffff; font-size:20px; font-weight:bold;">
        ⚠️ Su RUT no fue encontrado en nuestros registros.
    </div>
""", unsafe_allow_html=True)

# ---- FOOTER: CENTERED AND MOBILE-OPTIMIZED ----
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #f9f9f9;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        font-size: 14px;
        color: #333;
        z-index: 9999;
        max-width: 90%;
        text-align: left;
    }

    .footer img {
        width: 30px;
        height: auto;
        flex-shrink: 0;
    }

    .footer span {
        display: inline-block;
        max-width: 85vw;
        line-height: 1.4;
    }

    .footer a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }

    .footer a:hover {
        text-decoration: underline;
    }

    @media (max-width: 480px) {
        .footer {
            font-size: 13px;
            padding: 12px;
        }
    }
    </style>

    <div class="footer">
        <img src="https://raw.githubusercontent.com/josefina-cg/voting-status-app/main/BallotBox%20Logo.png" alt="Logo">
        <span>¿Necesitas ayuda? Contáctanos al Whatsapp: <a href="https://wa.me/56923987722" target="_blank">+56 9 2398 7722</a></span>
    </div>
""", unsafe_allow_html=True)
