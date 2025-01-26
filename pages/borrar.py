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

record_id = int(st.number_input("ID del registre a borrar",min_value=1, step=1))

st.write(f"El registre seleccionat es el {record_id}")
st.write("Aquesta es la Recepte")
cursor.execute('SELECT * FROM Receptes WHERE ID_Recepte = ?', (record_id,))
record = cursor.fetchone()

st.write(f"ID: {record[0]}, Titol: {record[2]}, Data_formatejada: {record[1]}")

# Esborrar el registre seleccionat si existeix
if st.button("Esborrar"):
    if record:  # Comprovar que el registre existeix abans d'esborrar
        cursor.execute('DELETE FROM Receptes WHERE ID_Recepte = ?', (record_id,))
        conn.commit()
        st.success("Registre esborrat amb èxit!")

        # Comprovar si els registres relacionats s'han esborrat de la taula ingredients
        cursor.execute('SELECT * FROM ingredients WHERE ID_Recepte = ?', (record_id,))
        remaining_records = cursor.fetchall()
        if not remaining_records:
            st.write("Els registres relacionats s'han esborrat correctament.")
        else:
            st.write("Els registres relacionats NO s'han esborrat.")
    else:
        st.error("No s'ha trobat cap registre amb aquest ID. No es pot esborrar.")

# Tancar la connexió
conn.close()

