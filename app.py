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

st.set_page_config(page_title="Gestoría Nogales", layout="wide")
st.title("📂 GESTORÍA NOGALES - PORTAL DE TRÁMITES")

if 'xml_generado' not in st.session_state:
    st.session_state['xml_generado'] = None
    st.session_state['nombre_archivo'] = None

# Sidebar navegación
opcion = st.sidebar.radio("Selecciona el trámite:", ["MATRICULACIONES", "PROVISIONALES"])

# ==========================================
# 1. MATRICULACIONES
# ==========================================
if opcion == "MATRICULACIONES":
    st.header("Solicitud de Matriculación")
    
    with st.form("form_matri_completo"):
        col1, col2 = st.columns(2)
        bastidor = col1.text_input("Bastidor (VIN)").upper()
        
        # Selección de tipo de titular
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

        if st.form_submit_button("Generar XML Matriculación"):
            # Limpieza: solo números para el XML
            dni_limpio = "".join(filter(str.isdigit, dni_input))
            fecha = datetime.now().strftime("%d/%m/%Y")
            nombre_xml = f"{nombre} {ape1} {ape2}".strip() if tipo_titular == "Persona Física" else nombre
            
            # XML ajustado para evitar el error "Núm doc (1)"
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Version="1.0" Procesar576="1" Procesar05_06="0">
        <JEFATURA>BA</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
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
        st.success("✅ Archivo matriculación generado.")
        st.download_button("⬇️ Descargar .ga.xml", st.session_state['xml_generado'], st.session_state['nombre_archivo'], mime="text/xml")

# ==========================================
# 2. PROVISIONALES
# ==========================================
elif opcion == "PROVISIONALES":
    st.header("Generación de Justificante Provisional")
    
    with st.form("form_prov"):
        tipo_titular = st.radio("Tipo de Titular", ["Persona Física", "Empresa"], horizontal=True)
        
        if tipo_titular == "Persona Física":
            col_p1, col_p2, col_p3 = st.columns(3)
            col_p1.text_input("Nombre")
            col_p2.text_input("1er Apellido")
            col_p3.text_input("2do Apellido")
        else:
            st.text_input("Razón Social")
        
        matricula = st.text_input("Matrícula").upper()
        
        if st.form_submit_button("Generar Provisional"):
            st.info(f"Módulo de provisionales activo para: {matricula}")
