import streamlit as st
from datetime import datetime
import random
import unicodedata

def limpiar_texto(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.upper()

st.set_page_config(page_title="Gestoría Nogales - Matriculaciones", layout="wide")
st.title("🚗 MÓDULO DE MATRICULACIONES (Simplificado)")

if 'xml_data' not in st.session_state:
    st.session_state['xml_data'] = None
    st.session_state['nombre_archivo'] = None

with st.form("form_matri_simple"):
    bastidor = st.text_input("Bastidor (17 caracteres)").upper()
    dni = st.text_input("DNI (Ej: 12345678X)")
    nombre = st.text_input("Nombre / Razón Social")
    calle = st.text_input("Calle")
    prov = st.text_input("Provincia (Ej: BA)")
    muni = st.text_input("Municipio")
    cp = st.text_input("CP")
    
    submitted = st.form_submit_button("GENERAR XML")

if submitted:
    # Código INE por defecto (ajusta este valor si necesitas uno específico para Badajoz)
    ine_default = "06015" 
    
    fecha = datetime.now().strftime("%d/%m/%Y")
    n_limpio = limpiar_texto(nombre)
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Version="1.0" Procesar576="1" Procesar05_06="0">
        <JEFATURA>BA</JEFATURA>
        <SUCURSAL/>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <FABRICACION_ITV/>
            <FECHA_MATRICULACION>{fecha}</FECHA_MATRICULACION>
            <NIVE/>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <DIRECCION_VEHICULO>
                <PROVINCIA_VEHICULO>{prov}</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{muni}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
                <DOMICILIO_VEHICULO>{calle}</DOMICILIO_VEHICULO>
                <MUNICIPIO_VEHICULO_INE>{ine_default}</MUNICIPIO_VEHICULO_INE>
                <TIPO_VIA_DIRECCION_VEHICULO>CALLE</TIPO_VIA_DIRECCION_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{dni}</DNI_TITULAR>
            <NOMBRE_TITULAR>{n_limpio}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{prov}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{muni}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{calle}</NOMBRE_VIA_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <NUMERO_DOCUMENTO>sg-08469aee8de43bf0</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
    
    st.session_state['xml_data'] = xml_content
    st.session_state['nombre_archivo'] = f"matricula_{bastidor}.ga.xml"

if st.session_state['xml_data']:
    st.success("✅ Datos generados.")
    st.download_button("⬇️ DESCARGAR .GA.XML", st.session_state['xml_data'], st.session_state['nombre_archivo'], mime="text/xml")
