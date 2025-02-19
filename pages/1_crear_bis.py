import sqlitecloud
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO, StringIO
from PIL import Image
import pandas as pd
import base64
import io
import requests
from altres.funcions import rellotge
from altres.funcions import banner
from altres.variables import cami_db
from altres.variables import img_url
import emoji
import sqlitecloud
from altres.funcions import cropping

st.set_page_config(layout="wide")

rellotge()
#_______________________________
st.header("Grava una receta")

base64_image, cropped_image = cropping()
banner(base64_image)

#___________________________________________

# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

conn.commit()

ultimo_id = None
if 'ultimo_id' not in st.session_state:
    st.session_state.ultimo_id = None

st.subheader("Recepte")

with st.form(key="Form"):
    col1, col2 = st.columns(2)

    with col1:
        Data = st.date_input("Seleccionar data")

    with col2:
        Titol = st.text_input("Titol")

    st.markdown("---")  # Separador

    foto = st.file_uploader("Elige",type=["jpg","png"])
    st.markdown("---")  # Separador

    col3, col4 = st.columns(2)
    with col3:
        Categoria = st.selectbox("Selecciona", ["Cat1","Cat2", "Cat3"])
        st.markdown("---")  # Separador

    with col4:
        tags = st.text_input("Etiquetes")
        st.markdown("---")  # Separador

    Observacions = st.text_area("Observacions")
    st.markdown("---")  # Separador

    col5, col6 = st.columns(2)
    with col5:
        st.write("Temps de preparacio")
        Hores_prep = st.number_input("Hores", step=1, key="hores_preparacio")
        Minuts_prep = st.number_input("Minuts", step=1, key="minuts_preparacio")

    with col6:
        st.write("Temps total")
        Hores = st.number_input("Hores", step=1, key="hores_totals")
        Minuts = st.number_input("Minuts", step=1, key="minuts_totals")

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

            Temps = Hores * 60 + Minuts
            Preparacio = Hores_prep * 60 + Minuts_prep


            sql = ("INSERT INTO Receptes (Data_formatejada, Titol, Observacions, Etiquetes, blob, Temps, Preparacio, Categoria)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            datos = Data_formatejada, Titol, Observacions, Etiquetes, blob, Temps, Preparacio, Categoria
            cursor.execute(sql, datos)
            conn.commit()

            cursor.execute('''SELECT last_insert_rowid()''')
            st.session_state.ultimo_id = cursor.fetchone()[0]
            st.write(f'El último ID asignado en la tabla Receptes es: {st.session_state.ultimo_id}')


# Crear un formulario para los ingredientes
st.subheader("Ingredients")

# Lista para almacenar temporalmente los ingredientes
if 'ingredientes' not in st.session_state:
    st.session_state.ingredientes = []

# Estil CSS per personalitzar el botó "Finalizar"
st.markdown("""
    <style>
    st.button_Finalizar {
        background-color: red;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# Formulari per afegir ingredients
with st.form(key="Form2"):
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom de l'ingredient")
        submit_button1 = st.form_submit_button("Afegir ingredient")
    with col2:
        quantitat = st.text_input('Quantitat')


    if submit_button1:
        if nom and quantitat:
            st.session_state.ingredientes.append((nom, quantitat))
        else:
            st.error("Sisplau, ompli tots dos camps.")

# Mostrar ingredients afegits en una llista acumulativa
if st.session_state.ingredientes:
    st.write("Ingredients afegits temporalment:")
    for idx, (nom, quantitat) in enumerate(st.session_state.ingredientes, start=1):
        st.write(f"{idx}. Ingredient: {nom}, Quantitat: {quantitat}")

submit_button2 = st.button("Acabar")
if submit_button2:
    if 'ultimo_id' in st.session_state:
        # Inserir ingredients a la base de dades només quan es pressiona "Finalizar"
        for nom, quantitat in st.session_state.ingredientes:
            cursor.execute('INSERT INTO ingredients (nom, quantitat, ID_Recepte) VALUES (?, ?, ?)',
                           (nom, quantitat, st.session_state.ultimo_id))
            conn.commit()

        # Fer un SELECT per mostrar els ingredients de l'última recepta
        cursor.execute('SELECT nom, quantitat FROM ingredients WHERE ID_Recepte = ?', (st.session_state.ultimo_id,))
        ingredients = cursor.fetchall()

        st.write("Ingredients de l'última recepte guardada:")
        if ingredients:
            for idx, (nom, quantitat) in enumerate(ingredients, start=1):
                st.write(f"{idx}. Ingredient: {nom}, Quantitat: {quantitat}")

        st.success("Tots els ingredients s'han guardat amb exit!")
        st.session_state.ingredientes = []

    else:
        st.error("Primer ha de guardar una recepte.")


# Tancar la connexió
conn.close()