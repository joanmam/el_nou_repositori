import sqlite3
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
import emoji
import sqlitecloud
import html

st.set_page_config(layout="wide")


rellotge()
#___________________________________________________________________________________
st.header('Protocol')
#______________________________________________________________________________________
banner()

# Obtenir els IDs de la recepte per introduir els passos
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Recepte seleccionada:</p>', unsafe_allow_html=True)
recepte_seleccionada = st.number_input("", min_value=3, step=1)

st.write(f"La recepte seleccionada per afegir un protocol es la numero **{recepte_seleccionada}**")



# Connexió a la base de dades (ajusta la teva base de dades aquí)
conn = sqlite3.connect(cami_db)
cursor = conn.cursor()

# Consulta per obtenir el títol i l'ID de la recepta
query_encapcalat = ('SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?;')
cursor.execute(query_encapcalat, (recepte_seleccionada,))
encapcalat_record = cursor.fetchone()

if not encapcalat_record:
    st.error("No s'ha trobat el títol i l'ID de la recepta seleccionada.")
else:
    encapcalat = {
        'ID_Recepte': encapcalat_record[0],
        'Titol': encapcalat_record[1]
    }

    # Consulta per obtenir els passos de la recepta
    query_passos = ('SELECT Numero, Pas, Imatge_passos '
                    'FROM Passos '
                    'WHERE ID_Recepte = ?;')
    cursor.execute(query_passos, (recepte_seleccionada,))
    passos_records = cursor.fetchall()

    if not passos_records:
        st.error("No s'han trobat passos per a la recepta seleccionada.")
    else:
        passos = []

        for record in passos_records:
            imatge_blob = record[2]

            Imatge = convert_blob_to_image(imatge_blob)
            if Imatge is not None:
                thumbnail = create_thumbnail(Imatge)
                imatge_base64 = convert_image_to_base64(thumbnail)
            else:
                imatge_base64 = ""  # Valor buit en cas d'error

            passos.append({
                'Numero': record[0],
                'Pas': record[1],
                'Imatge': imatge_base64
            })


        # Genera el HTML de la taula d'encapçalament
        encapcalat_html = crear_taula_encapcalat(encapcalat)
        st.markdown(encapcalat_html, unsafe_allow_html=True)

        st.write("")
        st.write("Els passos son")


        # Genera el HTML de la taula dels passos sense encapçalament
        passos_html = crear_taula_passos_sense_encapcalat(passos)

        st.components.v1.html(passos_html, height=500)



