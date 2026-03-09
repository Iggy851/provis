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

st.set_page_config(page_title="Gestoría Nogales - Trámites", layout="wide")
st.title("📂 GESTORÍA NOGALES - PORTAL DE TRÁMITES")

if 'xml_generado' not in st.session_state:
    st.session_state['xml_generado'] = None
    st.session_state['nombre_archivo'] = None

opcion = st.sidebar.radio("Selecciona:", ["PROVISIONALES", "MATRICULACIONES"])

if opcion == "MATRICULACIONES":
    st.header("Solicitud de Matriculación (Prueba: Solo dígitos DNI)")
    
    with st.form("form_matri_completo"):
        col1, col2, col3 = st.columns(3)
        bastidor = col1.text_input("Bastidor (VIN)").upper()
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        
        tipo_titular = st.radio("Tipo de Titular", ["Persona Física", "Empresa"], horizontal=True)
        dni_completo = st.text_input("DNI/NIE/CIF completo")
        nombre = st.text_input("Nombre / Razón Social")
        ape1 = st.text_input("Apellido 1")
        ape2 = st.text_input("Apellido 2")
        
        prov_sel = st.selectbox("Provincia", list(PROVINCIAS.keys()), format_func=lambda x: PROVINCIAS[x])
        muni_data = st.selectbox("Municipio", MUNICIPIOS.get(prov_sel, []), format_func=lambda x: x[0])
        nombre_muni, cod_ine, cp = muni_data
        calle = st.text_input("Calle / Vía")
        num = st.text_input("Número")

        submit = st.form_submit_button("Generar archivo .ga.xml")
        
    if submit:
        # LÓGICA DE LIMPIEZA: Extraer solo los primeros 8 dígitos numéricos del DNI
        # Usamos filter(str.isdigit, ...) para asegurar que solo se pasen números
        dni_limpio = "".join(filter(str.isdigit, dni_completo))[:8]
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Version="1.0" Procesar576="1" Procesar05_06="0">
        <JEFATURA>BA</JEFATURA>
        <SUCURSAL/>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <FABRICACION_ITV/>
            <FECHA_MATRICULACION>{fecha_hoy}</FECHA_MATRICULACION>
            <MATRICULA_TEMPORAL/>
            <FECHA_ITV/>
            <TIPO_INSPECCION_ITV>M</TIPO_INSPECCION_ITV>
            <NIVE/>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <DIRECCION_VEHICULO>
                <PROVINCIA_VEHICULO>{prov_sel}</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{nombre_muni}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
                <DOMICILIO_VEHICULO>{calle}</DOMICILIO_VEHICULO>
                <NUMERO_DIRECCION_VEHICULO>{num}</NUMERO_DIRECCION_VEHICULO>
                <MUNICIPIO_VEHICULO_INE>{cod_ine}</MUNICIPIO_VEHICULO_INE>
                <TIPO_VIA_DIRECCION_VEHICULO>CALLE</TIPO_VIA_DIRECCION_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{dni_limpio}</DNI_TITULAR>
            <APELLIDO1_TITULAR>{ape1}</APELLIDO1_TITULAR>
            <APELLIDO2_TITULAR>{ape2}</APELLIDO2_TITULAR>
            <NOMBRE_TITULAR>{nombre}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{prov_sel}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{nombre_muni}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{calle}</NOMBRE_VIA_DIRECCION_TITULAR>
                <NUMERO_DIRECCION_TITULAR>{num}</NUMERO_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <NUMERO_DOCUMENTO>sg-{random.getrandbits(40):x}</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
        
        st.session_state['xml_generado'] = xml_content
        st.session_state['nombre_archivo'] = f"matricula_{bastidor}.ga.xml"

    if st.session_state['xml_generado']:
        st.success("✅ Archivo generado con DNI truncado a 8 dígitos.")
        st.download_button("⬇️ Descargar archivo .ga.xml", st.session_state['xml_generado'], st.session_state['nombre_archivo'], mime="text/xml")
