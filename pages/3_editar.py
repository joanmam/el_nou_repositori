import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from altres.funcions import obtenir_emoji
from altres.funcions import agregar_estilos_css
from altres.funcions import crear_tarjeta_html
from altres.funcions import convert_blob_to_base64
from altres.funcions import obtenir_ingredients
from altres.funcions import rellotge
from altres.funcions import separador
from altres.funcions import banner
from altres.funcions import lletra_variable
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_resumida
from altres.variables import cami_db

st.set_page_config(layout="wide")

rellotge()
#___________________________________________________________________________________
st.header('Actualitzacio')
#______________________________________________________________________________________
banner()
#_____________________________________________________________________________
#connexio a la base de dades
conn = sqlite3.connect(cami_db)
cursor = conn.cursor()

# Obtenir els IDs dels registres a actualitzar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registre per actualitzar:</p>', unsafe_allow_html=True)
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

separador()

st.markdown('<div class="custom-element"><p class="custom-title">Titol actual:</p>', unsafe_allow_html=True)
new_Titol = st.text_input("", record[1])
st.markdown('<div class="custom-element"><p class="custom-title">Metode actual:</p>', unsafe_allow_html=True)
new_Metode =  st.text_area("", record[2])

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown('<div class="custom-element"><p class="custom-title">Etiquetes actual:</p>', unsafe_allow_html=True)
    new_Etiquetes = st.text_input("", record[3])

with col2:
    st.markdown('<div class="custom-element"><p class="custom-title">Categoria actual:</p>', unsafe_allow_html=True)
    new_Categoria = st.text_input("", record[4])

with col3:
    st.markdown('<div class="custom-element"><p class="custom-title">Preparacio actual:</p>', unsafe_allow_html=True)
    new_Preparacio = st.text_input("", record[5])

with col4:
    st.markdown('<div class="custom-element"><p class="custom-title">Temps actual:</p>', unsafe_allow_html=True)
    new_Temps = st.text_input("", record[6])



query = ('UPDATE Receptes SET '
         'Titol = ?, '
         'Metode = ?, '
         'Etiquetes = ?, '
         'Categoria = ?, '
         'Preparacio = ?, '
         'Temps = ? '
         'WHERE ID_Recepte = ?')


nous_valors = (new_Titol, new_Metode, new_Etiquetes, new_Categoria, new_Preparacio, new_Temps, id_to_update)

if st.button("Actualitzar"):
    cursor.execute(query, nous_valors)
    conn.commit()
    st.subheader("Registre actualitzat")
    # record = cursor.fetchone()

# if record:
#     data = {
#         'ID_Recepte': record[0],
#         'Titol': record[1],
#         'Metode': record[2],
#         'Etiquetes': record[3],
#         'Categoria': record[4],
#         'Preparacio': record[5],
#         'Temps': record[6]
#     }
#     card_html = crear_tarjeta_html_resumida(data)
#     st.markdown(card_html, unsafe_allow_html=True)
# else:
#     st.write("No s'han trobat registres amb aquest ID.")
