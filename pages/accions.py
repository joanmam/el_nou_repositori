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

st.set_page_config(layout="wide")


# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________

rellotge()
st.header("Accions")
banner()

#___________________________________________________________________________________



#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

#__________________________________________________________
lletra_variable()
accio = "Fet"
today = date.today()
st.markdown('<div class="custom-element"><p class="custom-title">Data:</p>', unsafe_allow_html=True)
data_accio = st.date_input('', today)




# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres:</p>', unsafe_allow_html=True)
ids_to_action = st.text_input("", "1")


# Crear la cadena de placeholders per a la consulta
# placeholders = ', '.join(['?' for _ in ids_to_action])

# Mostrar informació dels registres seleccionats
query = 'SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?'
cursor.execute(query, ids_to_action)
record_to_show = cursor.fetchone()

if record_to_show is not None:
    data = {'ID_Recepte': record_to_show[0],
        'Titol': record_to_show[1],
        }
    card_html = crear_tarjeta_html_resumida(data)
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button('**Guardar la data**'):
        cursor.execute('INSERT INTO Accions (ID_Recepte, Accio, Data_accio) VALUES (?, ?, ?)', (record_to_show[0],accio, data_accio))
        conn.commit()
        st.write("Accion registrada")
else:
        st.write("**El registro no esta**")

st.markdown('---')



# Comprovar si els registres relacionats s'han esborrat de la taula ingredients
query = '''
SELECT Receptes.ID_Recepte, Receptes.Titol, Accions.Accio, Accions.Data_accio
FROM Receptes 
JOIN Accions ON Receptes.ID_Recepte = Accions.ID_Recepte
WHERE Receptes.ID_Recepte = ?;'''

cursor.execute(query,ids_to_action)
records = cursor.fetchall()

if st.button('**Resum**'):
    for record in records:
        data = {'ID_Recepte': record[0],
                'Titol': record[1],
                'Accio': record[2],
                'Data_accio': record[3]
    }
        card_html = crear_tarjeta_html_fet(data)
        st.markdown(card_html, unsafe_allow_html=True)


conn.close()