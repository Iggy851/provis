import streamlit as st
from datetime import datetime
import random

# Configuración de página
st.set_page_config(page_title="Gestoría Nogales - Generador .ga.xml", layout="wide")

st.title("🚗 Generador XML para Matriculaciones")
st.info("Instrucciones: 1. Rellena los datos. 2. Pulsa 'PREPARAR'. 3. Pulsa el botón azul de 'DESCARGAR' que aparecerá abajo.")

# 1. INICIALIZAR ESTADO (Para que no se borre al recargar)
if 'xml_data' not in st.session_state:
    st.session_state.xml_data = None
if 'archivo_nombre' not in st.session_state:
    st.session_state.archivo_nombre = None

# 2. FORMULARIO
with st.form("form_matriculacion"):
    c1, c2 = st.columns(2)
    with c1:
        bastidor = st.text_input("Bastidor (VIN)").upper()
        nif = st.text_input("NIF Titular")
        nombre = st.text_input("Nombre / Razón Social")
        apellido1 = st.text_input("1er Apellido (vacío si es Empresa)")
        apellido2 = st.text_input("2do Apellido (vacío si es Empresa)")
    
    with c2:
        municipio = st.text_input("Municipio")
        cp = st.text_input("CP")
        via = st.text_input("Calle/Vía")
        nive = st.text_input("NIVE (si lo tienes)")
        tipo_t = st.radio("Tipo Titular", ["Persona Física", "Empresa"])

    # El botón del formulario SOLO activa el procesamiento
    submit = st.form_submit_button("PREPARAR ARCHIVO")

# 3. LÓGICA DE GENERACIÓN
if submit:
    if not bastidor or not nif:
        st.error("El Bastidor y el NIF son obligatorios.")
    else:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        num_exp = f"SIGA.{random.randint(8000000, 8999999)}"
        num_doc = f"sg-{random.getrandbits(64):016x}"
        sexo = "H" if tipo_t == "Persona Física" else "X"
        
        # Estructura de alta compatibilidad (basada en tus archivos)
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Procesar05_06="0" Procesar576="1" Version="1.0">
        <JEFATURA>BA</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha_hoy}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>{num_exp}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <FECHA_MATRICULACION>{fecha_hoy}</FECHA_MATRICULACION>
            <TIPO_INSPECCION_ITV>M</TIPO_INSPECCION_ITV>
            <NUEVO>SI</NUEVO>
            <USADO>NO</USADO>
            <PROCEDENCIA_VEHICULO>0</PROCEDENCIA_VEHICULO>
            <FICHAELECTRONICA>SI</FICHAELECTRONICA>
            <NIVE>{nive if nive else ""}</NIVE>
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
        
        # Guardamos en el estado para que sobreviva a la recarga
        st.session_state.xml_data = xml_content
        st.session_state.archivo_nombre = f"matricula_{bastidor}.ga.xml"

# 4. BOTÓN DE DESCARGA REAL (Siempre fuera del formulario)
if st.session_state.xml_data:
    st.divider()
    st.success(f"✅ Archivo '{st.session_state.archivo_nombre}' listo para descargar.")
    st.download_button(
        label="⬇️ DESCARGAR AHORA (.ga.xml)",
        data=st.session_state.xml_data,
        file_name=st.session_state.archivo_nombre,
        mime="text/xml"
    )
