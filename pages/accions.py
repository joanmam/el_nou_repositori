import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
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

st.set_page_config(layout="wide")



# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________
rellotge()

#___________________________________________________________________________________
banner()
#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

#__________________________________________________________
accio = "Fet"
data_accio = datetime.now().strftime('%d-%m-%Y %H:%M:%S')




# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres:</p>', unsafe_allow_html=True)
ids_to_action = st.text_input("", "1")


st.write(f"El registre fet es: {ids_to_action}")

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
    if st.button('fet'):
        cursor.execute('INSERT INTO Accions (ID_Recepte, Data_accio) VALUES (?, ?)', (record_to_show[0], data_accio))
        conn.commit()
        st.write("Accion registrada")
else:
    st.write("EL registro no esta")





    # Comprovar si els registres relacionats s'han esborrat de la taula ingredients
# cursor.execute('SELECT * FROM Accions WHERE ID_Recepte = ?'
# remaining_records = cursor.fetchall()
# if not remaining_records:
#     st.success("Els registres relacionats s'han esborrat correctament.")
# else:
#     st.error("Els registres relacionats NO s'han esborrat.")

# Tancar la connexió
conn.close()