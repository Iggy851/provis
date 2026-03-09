import streamlit as st
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

def enviar_email(archivo_nombre, contenido_xml, datos_usuario, tipo_tramite):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EMISOR
    msg['To'] = EMAIL_RECEPTOR
    msg['Subject'] = Header(f"{tipo_tramite.upper()} - {archivo_nombre}", 'utf-8')
    
    cuerpo = f"""
    NUEVO TRÁMITE RECIBIDO: {tipo_tramite.upper()}
    
    DATOS DEL SOLICITANTE:
    --------------------------
    Concesionario/Empresa: {datos_usuario['concesionario']}
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

# --- APP ---
st.set_page_config(page_title="Gestoría Nogales - Trámites", page_icon="📄")
st.title("📂 ENVÍO DE DOCUMENTACIÓN - GESTORÍA NOGALES")

# --- BLOQUE DE ACCESO ---
st.subheader("Identificación del Solicitante")
col_acc1, col_acc2 = st.columns(2)
with col_acc1:
    concesionario_sel = st.text_input("Tu Concesionario / Empresa").upper()
with col_acc2:
    email_usuario = st.text_input("Tu Email de contacto").lower()

if concesionario_sel and email_usuario:
    st.divider()
    tipo_tramite = st.radio("¿Qué trámite deseas realizar?", ["PROVISIONAL (TRANSFERENCIA)", "SOLICITUD DE MATRICULACIÓN"], horizontal=True)
    st.divider()

    # --- LÓGICA 1: PROVISIONALES ---
    if tipo_tramite == "PROVISIONAL (TRANSFERENCIA)":
        doc = st.text_input("NIF / CIF / NIE del Adquirente").upper().replace(" ", "").replace("-", "")
        nombre, ape1, ape2, razon_social, tipo_sujeto = "", "", "", "", None

        if doc:
            if re.match(r"^[0-9XYZ][0-9]{7}[A-Z]$", doc):
                tipo_sujeto = "PERSONA"
                nombre = st.text_input("Nombre").upper()
                ape1 = st.text_input("Primer Apellido").upper()
                ape2 = st.text_input("Segundo Apellido").upper()
            elif re.match(r"^[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J]$", doc):
                tipo_sujeto = "EMPRESA"
                razon_social = st.text_input("Razón Social").upper()

        if (tipo_sujeto == "PERSONA" and nombre) or (tipo_sujeto == "EMPRESA" and razon_social):
            with st.form("form_provisional"):
                st.subheader("Datos de Dirección y Vehículo")
                calle = st.text_input("Calle / Vía").upper()
                num_dir = st.text_input("Nº")
                cp = st.text_input("C.P.")
                municipio = st.text_input("Municipio").upper()
                prov_input = st.selectbox("Provincia", list(PROVINCIAS.keys()))
                st.divider()
                matricula = st.text_input("Matrícula").upper()
                bastidor = st.text_input("Bastidor (4 últimos)").upper()
                marca = st.text_input("Marca").upper()
                modelo = st.text_input("Modelo").upper()

                if st.form_submit_button("Generar y Enviar Provisional"):
                    if not calle or not matricula:
                        st.error("Rellene los campos obligatorios.")
                    else:
                        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <FORMATO_GA>
                            <JUSTIFICANTE>
                                <JEFATURA>BA</JEFATURA>
                                <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
                                <FECHA_PRESENTACION>{datetime.now().strftime("%d/%m/%Y")}</FECHA_PRESENTACION>
                                <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
                                <DOCUMENTOS>CAMBIO TITULAR</DOCUMENTOS>
                                <MOTIVO>OTROS</MOTIVO>
                                <DATOS_ADQUIRENTE>
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
                                </DATOS_ADQUIRENTE>
                                <DATOS_VEHICULO>
                                    <MATRICULA>{matricula}</MATRICULA>
                                    <NUMERO_BASTIDOR>{bastidor}</NUMERO_BASTIDOR>
                                    <MARCA>{marca}</MARCA>
                                    <MODELO>{modelo}</MODELO>
                                </DATOS_VEHICULO>
                            </JUSTIFICANTE>
                        </FORMATO_GA>"""
                        datos_sol = {"concesionario": concesionario_sel, "email_usuario": email_usuario}
                        if enviar_email(f"prov_{matricula}.xml", xml_content, datos_sol, "Provisional"):
                            st.success("✅ Enviado correctamente.")

    # --- LÓGICA 2: MATRICULACIÓN ---
    elif tipo_tramite == "SOLICITUD DE MATRICULACIÓN":
        with st.form("form_matriculacion"):
            st.subheader("Datos de Matriculación")
            col1, col2 = st.columns(2)
            with col1:
                bastidor_m = st.text_input("Número de Bastidor").upper()
                itv_m = st.text_input("Fabricación ITV").upper()
                dni_t = st.text_input("DNI/CIF Titular").upper()
            with col2:
                nombre_t = st.text_input("Nombre/Razón Social Titular").upper()
                municipio_t = st.text_input("Municipio").upper()
                prov_t = st.selectbox("Provincia Titular", list(PROVINCIAS.keys()))

            if st.form_submit_button("Enviar Solicitud de Matriculación"):
                if not bastidor_m or not dni_t:
                    st.error("Faltan campos obligatorios.")
                else:
                    # Basado en el esquema matriculaciones_2026-03-09_13-38-18.ga.xml
                    xml_m = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <FORMATO_GA>
                        <MATRICULACION>
                            <JEFATURA>BA</JEFATURA>
                            <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
                            <FECHA_PRESENTACION>{datetime.now().strftime("%d/%m/%Y")}</FECHA_PRESENTACION>
                            <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
                            <DATOS_VEHICULO>
                                <FABRICACION_ITV>{itv_m if itv_m else 'EMPTY_VALUE'}</FABRICACION_ITV>
                                <BASTIDOR>{bastidor_m}</BASTIDOR>
                            </DATOS_VEHICULO>
                            <DATOS_TITULAR>
                                <DNI>{dni_t}</DNI>
                                <NOMBRE>{nombre_t}</NOMBRE>
                                <MUNICIPIO>{municipio_t}</MUNICIPIO>
                                <PROVINCIA>{PROVINCIAS[prov_t]}</PROVINCIA>
                            </DATOS_TITULAR>
                        </MATRICULACION>
                    </FORMATO_GA>"""
                    datos_sol = {"concesionario": concesionario_sel, "email_usuario": email_usuario}
                    if enviar_email(f"matri_{bastidor_m[-6:]}.xml", xml_m, datos_sol, "Matriculacion"):
                        st.success("✅ Matriculación enviada.")
else:
    st.warning("Identifícate para comenzar.")
