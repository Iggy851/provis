import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Generador .ga.xml", layout="wide")

st.title("🚗 Generador XML para Matriculaciones")
st.info("Formato de salida: .ga.xml")

# 1. INICIALIZAR ESTADO (Fuera del formulario)
if 'xml_finalizado' not in st.session_state:
    st.session_state.xml_finalizado = None
    st.session_state.archivo_nombre = None

# 2. FORMULARIO DE DATOS
with st.form("form_matriculacion_definitivo"):
    c1, c2 = st.columns(2)
    with c1:
        bastidor = st.text_input("Bastidor (VIN)", value="UU1DJF00576399771").upper()
        nif = st.text_input("NIF Titular", value="09208671T")
        nombre = st.text_input("Nombre", value="ISABEL")
        apellido1 = st.text_input("1er Apellido", value="GONZALEZ")
        apellido2 = st.text_input("2do Apellido", value="LOPEZ")
        fecha_nac = st.date_input("Fecha Nacimiento", value=datetime(1980, 1, 1))
    
    with c2:
        municipio = st.text_input("Municipio", value="MONTIJO")
        cp = st.text_input("CP", value="06480")
        via = st.text_input("Vía/Calle", value="NAVA")
        nive = st.text_input("NIVE", value="4F15E5D9285E4694B24A1122DB5A40B6")
        sexo = st.selectbox("Sexo", ["H", "V"])

    # Este botón solo PROCESA, no descarga
    boton_procesar = st.form_submit_button("PREPARAR ARCHIVO")

# 3. LÓGICA DE PROCESAMIENTO (Fuera del formulario)
if boton_procesar:
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    f_nac = fecha_nac.strftime("%d/%m/%Y")
    num_exp = f"SIGA.{random.randint(8000000, 8999999)}"
    num_doc = f"sg-{random.getrandbits(64):016x}"
    
    # Estructura clonada de tus archivos SIGA
