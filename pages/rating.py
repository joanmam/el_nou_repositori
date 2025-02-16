import sqlitecloud
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from datetime import date
from io import BytesIO, StringIO
from PIL import Image
import pandas as pd
import base64
import io
import requests
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_resumida
from altres.funcions import lletra_variable
from altres.funcions import rellotge
from altres.funcions import banner
from altres.funcions import separador
from altres.variables import cami_db
import emoji
import sqlitecloud

st.set_page_config(layout="wide")



# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________
rellotge()
st.header("Valoracio")
banner()
#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

#__________________________________________________________
lletra_variable()

st.markdown('<div class="custom-element"><p class="custom-title">Registre per valorar:</p>', unsafe_allow_html=True)
id_to_update = st.number_input("", min_value=3, step=1)

# Mostrar informació dels registres seleccionats
registre = (id_to_update,)
st.write(f"El registre seleccionat per actualitzar és: {id_to_update}")

# Mostrar informació dels registres seleccionats
query = ('SELECT ID_Recepte, '
         'Titol, '
         'Metode, '
         'Etiquetes, '
         'Categoria, '
         'Preparacio, '
         'Temps '
         'FROM Receptes WHERE ID_Recepte = ?')

cursor.execute(query, registre)
record = cursor.fetchone()

data = {'ID_Recepte': record[0],
        'Titol': record[1],
        }
card_html = crear_tarjeta_html_resumida(data)
st.markdown(card_html, unsafe_allow_html=True)
separador()

accio = "fet"
today = date.today()


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="custom-element"><p class="custom-title">Accio:</p>', unsafe_allow_html=True)
    st.write(accio)

with col2:
    st.markdown('<div class="custom-element"><p class="custom-title">Rating:</p>', unsafe_allow_html=True)
    Rating = st.slider("", min_value=0, max_value=5, step=1)

with col3:
    st.markdown('<div class="custom-element"><p class="custom-title">Data:</p>',
                unsafe_allow_html=True)
    data_accio = st.date_input('', today)


st.markdown('<div class="custom-element"><p class="custom-title">Resenya:</p>', unsafe_allow_html=True)
Resenya = st.text_area("")

if st.button('Guardar'):
    cursor.execute('INSERT INTO Accions (ID_Recepte, Accio, Resenya, Rating, Data_accio) VALUES (?, ?, ?, ?, ?)',
               (record[0],accio, Rating, data_accio, Resenya))
    conn.commit()
    st.subheader("Valoracio actualitzada")
