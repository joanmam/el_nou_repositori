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

st.set_page_config(layout="wide")



# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

conn.commit()


# Obtenir la data actual
current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# CSS per a posicionar la data a la cantonada superior dreta
date_css = """
<style>
.date-corner {
    position: fixed;
    top: 10px;
    right: 10px;
    font-size: 16px;
    background-color: rgba(125, 125, 255, 0.8);
    padding: 5px 10px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    z-index: 1000; /* Assegura que la data estigui al damunt de qualsevol contingut */
}
</style>
"""

# HTML per a mostrar la data amb l'estil definit
date_html = f"""
<div class="date-corner">
    {current_date}
</div>
"""

# Aplicar el CSS i HTML personalitzat a l'aplicació
components.html(date_css + date_html, height=100)
#___________________________________________________________________________________

# URL de la imatge
img_url = "https://imagenes.20minutos.es/files/image_990_556/uploads/imagenes/2024/05/07/pimientos.jpeg"  # Utilitza una imatge amb l'amplada de la pàgina (1920px) i l'alçada (113px)

# Injectar CSS per a la imatge de fons
background_css = f"""
<style>
body .custom-background {{
    background-image: url('{img_url}');
    background-size: 100% ;  /* Ajusta l'amplada al 100% i l'alçada a 113 píxels (3 cm) */
    background-repeat: no-repeat;
    background-position: top;
    margin: 0;
    padding: 0;
    height: 256px;  /* Assegura que l'alçada sigui la desitjada */
}}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Aplicar la classe CSS específica al contenidor principal
st.markdown('<div class="custom-background"></div>', unsafe_allow_html=True)

#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres a borrar separats per commes:</p>', unsafe_allow_html=True)
ids_to_delete = st.text_input("", "1,2,3")
ids_to_delete = [int(x) for x in ids_to_delete.split(",")]

st.write(f"Els registres seleccionats per esborrar són: {ids_to_delete}")

# Crear la cadena de placeholders per a la consulta
placeholders = ', '.join(['?' for _ in ids_to_delete])

# Mostrar informació dels registres seleccionats
query = f'SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte IN ({placeholders})'
cursor.execute(query, ids_to_delete)
records_to_show = cursor.fetchall()



for record in records_to_show:
    data = {
        'ID_Recepte': record[0],
        'Titol': record[1],
    }
    card_html = crear_tarjeta_html_resumida(data)
    st.markdown(card_html, unsafe_allow_html=True)


# Esborrar el registre seleccionat si existeix
if st.button("Esborrar"):
    for record_id in ids_to_delete:
        cursor.execute('DELETE FROM Receptes WHERE ID_Recepte = ?', (record_id,))
    conn.commit()


    # Comprovar si els registres relacionats s'han esborrat de la taula ingredients
    cursor.execute('SELECT * FROM ingredients WHERE ID_Recepte IN ({})'.format(','.join(['?'] * len(ids_to_delete))),
                   ids_to_delete)
    remaining_records = cursor.fetchall()
    if not remaining_records:
        st.success("Els registres relacionats s'han esborrat correctament.")
    else:
        st.error("Els registres relacionats NO s'han esborrat.")

# Tancar la connexió
conn.close()
