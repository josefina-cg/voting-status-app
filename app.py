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
""", unsafe_allow_html=True)

# ✅ This is a new separate block — don't combine with the above
st.markdown("""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/josefina-cg/voting-status-app/main/logo.png" alt="Logo">
        <p class="header-title">Sindicato Interempresa Salud UC</p>
    </div>
    <hr>
""", unsafe_allow_html=True)


# ---- MAIN TITLE + SUBTITLE ----
st.markdown("""
    <h2 style='text-align: center; font-size: 36px;'>Nueva Oferta del Empleador</h2>
    <p style='text-align: center; font-size: 20px;'>¡Confirma si tu voto fue registrado!</p>
""", unsafe_allow_html=True)

# ---- LOAD DATA FROM GOOGLE SHEETS ----
sheet_url = "https://docs.google.com/spreadsheets/d/17m1Km09QjTSH2fia8rPyqx393DiUv2eLJ5z7cTxiV74/export?format=csv&gid=2002531286"
df = pd.read_csv(sheet_url)

st.dataframe(df)

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

# ---- INPUT FIELD & MATCHING LOGIC ----

# Clean headers
data.columns = data.columns.str.strip()

# Normalize 'RUT' and 'Estado' values
data["RUT"] = data["RUT"].astype(str)\
    .str.replace(u'\xa0', '', regex=True)\
    .str.strip()\
    .str.upper()

data["Estado"] = data["Estado"].astype(str)\
    .str.replace(u'\xa0', '', regex=True)\
    .str.strip()\
    .str.lower()

st.write("Estado detectado:", estado)

# Input field
user_id = st.text_input("Ingresa tu RUT:", "").strip()

# Normalize input RUT
input_rut = user_id.replace('\u00a0', '').strip().upper()

# Match RUT
result = data[data["RUT"] == input_rut]

if not result.empty:
    estado = result["Estado"].values[0]
    estado = str(estado).replace('\u00a0', '').strip().lower()  # <-- THIS FIXES YOUR ISSUE

    if estado == "votó":
        st.markdown("""
            <div style="background-color:#d4edda; padding:20px; border-radius:8px; color:#155724; font-size:22px; font-weight:bold;">
                ✅ Estado: Votó
            </div>
        """, unsafe_allow_html=True)
    elif estado == "no ha votado":
        st.markdown("""
            <div style="background-color:#f8d7da; padding:20px; border-radius:8px; color:#721c24; font-size:22px; font-weight:bold;">
                ❌ Estado: No ha Votado
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"Estado desconocido: {estado}")
elif user_id != "":
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
        <img src="https://raw.githubusercontent.com/josefina-cg/voting-Estado-app/main/BallotBox%20Logo.png" alt="Logo">
        <span>¿Necesitas ayuda? Contáctanos al Whatsapp: <a href="https://wa.me/56923987722" target="_blank">+56 9 2398 7722</a></span>
    </div>
""", unsafe_allow_html=True)
