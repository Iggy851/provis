import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Matriculación Pro", layout="wide")
st.title("🚗 GENERADOR XML MATRICULACIÓN")

# Inicializar sesión
if 'xml_generado' not in st.session_state:
    st.session_state['xml_generado'] = None
    st.session_state['nombre_archivo'] = None

with st.form("form_matri_pro"):
    # Datos básicos
    bastidor = st.text_input("Bastidor (17 caracteres)").upper()
    tipo_titular = st.radio("Tipo de Titular", ["Persona Física", "Empresa"])
    
    # Datos Titular
    nif = st.text_input("NIF / NIE / CIF")
    calle = st.text_input("Calle")
    cp = st.text_input("CP")
    municipio = st.text_input("Municipio")
    prov = st.text_input("Provincia (Ej: BA)")
    
    if tipo_titular == "Persona Física":
        nombre = st.text_input("Nombre")
        ape1 = st.text_input("1er Apellido")
        ape2 = st.text_input("2do Apellido")
        fecha_nac = st.date_input("Fecha de Nacimiento", value=datetime(1980, 1, 1))
        sexo = st.selectbox("Sexo", ["V", "H"])
    else:
        razon_social = st.text_input("Razón Social")
        fecha_nac = None
        sexo = "X"
        nombre, ape1, ape2 = "", "", ""

    # Botón de proceso (dentro del form)
    submitted = st.form_submit_button("GENERAR XML")

if submitted:
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    f_nac_str = fecha_nac.strftime("%d/%m/%Y") if fecha_nac else ""
    razon_t = razon_social if tipo_titular == "Empresa" else ""

    # XML con estructura mínima pero jerarquía completa
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Version="1.0" Procesar576="1" Procesar05_06="0">
        <JEFATURA>{prov}</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <DIRECCION_VEHICULO>
                <PROVINCIA_VEHICULO>{prov}</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{municipio}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{nif}</DNI_TITULAR>
            <RAZON_SOCIAL_TITULAR>{razon_t}</RAZON_SOCIAL_TITULAR>
            <APELLIDO1_TITULAR>{ape1}</APELLIDO1_TITULAR>
            <APELLIDO2_TITULAR>{ape2}</APELLIDO2_TITULAR>
            <NOMBRE_TITULAR>{nombre}</NOMBRE_TITULAR>
            <FECHA_NACIMIENTO_TITULAR>{f_nac_str}</FECHA_NACIMIENTO_TITULAR>
            <SEXO_TITULAR>{sexo}</SEXO_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{prov}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{municipio}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{calle}</NOMBRE_VIA_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <NUMERO_DOCUMENTO>sg-{random.getrandbits(32):x}</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
    
    st.session_state['xml_generado'] = xml_content
    st.session_state['nombre_archivo'] = f"matricula_{bastidor}.ga.xml"

# Botón de descarga (FUERA del form)
if st.session_state['xml_generado']:
    st.download_button(
        label="⬇️ DESCARGAR .GA.XML", 
        data=st.session_state['xml_generado'], 
        file_name=st.session_state['nombre_archivo'], 
        mime="text/xml"
    )
