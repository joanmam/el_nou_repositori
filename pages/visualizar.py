import pandas as pd
import io
import requests
import sqlite3
import base64
import streamlit as st




conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()
query = 'SELECT ID_Recepte, Data_formatejada, Titol, Descripcio, blob, Etiquetes FROM Receptes'
df = pd.read_sql_query(query, conn)

# Función para convertir el BLOB a una imagen en base64
def get_image_base64(blob):
    return base64.b64encode(blob).decode('utf-8')



# Plantilla HTML para la tarjeta
html_card_template = """
<div style="background-color:#f9f9f9;padding:10px;border-radius:5px;margin:10px;">
    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        <div style="flex: 1; border-right: 1px solid #ccc; padding-right: 10px;"><strong>ID: </strong> {}</div>
        <div style="flex: 1; border-right: 1px solid #ccc; padding-right: 10px;"><strong> {}</div>
        <div style="flex: 1;">{}</div>
    </div>
    <div style="display: flex; justify-content: space-between; padding-top: 10px;">
        <div style="flex: 2; border-right: 1px solid #ccc; padding-right: 10px;"><strong>{}</div>
        <div style="flex: 1;"><strong>{}</div>
    </div>
    <div style="text-align: center; margin-top: 10px;">
        <img src="data:image/jpeg;base64,{}" alt="Imagen" style="max-width: 100%; height: auto; border-radius: 5px;"/>
    </div>
</div>
"""

def create_card(row):
    img_base64 = get_image_base64(row['blob'])
    return html_card_template.format(row['ID_Recepte'], row['Data_formatejada'], row['Descripcio'], row['Titol'], row['Etiquetes'], img_base64)

# Aplicación Streamlit
st.title('Posts')
# Crear las tarjetas
for _, row in df.iterrows():
    card_html = create_card(row)
    st.markdown(card_html, unsafe_allow_html=True)

# Cerrar la conexión a la base de datos
conn.close()