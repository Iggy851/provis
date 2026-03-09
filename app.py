import streamlit as st
from datetime import datetime
import random

# --- CONFIGURACIÓN DE DATOS (Optimizado) ---
# En un futuro, estos datos vendrán de una base de datos o JSON externo
PROVINCIAS = {"BA": "BADAJOZ", "MA": "MADRID", "SE": "SEVILLA"} 
MUNICIPIOS = {
    "BA": [("BADAJOZ", "06015", "06005")],
    "MA": [("MADRID", "28079", "28001")],
    "SE": [("SEVILLA", "41091", "41001")]
}

st.set_page_config(page_title="Gestoría Nogales - Trámites", layout="wide")
st.title("📂 GESTORÍA NOGALES - PORTAL DE TRÁMITES")

# --- MENÚ PRINCIPAL ---
opcion = st.sidebar.radio("Selecciona el trámite:", ["PROVISIONALES", "MATRICULACIONES"])
st.sidebar.divider()

# ==========================================
# 1. TRÁMITE DE PROVISIONALES
# ==========================================
if opcion == "PROVISIONALES":
    st.header("Generación de Justificante Provisional")
    with st.form("form_prov"):
        # (Aquí mantienes tu lógica actual de provisionales)
        st.write("Formulario de Provisionales activo.")
        if st.form_submit_button("Generar Provisional"):
            st.success("Provisional generado.")

# ==========================================
# 2. TRÁMITE DE MATRICULACIONES
# ==========================================
else:
    st.header("Solicitud de Matriculación")
    with st.form("form_matri_completo"):
        # Sección 1: Vehículo
        st.subheader("1. Datos del Vehículo")
        col1, col2, col3 = st.columns(3)
        bastidor = col1.text_input("Bastidor (VIN)").upper()
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        st.info(f"Fecha de Matriculación: {fecha_hoy}")
        
        # Sección 2: Titular
        st.subheader("2. Datos del Titular")
        tipo_titular = st.radio("Tipo de Titular", ["Persona Física", "Empresa"], horizontal=True)
        c4, c5 = st.columns(2)
        dni = c4.text_input("DNI/NIE/CIF")
        if tipo_titular == "Persona Física":
            nombre = c5.text_input("Nombre")
            ape1 = c4.text_input("1er Apellido")
            ape2 = c5.text_input("2do Apellido")
            f_nac = c4.date_input("Fecha de Nacimiento")
        else:
            razon_social = c5.text_input("Razón Social")

        # Sección 3: Domicilio
        st.subheader("3. Domicilio (Titular y Vehículo)")
        c6, c7, c8 = st.columns(3)
        prov_sel = c6.selectbox("Provincia", list(PROVINCIAS.keys()), format_func=lambda x: PROVINCIAS[x])
        munis_disp = MUNICIPIOS.get(prov_sel, [])
        muni_data = c7.selectbox("Municipio", munis_disp, format_func=lambda x: x[0])
        nombre_muni, cod_ine, cp = muni_data
        c8.text(f"CP: {cp}")
        
        calle = st.text_input("Calle / Vía")
        num = st.text_input("Número")

        if st.form_submit_button("Generar archivo .ga.xml"):
            # Generación de ID único (similar al formato del archivo real)
            id_doc = f"sg-{random.getrandbits(64):x}"
            
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Version="1.0" Procesar576="1" Procesar05_06="0">
        <JEFATURA>BA</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <FECHA_MATRICULACION>{fecha_hoy}</FECHA_MATRICULACION>
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
            <DNI_TITULAR>{dni}</DNI_TITULAR>
            <NOMBRE_TITULAR>{nombre if tipo_titular == 'Persona Física' else razon_social}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>{prov_sel}</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{nombre_muni}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{calle}</NOMBRE_VIA_DIRECCION_TITULAR>
                <NUMERO_DIRECCION_TITULAR>{num}</NUMERO_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <NUMERO_DOCUMENTO>{id_doc}</NUMERO_DOCUMENTO>
    </MATRICULACION>
</FORMATO_GA>"""
            st.download_button("Descargar .ga.xml", xml_content, file_name=f"matricula_{bastidor}.ga.xml")
