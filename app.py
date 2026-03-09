import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Test Definitivo", layout="wide")
st.title("🚗 MÓDULO DE MATRICULACIONES (Test 5)")

with st.form("form_matri_test"):
    bastidor = st.text_input("Bastidor (17 caracteres obligatorios)").upper()
    dni = st.text_input("DNI (Formato 12345678A)")
    nombre = st.text_input("Nombre / Razón Social")
    calle = st.text_input("Calle")
    prov = st.text_input("Provincia (Ej: BA)")
    muni = st.text_input("Municipio")
    cp = st.text_input("CP")
    muni_ine = st.text_input("Código INE (5 dígitos)")

    if st.form_submit_button("Generar XML (Nuevo ID)"):
        fecha = datetime.now().strftime("%d/%m/%Y")
        # Generar un ID nuevo completamente aleatorio cada vez
        nuevo_id = f"sg-{random.getrandbits(64):x}"
        
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
        <NUMERO_DOCUMENTO>{nuevo_id}</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
        
        st.download_button("Descargar .ga.xml", xml_content, f"matricula_{bastidor}.ga.xml", mime="text/xml")
