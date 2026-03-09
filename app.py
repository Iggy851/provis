import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Generador XML Completo", layout="wide")

# Estado de la sesión para el botón de descarga
if 'xml_data' not in st.session_state:
    st.session_state.xml_data = None

st.title("🚗 Generador XML (Estructura Real)")
st.info("Esta versión incluye todos los bloques técnicos detectados en tus archivos originales para evitar el error de esquema.")

with st.form("form_completo"):
    col1, col2 = st.columns(2)
    with col1:
        bastidor = st.text_input("Bastidor (17 caracteres)", value="UU1DJF00576399771").upper()
        nif = st.text_input("NIF / NIE / CIF del Titular", value="09208671T")
        tipo_titular = st.radio("Tipo", ["Persona Física", "Empresa"])
        nombre = st.text_input("Nombre / Razón Social")
    
    with col2:
        provincia = st.text_input("Provincia (Ej: BA)", value="BA")
        municipio = st.text_input("Municipio", value="MONTIJO")
        cp = st.text_input("Código Postal", value="06480")
        calle = st.text_input("Calle/Dirección", value="NAVA")

    if st.form_submit_button("GENERAR ESTRUCTURA COMPLETA"):
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        num_exp = f"SIGA.{random.randint(1000000, 9999999)}"
        num_doc = f"sg-{random.getrandbits(64):016x}"
        
        # Lógica de nombres según tus archivos
        razon_social = nombre if tipo_titular == "Empresa" else ""
        nombre_t = nombre if tipo_titular == "Persona Física" else ""
        sexo = "V" if tipo_titular == "Persona Física" else "X"

        # XML Reconstruido fielmente a partir de tus archivos
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Procesar05_06="0" Procesar576="1" Version="1.0">
        <JEFATURA>{provincia}</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>{num_exp}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <NUEVO>SI</NUEVO>
            <USADO>NO</USADO>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <DATOS_COMBUSTIBLE>
                <EMISION_CO2>000000</EMISION_CO2>
                <CARBURANTE>G</CARBURANTE>
            </DATOS_COMBUSTIBLE>
            <DIRECCION_VEHICULO>
                <PROVINCIA_VEHICULO>{provincia}</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{municipio}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{nif}</DNI_TITULAR>
            <RAZON_SOCIAL_TITULAR>{razon_social}</RAZON_SOCIAL_TITULAR>
            <NOMBRE_TITULAR>{nombre_t}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{provincia}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{municipio}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{calle}</NOMBRE_VIA_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
            <SEXO_TITULAR>{sexo}</SEXO_TITULAR>
        </DATOS_TITULAR>
        <DATOS_IMPUESTOS>
            <DATOS_576>
                <EXENTO_576>NO</EXENTO_576>
            </DATOS_576>
        </DATOS_IMPUESTOS>
        <DATOS_LIMITACION>
            <FINANCIERA_LIMITACION>NO SUJETOS IEDMT</FINANCIERA_LIMITACION>
        </DATOS_LIMITACION>
        <NUMERO_DOCUMENTO>{num_doc}</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
        st.session_state.xml_data = xml_content

# Botón de descarga fuera del formulario
if st.session_state.xml_data:
    st.download_button(
        label="⬇️ Descargar XML para probar",
        data=st.session_state.xml_data,
        file_name="prueba_matriculacion.xml",
        mime="text/xml"
    )
