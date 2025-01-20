import pandas as pd
import io
import requests
import sqlite3
import base64
import streamlit as st




conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()


# Función para convertir el BLOB a una imagen en base64
def get_image_base64(blob):
    return base64.b64encode(blob).decode('utf-8')





# Función para generar la tarjeta con los datos proporcionados
def create_card(ID_Recepte, Data_formatejada, Titol, img_base64, Metode):
    html_card_template = '''
    <div style="background-color:#f9f9f9;padding:10px;border-radius:5px;margin:10px;">
        <!-- Primera fila: dos columnas -->
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <div style="flex: 1; border-right: 1px solid #ccc; padding-right: 10px;"> <strong>ID:</strong> {} </div>
            <div style="flex: 1; padding-left: 10px;"> <strong>Data: <strong>{}</strong> </div>
        </div>
        <!-- Segunda fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;"> <strong>{}</strong>
        </div>
        <!-- Tercera fila: una columna con imagen centrada -->
        <div style="text-align: center; padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <img src="data:image/jpeg;base64,{}" alt="Imagen" style="max-width: 100%; height: auto; border-radius: 5px;"/>
        </div>
        <!-- Cuarta fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;"> <strong>{}</strong>
        </div>
    </div>
    <!-- Separador -->
    <div style="width: 100%; height: 2px; background-color: #123456; margin: 20px 0;"></div>
    '''
    return html_card_template.format(ID_Recepte, Data_formatejada, Titol, img_base64, Metode)



# # Aplicació(id_recepte, data_formatejada, titol, img_base64, descripcio)
# Explicación:n Streamlit
# st.title('Posts')
# # Crear las tarjetas
# for _, row in df.iterrows():
#     card_html = create_card(row)
#     st.markdown(card_html, unsafe_allow_html=True)

# Cerrar la conexión a la base de datos
conn.close()



