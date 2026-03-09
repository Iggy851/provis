import streamlit as st
from datetime import datetime
import random

# --- CONFIGURACIÓN ---
PROVINCIAS = {"BA": "BADAJOZ", "MA": "MADRID", "SE": "SEVILLA"} 
MUNICIPIOS = {
    "BA": [("BADAJOZ", "06015", "06005")],
    "MA": [("MADRID", "28079", "28001")],
    "SE": [("SEVILLA", "41091", "41001")]
}

st.set_page_config(page_title="Gestoría Nogales - Matriculaciones", layout="wide")
st.title("🚗 MÓDULO DE MATRICULACIONES")

if 'xml_generado' not in st.session_state:
    st.session_state['xml_generado'] = None
    st.session_state['nombre_archivo'] = None

with st.form("form_matri_pro"):
    col1, col2 = st.columns(2)
    bastidor = col1.text_input("Bastidor (VIN)").upper()
    
    tipo_titular = st.radio("Tipo de Titular", ["Persona Física", "Empresa"], horizontal=True)
    dni_input = st.text_input("DNI / CIF (Solo números)")
    
    if tipo_titular == "Persona Física":
        c_nom, c_ap1, c_ap2 = st.columns(3)
        nombre = c_nom.text_input("Nombre")
        ape1 = c_ap1.text_input("1er Apellido")
        ape2 = c_ap2.text_input("2do Apellido")
    else:
        nombre = st.text_input("Razón Social")
        ape1, ape2 = "", ""
        
    calle = st.text_input("Calle")
    prov_sel = st.selectbox("Provincia", list(PROVINCIAS.keys()))
    muni_data = st.selectbox("Municipio", MUNICIPIOS.get(prov_sel, []))
    nombre_muni, cod_ine, cp = muni_data

    if st.form_submit_button("Generar XML"):
        dni_limpio = "".join(filter(str.isdigit, dni_input))
        fecha = datetime.now().strftime("%d/%m/%Y")
        nombre_xml = f"{nombre} {ape1} {ape2}".strip() if tipo_titular == "Persona Física" else nombre
        
        # XML basado en la estructura de tu archivo funcional
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
                <PROVINCIA_VEHICULO>{prov_sel}</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{nombre_muni}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
                <DOMICILIO_VEHICULO>{calle}</DOMICILIO_VEHICULO>
                <MUNICIPIO_VEHICULO_INE>{cod_ine}</MUNICIPIO_VEHICULO_INE>
                <TIPO_VIA_DIRECCION_VEHICULO>CALLE</TIPO_VIA_DIRECCION_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{dni_limpio}</DNI_TITULAR>
            <NOMBRE_TITULAR>{nombre_xml}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{prov_sel}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{nombre_muni}</MUNICIPIO_TITULAR>
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
    st.success("✅ Archivo listo.")
    st.download_button("⬇️ Descargar .ga.xml", st.session_state['xml_generado'], st.session_state['nombre_archivo'], mime="text/xml")
