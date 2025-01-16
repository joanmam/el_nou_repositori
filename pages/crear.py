import sqlite3
import streamlit as st
from datetime import datetime
from io import BytesIO, StringIO
from PIL import Image
import pandas as pd
import base64
import io
import requests

st.title("Post")
st.write("contenido")

# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Crear tabla de clientes con ID autoincremental

cursor.execute('''CREATE TABLE IF NOT EXISTS Receptes (
             ID_Recepte INTEGER PRIMARY KEY AUTOINCREMENT, 
             Data_formatejada TEXT, 
             Titol TEXT,
             Descripcio TEXT,
             blob BLOB,
             Etiquetes TEXT)''')

# Crear una tabla para los ingredientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    ID_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    quantitat TEXT NOT NULL,
    unitats TEXT NOT NULL,
    ID_Recepte INTEGER,
    FOREIGN KEY (ID_Recepte) REFERENCES Receptes(id)
)
''')
conn.commit()

ultimo_id = None
if 'ultimo_id' not in st.session_state:
    st.session_state.ultimo_id = None

with st.form(key="Form"):
    Data = st.date_input("seleccionar fecha")
    foto = st.file_uploader("elige",type=["jpg","png"])
    Titol = st.text_input("Titol")
    Descripcio = st.text_area("Descripcio")
    tags = st.text_area("Etiquetes")
    enviar = st.form_submit_button()
    if enviar:
        if foto is not None:
            foto_bytes = foto.read()
            img = Image.open(BytesIO(foto_bytes))
            st.image(img)
            buffer = BytesIO()
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(buffer, format="JPEG")
            blob = buffer.getvalue()
            Etiquetes = ', '.join([tag.strip() for tag in tags.split(',')])
            Data_formatejada = Data.strftime("%d-%m-%Y")
            sql = "INSERT INTO Receptes (Data_formatejada, Titol, Descripcio, Etiquetes, blob) VALUES (?, ?, ?, ?, ?)"
            datos = Data, Titol, Descripcio, Etiquetes, blob
            cursor.execute(sql, datos)
            conn.commit()

            cursor.execute('''SELECT last_insert_rowid()''')
            st.session_state.ultimo_id = cursor.fetchone()[0]
            st.write(f'El último ID asignado en la tabla Receptes es: {st.session_state.ultimo_id}')


# Crear un formulario para los ingredientes
st.write("Ingredientes")

# Lista para almacenar temporalmente los ingredientes
if 'ingredientes' not in st.session_state:
    st.session_state.ingredientes = []

# Formulario para añadir ingredientes
with st.form(key="Form2"):
    nom = st.text_input('Nombre del ingrediente')
    quantitat = st.text_input('Cantidad')
    unitats = st.text_input('Unitats')
    añadir_ingrediente = st.form_submit_button("Añadir ingrediente")
    finalizar = st.form_submit_button("Finalizar e Ingredientes")

    if añadir_ingrediente:
        if nom and quantitat and unitats:
            st.session_state.ingredientes.append((nom, quantitat, unitats))
        else:
            st.error("please")

    if finalizar:
        if st.session_state.ultimo_id is not None:
            for nom, quantitat, unitats in st.session_state.ingredientes:
                cursor.execute('INSERT INTO ingredients (nom, quantitat, unitats, ID_Recepte) VALUES (?, ?, ?, ?)',
                           (nom, quantitat, unitats, st.session_state.ultimo_id))
            conn.commit()
            st.success('Todos los ingredientes han sido guardados con éxito!')
            st.session_state.ingredientes = []
        else:
            st.error("Primero debe guardar una receta")

if st.session_state.ingredientes:
    st.write("Ingredientes añadidos:")
    for idx, (nom, quantitat, unitats) in enumerate(st.session_state.ingredientes, start=1):
        st.write(f'{idx}. Ingrediente: {nom}, Cantidad: {quantitat}, Unitats: {unitats}')

# Cerrar la conexión
conn.close()
