import sqlite3
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
from streamlit import date_input
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_resumida
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_fet
from altres.funcions import lletra_variable
from altres.funcions import rellotge
from altres.funcions import banner
from altres.funcions import separador
from altres.variables import cami_db
import emoji
import sqlitecloud

st.set_page_config(layout="wide")


# Conectarse a la base de datos
conn = sqlite3.connect(cami_db)
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________
rellotge()

#___________________________________________________________________________________
banner()
#_________________________________________________________________________________________
conn = sqlite3.connect(cami_db)
cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"

cursor.execute(query)
num_registres = cursor.fetchone()[0]


#_______________________________________________________
# Afegir text dins d'un marc amb l'estil definit
text_personalitzat = f"Portem {num_registres} receptes acumulades"

st.write("")
st.subheader(f"{text_personalitzat}")
conn.commit()

#______________________________________________________________

query = f'SELECT ID_Recepte, Titol FROM Receptes;'

cursor.execute(query)
registres = cursor.fetchall()

# Obtenir els tres últims registres utilitzant slicing
ultims_registres = registres[-3:]

separador()

st.subheader("Aquestes son les ultimes 3")

for i, registre in enumerate(ultims_registres, start=1):
    data = {
        'ID_Recepte': registre[0],
        'Titol': registre[1],
    }
    card_html = crear_tarjeta_html_resumida(data)
    st.markdown(card_html, unsafe_allow_html=True)
