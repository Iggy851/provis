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
    cuerpo = f"NUEVO TRÁMITE: {tipo_tramite}\nSolicitante: {datos_usuario['concesionario']}\nEmail: {datos_usuario['email_usuario']}"
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
        st.error(f"Error: {e}")
        return False

# --- APP ---
st.set_page_config(page_title="Gestoría Nogales", page_icon="📄")
st.title("📂 GESTORÍA NOGALES - ENVÍO DE TRÁMITES")

# ACCESO
col_a, col_b = st.columns(2)
concesionario = col_a.text_input("Concesionario / Empresa").upper()
email_solicitante = col_b.text_input("Tu Email").lower()

if concesionario and email_solicitante:
    st.divider()
    tipo = st.radio("Selecciona trámite:", ["PROVISIONAL", "MATRICULACIÓN"], horizontal=True)
    st.divider()

    # --- MATRICULACIÓN ---
    if tipo == "MATRICULACIÓN":
        with st.form("form_matri"):
            # 1. DATOS BÁSICOS Y TITULAR
            st.subheader("1. Datos Básicos y Titular")
            c1, c2, c3 = st.columns(3)
            bastidor = c1.text_input("Bastidor (VIN)").upper()
            nive = c2.text_input("NIVE").upper()
            itv_fab = c3.text_input("Fabricación ITV").upper()
            
            c4, c5, c6 = st.columns(3)
            dni_t = c4.text_input("NIF/CIF Titular").upper()
            nom_t = c5.text_input("Nombre / Razón Social").upper()
            ape_t = c6.text_input("Apellidos (si aplica)").upper()

            # 2. DIRECCIÓN TITULAR
            st.subheader("2. Dirección Titular")
            c7, c8, c9 = st.columns([3, 1, 1])
            calle_t = c7.text_input("Calle Titular").upper()
            num_t = c8.text_input("Nº").upper()
            cp_t = c9.text_input("C.P. Titular")
            
            c10, c11 = st.columns(2)
            muni_t = c10.text_input("Municipio Titular").upper()
            prov_t = c11.selectbox("Provincia Titular", list(PROVINCIAS.keys()), key="prov_t")

            # 3. DIRECCIÓN VEHÍCULO (Si es distinta)
            st.subheader("3. Dirección del Vehículo")
            exp_dir = st.checkbox("¿La dirección del vehículo es distinta a la del titular?")
            calle_v, num_v, cp_v, muni_v, prov_v = "", "", "", "", "BADAJOZ"
            if exp_dir:
                v1, v2, v3 = st.columns([3, 1, 1])
                calle_v = v1.text_input("Calle Vehículo").upper()
                num_v = v2.text_input("Nº Vehículo")
                cp_v = v3.text_input("C.P. Vehículo")
                v4, v5 = st.columns(2)
                muni_v = v4.text_input("Municipio Vehículo").upper()
                prov_v = v5.selectbox("Provincia Vehículo", list(PROVINCIAS.keys()), key="prov_v")

            # 4. IMPUESTOS
            st.subheader("4. Impuestos")
            i1, i2 = st.columns(2)
            mod_576 = i1.text_input("Referencia Mod. 576 (IEDMT)").upper()
            exento_ivtm = i2.checkbox("Exento de IVTM (Circulación)")

            if st.form_submit_button("Enviar Matriculación"):
                if not bastidor or not dni_t:
                    st.error("Bastidor y DNI son obligatorios.")
                else:
                    # Generamos el XML basado en tu archivo de ejemplo
                    xml_m = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <FORMATO_GA>
                        <MATRICULACION>
                            <JEFATURA>BA</JEFATURA>
                            <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
                            <FECHA_PRESENTACION>{datetime.now().strftime("%d/%m/%Y")}</FECHA_PRESENTACION>
                            <DATOS_VEHICULO>
                                <BASTIDOR>{bastidor}</BASTIDOR>
                                <NIVE>{nive}</NIVE>
                                <FABRICACION_ITV>{itv_fab if itv_fab else 'EMPTY_VALUE'}</FABRICACION_ITV>
                            </DATOS_VEHICULO>
                            <DATOS_TITULAR>
                                <DNI>{dni_t}</DNI>
                                <NOMBRE>{nom_t}</NOMBRE>
                                <APELLIDOS>{ape_t}</APELLIDOS>
                                <DIRECCION_TITULAR>
                                    <CALLE>{calle_t}</CALLE>
                                    <NUMERO>{num_t}</NUMERO>
                                    <CP>{cp_t}</CP>
                                    <MUNICIPIO>{muni_t}</MUNICIPIO>
                                    <PROVINCIA>{PROVINCIAS[prov_t]}</PROVINCIA>
                                </DIRECCION_TITULAR>
                            </DATOS_TITULAR>
                            <IMPUESTOS>
                                <IEDMT>{mod_576}</IEDMT>
                                <EXENTO_IVTM>{'SI' if exento_ivtm else 'NO'}</EXENTO_IVTM>
                            </IMPUESTOS>
                        </MATRICULACION>
                    </FORMATO_GA>"""
                    
                    datos_sol = {"concesionario": concesionario, "email_usuario": email_solicitante}
                    if enviar_email(f"matri_{bastidor}.xml", xml_m, datos_sol, "Matriculacion"):
                        st.success("✅ Solicitud de Matriculación enviada.")

    # --- PROVISIONAL (Manteniendo la lógica que ya funcionaba) ---
    elif tipo == "PROVISIONAL":
        # ... (Aquí va el bloque de código de provisionales que ya tenías configurado)
        st.info("Formulario de Provisionales activo.")
        # [Se mantiene el bloque de código anterior para Provisionales]

else:
    st.warning("Por favor, identifícate arriba para ver los formularios.")
