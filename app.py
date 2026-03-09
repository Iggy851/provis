import streamlit as st
import xml.etree.ElementTree as ET
import io

st.title("🔄 LIMPIADOR DE XML DGT")

uploaded_file = st.file_uploader("Sube un XML de referencia (funcional)", type="xml")

if uploaded_file:
    tree = ET.parse(uploaded_file)
    root = tree.getroot()
    
    st.subheader("Datos del Titular a modificar")
    nif = st.text_input("NIF/NIE/CIF")
    nombre = st.text_input("Nombre")
    ape1 = st.text_input("1er Apellido")
    ape2 = st.text_input("2do Apellido")
    bastidor = st.text_input("Nuevo Bastidor")

    if st.button("Generar XML Limpio"):
        # Modificar datos en el XML
        titular = root.find(".//DATOS_TITULAR")
        if titular is not None:
            titular.find("DNI_TITULAR").text = nif
            titular.find("NOMBRE_TITULAR").text = nombre
            titular.find("APELLIDO1_TITULAR").text = ape1
            titular.find("APELLIDO2_TITULAR").text = ape2
            
        # Modificar bastidor
        vehiculo = root.find(".//DATOS_VEHICULO")
        if vehiculo is not None:
            vehiculo.find("NUMERO_BASTIDOR").text = bastidor

        # Convertir a string
        xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode()
        
        st.download_button("Descargar XML Modificado", xml_str, "archivo_limpio.ga.xml", "text/xml")
