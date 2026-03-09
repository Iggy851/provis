import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Matriculaciones", layout="wide")
st.title("🚗 MÓDULO DE MATRICULACIONES (Simplificado)")

if 'xml_generado' not in st.session_state:
    st.session_state['xml_generado'] = None
    st.session_state['nombre_archivo'] = None

with st.form("form_matri_simple"):
    col1, col2 = st.columns(2)
    bastidor = col1.text_input("Bastidor (VIN)").upper()
    dni = col2.text_input("DNI / CIF (Solo números)")
    
    nombre = st.text_input("Nombre / Razón Social")
    calle = st.text_input("Calle / Domicilio")
    
    col3, col4, col5 = st.columns(3)
    prov = col3.text_input("Provincia (Ej: BA)")
    muni = col4.text_input("Municipio")
    cp = col5.text_input("CP")
    
    muni_ine = st.text_input("Municipio INE (Código 5 dígitos)")

    if st.form_submit_button("Generar XML Simplificado"):
        fecha = datetime.now().strftime("%d/%m/%Y")
        
        # Estructura mínima necesaria que detectamos en el archivo funcional
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
                <MUNICIPIO_VEHICULO_INE>{muni_ine}</MUNICIPIO_VEHICULO_INE>
                <TIPO_VIA_DIRECCION_VEHICULO>CALLE</TIPO_VIA_DIRECCION_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{dni}</DNI_TITULAR>
            <NOMBRE_TITULAR>{nombre}</NOMBRE_TITULAR>
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
        
        st.session_state['xml_generado'] = xml_content
        st.session_state['nombre_archivo'] = f"matricula_{bastidor}.ga.xml"

if st.session_state['xml_generado']:
    st.success("✅ Archivo generado.")
    st.download_button("⬇️ Descargar .ga.xml", st.session_state['xml_generado'], st.session_state['nombre_archivo'], mime="text/xml")
