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
    <p style='text-align: center; font-size: 20px;'>¡Confirma si tu voto fue registrado!</p>
    """,
    unsafe_allow_html=True
)

# ---- LOAD DATA FROM GOOGLE SHEETS ----
sheet_url = "https://docs.google.com/spreadsheets/d/1bLu7UgEt7aS9a39tUYUt9n6_fSjNc5qQ/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

data = load_data()

# Defensive programming: ensure data loaded correctly
if not data.empty:
    data.columns = data.columns.str.strip()
    st.write("📄 Columnas detectadas:", data.columns.tolist())
else:
    st.error("❌ No se pudo cargar la información desde la hoja de cálculo.")
# DEBUGGING: Print the first few rows of the sheet
st.write("🧪 Preview of loaded data:")
st.write(data.head())

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
    # Try to find the RUT column
    rut_col = [col for col in data.columns if "rut" in col.lower()]
    if not rut_col:
        st.error("❌ No se encontró la columna de RUT.")
    else:
        # Clean RUTs
        clean_ruts = data[rut_col[0]].astype(str).str.strip().str.replace(u'\xa0', '', regex=True).str.upper()
        input_rut = user_id.strip().replace('\u00a0', '').upper()
        result = data[clean_ruts == input_rut]

        if result.empty:
            st.error("Su RUT no fue encontrado en nuestros registros.")
        else:
            # Find the Status column
            status_col = [col for col in data.columns if "status" in col.lower()]
            if not status_col:
                st.error("❌ No se encontró la columna de estado.")
            else:
                status = result.iloc[0][status_col[0]]
                st.success(f"Estado: {status}")

    # Optional debug
    # st.write("🔍 Cleaned RUTs:", clean_ruts.tolist())
    # st.write("🔍 Input RUT:", input_rut)

    # Compare
    result = data[clean_ruts == input_rut]

    if not result.empty:
        status = result.iloc[0]["Status"]
        st.success(f"Estado: {status}")
    else:
        st.error("Su RUT no fue encontrado en nuestros registros.")


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
