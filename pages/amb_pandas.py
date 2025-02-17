import sqlitecloud
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from altres.funcions import agregar_estilos_css
from altres.funcions import crear_tarjeta_html
from altres.funcions import convert_blob_to_base64
from altres.funcions import obtenir_ingredients
from altres.funcions import rellotge
from altres.funcions import separador
from altres.funcions import banner
from altres.funcions import lletra_variable
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_resumida
from PIL import Image
import io
import base64
from altres.funcions import crear_tarjeta_html_pas
from altres.funcions import crear_tarjeta_html_protocol
from altres.funcions import convert_image_to_base64
from altres.funcions import create_thumbnail
from altres.funcions import convert_blob_to_image
from altres.funcions import crear_taula_encapcalat
from altres.funcions import crear_taula_passos_sense_encapcalat
from altres.variables import cami_db
import sqlitecloud
import html
import pandas as pd


st.set_page_config(layout="wide")


rellotge()
#___________________________________________________________________________________
st.header('Protocol')
#______________________________________________________________________________________
banner()
def row_style(row):
    return ['background-color: #f0f0f0' if row.name % 2 == 0 else 'background-color: #ffffff' for _ in row]

# Establir la connexió amb SQLite Cloud
conn = sqlitecloud.connect(cami_db)

# Selecciona la base de dades
db_name = "Mamen_Receptes.db"
conn.execute(f"USE DATABASE {db_name}")

# Llista d'ID de receptes disponibles per seleccionar




# Executa una consulta SQL i guarda els resultats en un DataFrame de Pandas

receptes_seleccionades = st.text_input("Selecciona els ID de les receptes:")

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[receptes_seleccionades])
    styled_df = df.style.apply(row_style, axis=1)

# Genera l'HTML i oculta l'índex utilitzant CSS
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;}.row1 {background-color: #ffffff;}')

# Mostra el DataFrame estilitzat utilitzant Streamlit
    st.write(styled_df.to_html(), unsafe_allow_html=True)



