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
from email.mime.text import MIMEText

# --- CONFIGURACIÓN ---
EMAIL_EMISOR = st.secrets.get("EMAIL_EMISOR", "")
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", "")
EMAIL_RECEPTOR = "correo@gestorianogales.com"

CONCESIONARIOS = [
    "SELECCIONA TU CONCESIONARIO",
    "CONCESIONARIO CENTRO",
    "CONCESIONARIO NORTE",
    "CONCESIONARIO SUR",
    "MOTOR BADAJOZ",
    "VEHÍCULOS MÉRIDA",
    "OTROS"
]

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

def enviar_email(archivo_nombre, contenido_xml, datos_usuario):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EMISOR
    msg['To'] = EMAIL_RECEPTOR
    msg['Subject'] = Header(f"Nuevo Justificante GA - {archivo_nombre}", 'utf-8')
    
    cuerpo = f"""
    Se ha generado un nuevo justificante provisional.
    
    DATOS DEL SOLICITANTE:
    --------------------------
    Concesionario: {datos_usuario['concesionario']}
    Email de contacto: {datos_usuario['email_usuario']}
    Fecha/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    --------------------------
    """
    msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

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

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gestoría Nogales", page_icon="📄")
st.title("📄 PROVISIONALES GESTORIA NOGALES")

# --- ACCESO SOLICITANTE ---
st.subheader("Acceso Solicitante")
col1, col2 = st.columns(2)
with col1:
    concesionario_sel = st.selectbox("Tu Concesionario", CONCESIONARIOS)
with col2:
    email_usuario = st.text_input("Tu Email de contacto").lower()

if concesionario_sel != "SELECCIONA TU CONCESIONARIO" and email_usuario:
    st.divider()
    
    st.subheader("1. Identificación del Adquirente")
    doc = st.text_input("Introduce NIF / CIF / NIE y pulsa INTRO").upper().replace(" ", "").replace("-", "")

    nombre, ape1, ape2, razon_social, tipo_sujeto = "", "", "", "", None

    if doc:
        if re.match(r"^[0-9XYZ][0-9]{7}[A-Z]$", doc):
            tipo_sujeto = "PERSONA"
            st.info("Detectado: Persona Física / NIE")
            nombre = st.text_input("Nombre").upper()
            ape1 = st.text_input("Primer Apellido").upper()
            ape2 = st.text_input("Segundo Apellido").upper()
        elif re.match(r"^[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]$", doc):
            tipo_sujeto = "EMPRESA"
            st.info("Detectado: Empresa (CIF)")
            razon_social = st.text_input("Razón Social").upper()
        else:
            st.error("Formato de documento no válido.")

    if (tipo_sujeto == "PERSONA" and nombre) or (tipo_sujeto == "EMPRESA" and razon_social):
        with st.form("resto_formulario"):
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
                if not calle or not num_dir or not municipio or not cp or not matricula or not marca or not modelo:
                    st.error("Por favor, rellena todos los campos.")
                elif len(cp) != 5 or not cp.isdigit():
                    st.error("El Código Postal debe tener 5 números.")
                else:
                    datos_solicitante = {"concesionario": concesionario_sel, "email_usuario": email_usuario}
                    
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
                    
                    if enviar_email(f"justificante_{matricula}.ga.xml", xml_content, datos_solicitante):
                        st.success(f"✅ ¡Enviado! Concesionario: {concesionario_sel}")
else:
    st.warning("Por favor, identifica tu concesionario y email para empezar.")
