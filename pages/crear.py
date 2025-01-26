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

st.title("Grava una receta")

#___________________________________________
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




# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Crear tabla de clientes con ID autoincremental

cursor.execute('''CREATE TABLE IF NOT EXISTS Receptes (
             ID_Recepte INTEGER PRIMARY KEY AUTOINCREMENT, 
             Data_formatejada TEXT, 
             Titol TEXT,
             Metode TEXT,
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
    FOREIGN KEY (ID_Recepte) ,REFERENCES Receptes(ID_Recepte) ON DELETE CASCADE
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
    Metode = st.text_area("Metode")
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
            sql = ("INSERT INTO Receptes (Data_formatejada, Titol, Metode, Etiquetes, blob, Temps, Preparacio, Categoria)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            datos = Data_formatejada, Titol, Metode, Etiquetes, blob, Temps, Preparacio, Categoria
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
        nom = st.text_input('Nombre del ingrediente')
        submit_button1 = st.form_submit_button("Añadir ingrediente")
    with col2:
        quantitat = st.text_input('Cantidad')


    if submit_button1:
        if nom and quantitat:
            st.session_state.ingredientes.append((nom, quantitat))
        else:
            st.error("Por favor, rellena ambos campos.")

# Mostrar ingredients afegits en una llista acumulativa
if st.session_state.ingredientes:
    st.write("Ingredientes añadidos temporalmente:")
    for idx, (nom, quantitat) in enumerate(st.session_state.ingredientes, start=1):
        st.write(f"{idx}. Ingrediente: {nom}, Cantidad: {quantitat}")

submit_button2 = st.button("Finalizar")
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

        st.write("Ingredientes de la última receta guardada:")
        if ingredients:
            for idx, (nom, quantitat) in enumerate(ingredients, start=1):
                st.write(f"{idx}. Ingrediente: {nom}, Cantidad: {quantitat}")

        st.success('Todos los ingredientes han sido guardados con éxito!')
        st.session_state.ingredientes = []

    else:
        st.error("Primero debe guardar una receta.")


# Tancar la connexió
conn.close()