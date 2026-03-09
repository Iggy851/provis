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
    
    # --- SELECCIÓN DE TRÁMITE ---
    tipo_tramite = st.radio(
        "¿Qué trámite deseas realizar?",
        ["PROVISIONAL (TRANSFERENCIA)", "SOLICITUD DE MATRICULACIÓN"],
        horizontal=True
    )
    st.divider()

    # ==========================================
    # LÓGICA 1: PROVISIONALES (TRANSFERENCIA)
    # ==========================================
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
                c1, c2, c3 = st.columns([2, 1, 1])
                calle = c1.text_input("Calle").upper()
                num_dir = c2.text_input("Nº")
                cp = c3.text_input("C.P.")
                
                municipio = st.text_input("Municipio").upper()
                prov_input = st.selectbox("Provincia", list(PROVINCIAS.keys()))
                
                st.divider()
                matricula = st.text_input("Matrícula").upper()
                bastidor = st.text_input("Bastidor (4 últimos)").upper()
                marca = st.text_input("Marca").upper()
                modelo = st.text_input("Modelo").upper()

                if st.form_submit_button("Generar Provisional"):
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
                        st.success("✅ Provisional enviado correctamente.")

    # ==========================================
    # LÓGICA 2: MATRICULACIÓN (ESTRUCTURA NUEVA)
    # ==========================================
    elif tipo_tramite == "SOLICITUD DE MATRICULACIÓN":
        st.info("Formulario para nuevas matriculaciones. Rellena los datos técnicos.")
        with st.form("form_matriculacion"):
            st.subheader("Datos del Vehículo y Titular")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                bast_m = st.text_input("Bastidor Completo (VIN)").upper()
                nive_m = st.text_input("NIVE").upper()
                dni_m = st.text_input("DNI/CIF Titular").upper()
            with col_m2:
                nom_m = st.text_input("Nombre/Razón Social Titular").upper()
                marca_m = st.text_input("Marca").upper()
                mod_m = st.text_input("Modelo").upper()
            
            st.divider()
            st.subheader("Impuestos")
            iedmt = st.text_input("Referencia IEDMT (Mod 576)").upper()
            ivtm_ex = st.checkbox("Exento de IVTM (Impuesto Circulación)")
            
            if st.form_submit_button("Enviar Matriculación"):
                # Aquí generamos el XML con la estructura de matriculación
                xml_m = f"""<?xml version="1.0" encoding="UTF-8"?>
                <MATRICULACION>
                    <BASTIDOR>{bast_m}</BASTIDOR>
                    <NIVE>{nive_m}</NIVE>
                    <TITULAR>{nom_m} ({dni_m})</TITULAR>
                    <MARCA>{marca_m}</MARCA>
                    <IEDMT>{iedmt}</IEDMT>
                    <EXENTO_IVTM>{ivtm_ex}</EXENTO_IVTM>
                </MATRICULACION>"""
                
                datos_sol = {"concesionario": concesionario_sel, "email_usuario": email_usuario}
                if enviar_email(f"matri_{bast_m[-6:]}.xml", xml_m, datos_sol, "Matriculacion"):
                    st.success("✅ Solicitud de Matriculación enviada.")

else:
    st.warning("Identifícate para acceder a la plataforma de documentación.")
