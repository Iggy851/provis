import streamlit as st
from datetime import datetime
import random

# Configuración de página
st.set_page_config(page_title="Gestoría Nogales - Test .ga.xml", layout="wide")

st.title("🚗 Generador XML (Con Datos de Prueba)")

# 1. INICIALIZAR ESTADO
if 'xml_data' not in st.session_state:
    st.session_state.xml_data = None
if 'archivo_nombre' not in st.session_state:
    st.session_state.archivo_nombre = None

# 2. FORMULARIO CON DATOS RELLENOS (Defaults)
with st.form("form_matriculacion"):
    c1, c2 = st.columns(2)
    with c1:
        # He puesto los datos exactos de uno de tus archivos que funcionan
        bastidor = st.text_input("Bastidor (VIN)", value="UU1DJF00576399771").upper()
        nif = st.text_input("NIF Titular", value="09208671T")
        nombre = st.text_input("Nombre / Razón Social", value="ISABEL")
        apellido1 = st.text_input("1er Apellido", value="GONZALEZ")
        apellido2 = st.text_input("2do Apellido", value="LOPEZ")
    
    with c2:
        municipio = st.text_input("Municipio", value="MONTIJO")
        cp = st.text_input("CP", value="06480")
        via = st.text_input("Calle/Vía", value="NAVA")
        nive = st.text_input("NIVE", value="4F15E5D9285E4694B24A1122DB5A40B6")
        tipo_t = st.radio("Tipo Titular", ["Persona Física", "Empresa"], index=0)

    submit = st.form_submit_button("PREPARAR ARCHIVO")

# 3. LÓGICA DE GENERACIÓN
if submit:
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    num_exp = f"SIGA.{random.randint(8000000, 8999999)}"
    num_doc = f"sg-{random.getrandbits(64):016x}"
    sexo = "H" if tipo_t == "Persona Física" else "X"
    
    # Estructura idéntica a tus archivos originales
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Procesar05_06="0" Procesar576="1" Version="1.0">
        <JEFATURA>BA</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>{num_exp}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <FABRICACION_ITV>IM</FABRICACION_ITV>
            <FECHA_MATRICULACION>{fecha_hoy}</FECHA_MATRICULACION>
            <TIPO_INSPECCION_ITV>M</TIPO_INSPECCION_ITV>
            <NUEVO>SI</NUEVO>
            <USADO>NO</USADO>
            <PROCEDENCIA_VEHICULO>0</PROCEDENCIA_VEHICULO>
            <FICHAELECTRONICA>SI</FICHAELECTRONICA>
            <NIVE>{nive}</NIVE>
            <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
            <DATOS_COMBUSTIBLE>
                <EMISION_CO2>116000</EMISION_CO2>
                <CARBURANTE>G</CARBURANTE>
            </DATOS_COMBUSTIBLE>
            <DIRECCION_VEHICULO>
                <PROVINCIA_VEHICULO>BA</PROVINCIA_VEHICULO>
                <MUNICIPIO_VEHICULO>{municipio}</MUNICIPIO_VEHICULO>
                <CP_VEHICULO>{cp}</CP_VEHICULO>
                <DOMICILIO_VEHICULO>{via}</DOMICILIO_VEHICULO>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{nif}</DNI_TITULAR>
            <RAZON_SOCIAL_TITULAR>{nombre if tipo_t == 'Empresa' else ""}</RAZON_SOCIAL_TITULAR>
            <APELLIDO1_TITULAR>{apellido1}</APELLIDO1_TITULAR>
            <APELLIDO2_TITULAR>{apellido2}</APELLIDO2_TITULAR>
            <NOMBRE_TITULAR>{nombre if tipo_t == 'Persona Física' else ""}</NOMBRE_TITULAR>
            <SEXO_TITULAR>{sexo}</SEXO_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>BA</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{municipio}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{via}</NOMBRE_VIA_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <DATOS_IMPUESTOS>
            <DATOS_IMVTM><JUSTIFICANTE_EXENCION_IMVTM>SI</JUSTIFICANTE_EXENCION_IMVTM></DATOS_IMVTM>
            <DATOS_576>
                <EXENTO_576>NO</EXENTO_576>
                <BASE_IMPONIBLE_576>00001405805</BASE_IMPONIBLE_576>
            </DATOS_576>
            <MODELO_ACTIVO>SI</MODELO_ACTIVO>
            <MODELO_IMPUESTO_MATRICULACION>576</MODELO_IMPUESTO_MATRICULACION>
        </DATOS_IMPUESTOS>
        <DATOS_LIMITACION>
            <FINANCIERA_LIMITACION>NO SUJETOS IEDMT</FINANCIERA_LIMITACION>
        </DATOS_LIMITACION>
        <NUMERO_DOCUMENTO>{num_doc}</NUMERO_DOCUMENTO>
        <TIPO_MATRICULACION>1</TIPO_MATRICULACION>
    </MATRICULACION>
</FORMATO_GA>"""
        
    st.session_state.xml_data = xml_content
    st.session_state.archivo_nombre = f"matricula_{bastidor}.ga.xml"

# 4. BOTÓN DE DESCARGA
if st.session_state.xml_data:
    st.divider()
    st.success(f"✅ Archivo preparado.")
    st.download_button(
        label=f"⬇️ DESCARGAR {st.session_state.archivo_nombre}",
        data=st.session_state.xml_data,
        file_name=st.session_state.archivo_nombre,
        mime="text/xml"
    )
