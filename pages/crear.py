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
             IDRecepte INTEGER PRIMARY KEY AUTOINCREMENT, 
             Data_formatejada TEXT, 
             Titol TEXT,
             Descripcio TEXT,
             blob BLOB,
             Etiquetes TEXT)''')


conn.commit()



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
            st.success(f"Se ha creado el post con el titulo: {Titol}")
