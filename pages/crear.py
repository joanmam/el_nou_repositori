import sqlite3
import streamlit as st
from datetime import datetime
from io import BytesIO, StringIO
from PIL import Image
import pandas as pd
import base64
import io
import requests
st.set_page_config(layout="wide")
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
             Etiquetes TEXT,
             Categoria TEXT,
             Preparacio TEXT,
             Temps TEXT)''')

# Crear una tabla para los ingredientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    ID_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    quantitat TEXT NOT NULL,
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
    Categoria = st.selectbox("Seleciona", ["Cat1","Cat2", "Cat3"])
    Temps = st.text_input("Temps")
    Preparacio = st.text_input("Preparacio")
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
            sql = ("INSERT INTO Receptes (Data_formatejada, Titol, Descripcio, Etiquetes, blob, Temps, Preparacio, Categoria)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            datos = Data_formatejada, Titol, Descripcio, Etiquetes, blob, Temps, Preparacio, Categoria
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
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input('Nombre del ingrediente')
        añadir_ingrediente = st.form_submit_button("Añadir ingrediente")
    with col2:
        quantitat = st.text_input('Cantidad')
        finalizar = st.form_submit_button("Finalizar")


    if añadir_ingrediente:
        if nom and quantitat:
            st.session_state.ingredientes.append((nom, quantitat))
        else:
            st.error("please")

    if finalizar:
        if st.session_state.ultimo_id is not None:
            for nom, quantitat in st.session_state.ingredientes:
                cursor.execute('INSERT INTO ingredients (nom, quantitat, ID_Recepte) VALUES (?, ?, ?)',
                           (nom, quantitat, st.session_state.ultimo_id))
            conn.commit()
            st.success('Todos los ingredientes han sido guardados con éxito!')
            st.session_state.ingredientes = []
        else:
            st.error("Primero debe guardar una receta")

if st.session_state.ingredientes:
    st.write("Ingredientes añadidos:")
    for idx, (nom, quantitat) in enumerate(st.session_state.ingredientes, start=1):
        st.write(f'{idx}. Ingrediente: {nom}, Cantidad: {quantitat}')

# Cerrar la conexión
conn.close()
