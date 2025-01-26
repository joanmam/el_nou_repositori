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
st.set_page_config(layout="wide")


# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Obtenir els IDs dels registres a esborrar
ids_to_delete = st.text_input("Introdueix els IDs dels registres a esborrar, separats per comes", "1,2,3")
ids_to_delete = [int(x) for x in ids_to_delete.split(",")]

st.write(f"Els registres seleccionats per esborrar són: {ids_to_delete}")

# Crear la cadena de placeholders per a la consulta
placeholders = ', '.join(['?' for _ in ids_to_delete])

# Mostrar informació dels registres seleccionats
query = f'SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte IN ({placeholders})'
cursor.execute(query, ids_to_delete)
records_to_show = cursor.fetchall()

if records_to_show:
    st.write("Registres seleccionats per esborrar:")
    for record in records_to_show:
        st.write(f"ID: {record[0]}, Nom: {record[1]}")
else:
    st.error("No s'ha trobat cap registre amb aquests IDs.")
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
