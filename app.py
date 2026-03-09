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
    cuerpo = f"Nuevo trámite de {tipo_tramite}\nSolicitante: {datos_usuario['concesionario']}\nEmail: {datos_usuario['email_usuario']}"
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
        st.error(f"Error al enviar: {e}")
        return False

# --- INTERFAZ ---
st.set_page_config(page_title="Gestoría Nogales", page_icon="📄")
st.title("📂 GESTORÍA NOGALES - PORTAL DE TRÁMITES")

# ACCESO
col_acc1, col_acc2 = st.columns(2)
conc_sol = col_acc1.text_input("Concesionario / Empresa").upper()
email_sol = col_acc2.text_input("Email de contacto").lower()

if conc_sol and email_sol:
    st.divider()
    opcion = st.radio("Seleccione el trámite:", ["MATRICULACIÓN", "PROVISIONAL"], horizontal=True)
    st.divider()

    if opcion == "MATRICULACIÓN":
        with st.form("form_matri_completo"):
            # 1. DATOS BÁSICOS
            st.subheader("1. Datos Básicos del Vehículo")
            c1, c2, c3 = st.columns(3)
            bastidor = c1.text_input("Bastidor (VIN)").upper()
            nive = c2.text_input("NIVE").upper()
            itv_fab = c3.text_input("Fabricación ITV").upper()

            # 2. TITULAR
            st.subheader("2. Datos del Titular")
            c4, c5 = st.columns(2)
            dni_t = c4.text_input("NIF / CIF Titular").upper().replace(" ", "")
            nom_t = c5.text_input("Nombre o Razón Social").upper()
            
            # 3. DIRECCIÓN TITULAR
            st.subheader("3. Dirección del Titular")
            c6, c7, c8 = st.columns([3, 1, 1])
            calle_t = c6.text_input("Calle / Vía Titular").upper()
            num_t = c7.text_input("Nº").upper()
            cp_t = c8.text_input("C.P.")
            c9, c10 = st.columns(2)
            muni_t = c9.text_input("Municipio Titular").upper()
            prov_t = c10.selectbox("Provincia Titular", list(PROVINCIAS.keys()), key="pt")

            # 4. DIRECCIÓN VEHÍCULO (Tutela fiscal)
            st.subheader("4. Dirección de Matriculación (Vehículo)")
            usa_misma = st.checkbox("Usar la misma dirección del titular", value=True)
            
            if not usa_misma:
                v1, v2, v3 = st.columns([3, 1, 1])
                calle_v = v1.text_input("Calle Vehículo").upper()
                num_v = v2.text_input("Nº Vehículo")
                cp_v = v3.text_input("C.P. Vehículo")
                v4, v5 = st.columns(2)
                muni_v = v4.text_input("Municipio Vehículo").upper()
                prov_v = v5.selectbox("Provincia Vehículo", list(PROVINCIAS.keys()), key="pv")
            else:
                calle_v, num_v, cp_v, muni_v, prov_v = calle_t, num_t, cp_t, muni_t, prov_t

            # 5. IMPUESTOS
            st.subheader("5. Impuestos")
            i1, i2 = st.columns(2)
            iedmt = i1.text_input("Referencia Mod. 576").upper()
            exento_ivtm = i2.selectbox("Exención IVTM", ["NO EXENTO", "EXENTO", "BONIFICADO"])

            if st.form_submit_button("Enviar Matriculación"):
                if not bastidor or not dni_t:
                    st.error("Bastidor y DNI son obligatorios.")
                else:
                    # Generamos XML con etiquetas estándar para evitar el error "Núm doc (1)"
                    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<FORMATO_GA>
    <MATRICULACION>
        <JEFATURA>BA</JEFATURA>
        <NUMERO_PROFESIONAL>00292</NUMERO_PROFESIONAL>
        <FECHA_PRESENTACION>{datetime.now().strftime("%d/%m/%Y")}</FECHA_PRESENTACION>
        <NUMERO_EXPEDIENTE>SIGA.{random.randint(1000000, 9999999)}</NUMERO_EXPEDIENTE>
        <DATOS_VEHICULO>
            <BASTIDOR>{bastidor}</BASTIDOR>
            <NIVE>{nive}</NIVE>
            <FABRICACION_ITV>{itv_fab if itv_fab else 'EMPTY_VALUE'}</FABRICACION_ITV>
            <DIRECCION_VEHICULO>
                <CALLE>{calle_v}</CALLE>
                <NUMERO>{num_v}</NUMERO>
                <CP>{cp_v}</CP>
                <MUNICIPIO>{muni_v}</MUNICIPIO>
                <PROVINCIA>{PROVINCIAS[prov_v]}</PROVINCIA>
            </DIRECCION_VEHICULO>
        </DATOS_VEHICULO>
        <DATOS_TITULAR>
            <DNI_TITULAR>{dni_t}</DNI_TITULAR>
            <NOMBRE_TITULAR>{nom_t}</NOMBRE_TITULAR>
            <DIRECCION_TITULAR>
                <CALLE>{calle_t}</CALLE>
                <NUMERO>{num_t}</NUMERO>
                <CP>{cp_t}</CP>
                <MUNICIPIO>{muni_t}</MUNICIPIO>
                <PROVINCIA>{PROVINCIAS[prov_t]}</PROVINCIA>
            </DIRECCION_TITULAR>
        </DATOS_TITULAR>
        <IMPUESTOS>
            <REFERENCIA_IEDMT>{iedmt}</REFERENCIA_IEDMT>
            <EXENTO_IVTM>{exento_ivtm}</EXENTO_IVTM>
        </IMPUESTOS>
    </MATRICULACION>
</FORMATO_GA>"""
                    datos_sol = {"concesionario": conc_sol, "email_usuario": email_sol}
                    if enviar_email(f"matri_{bastidor}.ga.xml", xml_content, datos_sol, "Matriculacion"):
                        st.success("✅ Matriculación enviada con éxito.")

    elif opcion == "PROVISIONAL":
        st.info("Complete los datos para el justificante provisional.")
        # Aquí se mantiene la estructura simple que ya tenías para provisionales
        with st.form("form_prov"):
            mat = st.text_input("Matrícula").upper()
            dni_p = st.text_input("DNI Adquirente").upper()
            if st.form_submit_button("Enviar Provisional"):
                st.success("Provisional enviado.")

else:
    st.warning("Introduzca sus datos de identificación para habilitar los formularios.")
