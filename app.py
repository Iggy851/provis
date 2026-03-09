import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Gestoría Nogales - Generador .ga.xml", layout="wide")

st.title("🚗 Generador XML para Matriculaciones")
st.info("El archivo se descargará con la extensión necesaria para el sistema: .ga.xml")

with st.form("form_final"):
    c1, c2 = st.columns(2)
    with c1:
        bastidor = st.text_input("Bastidor (VIN)", value="UU1DJF00576399771").upper()
        nif = st.text_input("NIF Titular", value="09208671T")
        nombre = st.text_input("Nombre", value="ISABEL")
        apellido1 = st.text_input("1er Apellido", value="GONZALEZ")
        apellido2 = st.text_input("2do Apellido", value="LOPEZ")
    
    with c2:
        municipio = st.text_input("Municipio", value="MONTIJO")
        cp = st.text_input("CP", value="06480")
        via = st.text_input("Vía/Calle", value="NAVA")
        nive = st.text_input("NIVE", value="4F15E5D9285E4694B24A1122DB5A40B6")

    if st.form_submit_button("GENERAR ARCHIVO .GA.XML"):
        fecha = datetime.now().strftime("%d/%m/%Y")
        # Generamos un número de expediente similar al de tus ejemplos (SIGA.XXXXXXX)
        num_exp = f"SIGA.{random.randint(8000000, 8999999)}"
        num_doc = f"sg-{random.getrandbits(64):016x}"
        
        # XML construido siguiendo el orden exacto de tus archivos 'SIGA'
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION Procesar05_06="0" Procesar576="1" Version="1.0">
        <JEFATURA>BA</JEFATURA>
        <SUCURSAL/>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{fecha}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>{num_exp}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <FABRICACION_ITV/>
            <FECHA_MATRICULACION>{fecha}</FECHA_MATRICULACION>
            <MATRICULA_TEMPORAL/>
            <FECHA_ITV/>
            <TIPO_INSPECCION_ITV>M</TIPO_INSPECCION_ITV>
            <TIPO_VEHICULO/>
            <NUEVO>SI</NUEVO>
            <USADO>NO</USADO>
            <FECHA_PRIMERA_MATRICULACION/>
            <PROCEDENCIA_VEHICULO>0</PROCEDENCIA_VEHICULO>
            <MATRICULA_ORIGINAL/>
            <MATRICULA_ORIGINAL_EXTRANJERA/>
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
            <DATOS_RUEDAS>
                <NUMERO_RUEDAS>04</NUMERO_RUEDAS>
                <NUMERO_EJES>2</NUMERO_EJES>
            </DATOS_RUEDAS>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{nif}</DNI_TITULAR>
            <RAZON_SOCIAL_TITULAR/>
            <APELLIDO1_TITULAR>{apellido1}</APELLIDO1_TITULAR>
            <APELLIDO2_TITULAR>{apellido2}</APELLIDO2_TITULAR>
            <NOMBRE_TITULAR>{nombre}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <PROVINCIA_TITULAR>BA</PROVINCIA_TITULAR>
                <MUNICIPIO_TITULAR>{municipio}</MUNICIPIO_TITULAR>
                <CP_TITULAR>{cp}</CP_TITULAR>
                <NOMBRE_VIA_DIRECCION_TITULAR>{via}</NOMBRE_VIA_DIRECCION_TITULAR>
            </DIRECCION_TITULAR>
            <SEXO_TITULAR>H</SEXO_TITULAR>
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

        # IMPORTANTE: El nombre del archivo ahora termina en .ga.xml
        nombre_archivo = f"matricula_{bastidor}.ga.xml"
        
        st.download_button(
            label="⬇️ DESCARGAR ARCHIVO .GA.XML",
            data=xml_content,
            file_name=nombre_archivo,
            mime="text/xml"
        )
