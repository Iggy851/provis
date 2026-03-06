import streamlit as st
import xml.etree.ElementTree as ET
from datetime import datetime
import random
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

# --- CONFIGURACIÓN ---
EMAIL_EMISOR = st.secrets.get("EMAIL_EMISOR", "")
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", "")
EMAIL_RECEPTOR = "correo@gestorianogales.com"

# --- DICCIONARIO DE PROVINCIAS ---
PROVINCIAS = {
    "ALAVA": "VI", "ALBACETE": "AB", "ALICANTE": "A", "ALMERIA": "AL", "ASTURIAS": "O", "AVILA": "AV",
    "BADAJOZ": "BA", "BALEARES": "PM", "BARCELONA": "B", "BURGOS": "BU", "CACERES": "CC", "CADIZ": "CA",
    "CANTABRIA": "S", "CASTELLON": "CS", "CIUDAD REAL": "CR", "CORDOBA": "CO", "CORUÑA": "C", "CUENCA": "CU",
    "GIRONA": "GI", "GRANADA": "GR", "GUADALAJARA": "GU", "GUIPUZCOA": "SS", "HUELVA": "H", "HUESCA": "HU",
    "JAEN": "J", "LEON": "LE", "LLEIDA": "L", "LUGO": "LU", "MADRID": "M", "MALAGA": "MA", "MURCIA": "MU",
    "NAVARRA": "NA", "OURENSE": "OU", "PALENCIA": "P", "PONTEVEDRA": "PO", "LA RIOJA": "LO", "SALAMANCA": "SA",
    "SEGOVIA": "SG", "SEVILLA": "SE", "SORIA": "SO", "TARRAGONA": "T", "TERUEL": "TE", "TOLEDO": "TO",
    "VALENCIA": "V", "VALLADOLID": "VA", "VIZCAYA": "BI", "ZAMORA": "ZA", "ZARAGOZA": "Z", "CEUTA": "CE", "MELILLA": "ML"
}

def enviar_email(archivo_nombre, contenido_xml):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EMISOR
    msg['To'] = EMAIL_RECEPTOR
    msg['Subject'] = Header(f"Nuevo Justificante GA - {archivo_nombre}", 'utf-8')
    part = MIMEBase('application', "octet-stream")
    part.set_payload(contenido_xml.encode('utf-8'))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{archivo_nombre}"')
    msg.attach(part)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_EMISOR, EMAIL_PASSWORD)
        server.sendmail(EMAIL_EMISOR, EMAIL_RECEPTOR, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error al enviar el email: {e}")
        return False

# --- APP ---
st.set_page_config(page_title="Gestoría Nogales", page_icon="📄")
st.title("📄 PROVISIONALES GESTORIA NOGALES")

with st.form("formulario_ga", clear_on_submit=False):
    st.subheader("1. Identificación")
    doc = st.text_input("NIF / CIF / NIE").upper().replace(" ", "").replace("-", "")
    
    nombre, ape1, ape2, razon_social, tipo_sujeto = "", "", "", "", None

    if doc:
        if re.match(r"^[0-9XYZ][0-9]{7}[A-Z]$", doc):
            tipo_sujeto = "PERSONA"
            st.success("Detección: Persona Física")
            nombre = st.text_input("Nombre").upper()
            ape1 = st.text_input("Primer Apellido").upper()
            ape2 = st.text_input("Segundo Apellido").upper()
        elif re.match(r"^[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]$", doc):
            tipo_sujeto = "EMPRESA"
            st.success("Detección: Empresa")
            razon_social = st.text_input("Razón Social").upper()
        else:
            st.warning("Formato de documento no reconocido")

    st.subheader("2. Dirección")
    calle = st.text_input("Calle / Vía").upper()
    num_dir = st.text_input("Número")
    municipio = st.text_input("Municipio").upper()
    prov_input = st.selectbox("Provincia", list(PROVINCIAS.keys()))
    cp = st.text_input("Código Postal (5 dígitos)")

    st.subheader("3. Vehículo")
    matricula = st.text_input("Matrícula").upper().replace(" ", "")
    bastidor_completo = st.text_input("Bastidor (4 últimos dígitos opcional)")
    marca = st.text_input("Marca").upper()
    modelo = st.text_input("Modelo").upper()

    enviado = st.form_submit_button("Generar y Enviar")

    if enviado:
        if not doc or not calle or not num_dir or not municipio or not cp or not matricula or not marca or not modelo:
            st.error("Por favor, rellena todos los campos.")
        elif len(cp) != 5 or not cp.isdigit():
            st.error("El Código Postal debe tener 5 números.")
        elif not tipo_sujeto or (tipo_sujeto == "PERSONA" and (not nombre or not ape1)) or (tipo_sujeto == "EMPRESA" and not razon_social):
            st.error("Datos de identidad incompletos.")
        else:
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
            <FORMATO_GA>
                <JUSTIFICANTE>
                    <JEFATURA>BA</JEFATURA>
                    <SUCURSAL/>
                    <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
                    <FECHA_PRESENTACION>{datetime.now().strftime("%d/%m/%Y")}</FECHA_PRESENTACION>
                    <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
                    <DIAS_VALIDEZ>30</DIAS_VALIDEZ>
                    <DOCUMENTOS>CAMBIO TITULAR</DOCUMENTOS>
                    <TIPO_TRAMITE>TRANSFERENCIA</TIPO_TRAMITE>
                    <MOTIVO>OTROS</MOTIVO>
                    <DATOS_ADQUIRENTE>
                        <SEXO_ADQUIRENTE/>
                        <RAZON_SOCIAL_ADQUIRENTE>{razon_social}</RAZON_SOCIAL_ADQUIRENTE>
                        <NOMBRE_ADQUIRENTE>{nombre}</NOMBRE_ADQUIRENTE>
                        <APELLIDO1_ADQUIRENTE>{ape1}</APELLIDO1_ADQUIRENTE>
                        <APELLIDO2_ADQUIRENTE>{ape2}</APELLIDO2_ADQUIRENTE>
                        <DNI_ADQUIRENTE>{doc}</DNI_ADQUIRENTE>
                        <SIGLAS_DIRECCION_ADQUIRENTE>6</SIGLAS_DIRECCION_ADQUIRENTE>
                        <NOMBRE_VIA_DIRECCION_ADQUIRENTE>{calle}</NOMBRE_VIA_DIRECCION_ADQUIRENTE>
                        <NUMERO_DIRECCION_ADQUIRENTE>{num_dir}</NUMERO_DIRECCION_ADQUIRENTE>
                        <MUNICIPIO_ADQUIRENTE>{municipio}</MUNICIPIO_ADQUIRENTE>
                        <PROVINCIA_ADQUIRENTE>{PROVINCIAS[prov_input]}</PROVINCIA_ADQUIRENTE>
                        <CP_ADQUIRENTE>{cp}</CP_ADQUIRENTE>
                        <MUNICIPIO_ADQUIRENTE_INE>06044</MUNICIPIO_ADQUIRENTE_INE>
                    </DATOS_ADQUIRENTE>
                    <DATOS_VEHICULO>
                        <MATRICULA>{matricula}</MATRICULA>
                        <NUMERO_BASTIDOR>{bastidor_completo[-4:] if bastidor_completo else ""}</NUMERO_BASTIDOR>
                        <MARCA>{marca}</MARCA>
                        <MODELO>{modelo}</MODELO>
                    </DATOS_VEHICULO>
                </JUSTIFICANTE>
            </FORMATO_GA>"""
            
            if enviar_email(f"justificante_{matricula}.ga.xml", xml_content):
                st.success("✅ ¡Enviado correctamente!")
