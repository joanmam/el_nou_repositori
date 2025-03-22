from altres.imports import *



st.set_page_config(layout="wide")




# Carregar Font Awesome
font_awesome()

#Comença la capçalera
# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)


# Mostrar resultats en diverses columnes
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    # Mostrar la imatge com a enllaç clicable
    # Mostrar el div estilitzat amb text
    st.markdown(
        f"""
        <a href="/crear" style="text-decoration: none;">
            <div style="border: 1px solid red; background-color: red; background: linear-gradient(90deg, red, yellow);
 border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: left;">
                Les Receptes de Mamen
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with col2:
    query = "SELECT * FROM Receptes"
    df = pd.read_sql(query, conn)
    count_total = df.shape[0]
    st.markdown(
        f'<div style="border: 1px solid red; border-radius: 20px; padding: 5px;"><i class="fas fa-bell"></i> {count_total}</div>',
        unsafe_allow_html=True)


with col3:
    st.markdown(
        f"""
    <a href="/crear" style="text-decoration: none;">
        <div style="border: 1px solid red; background-color: orange; border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white;">
        + Recepte
        </div>
    </a>   
    """,
    unsafe_allow_html=True)


separador()


conn = sqlitecloud.connect(cami_db)


# Botón para confirmar la entrada




# Configuració de la base de dades

import streamlit as st
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import sqlite3

# Configuració de la base de dades
conn = sqlitecloud.connect(cami_db)

# Inputs de Streamlit
pasted_text = st.text_input("URL")
font = st.text_input("Font")
meal = st.text_input("Meal")

if st.button("Enviar"):
    if pasted_text:
        # Fer una sol·licitud GET a la URL
        response = requests.get(pasted_text)

        # Comprovar si la sol·licitud ha tingut èxit
        if response.status_code == 200:
            html = response.text

            # Analitzar el contingut HTML amb BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # Extreure el títol
            title = soup.title.string if soup.title else "No se encontró un título"
            title2 = title.replace("Recipe", "").strip()
            st.success(f"Títol: {title2}")

            # Buscar la imatge
            blob = None
            image_tag = soup.find("img")  # Buscar la primera etiqueta img
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]
                if not image_url.startswith("http"):
                    # Assegura que l'URL sigui complet
                    image_url = requests.compat.urljoin(pasted_text, image_url)

                st.write(f"URL de la imatge: {image_url}")

                # Obtenir i mostrar la imatge
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    image = Image.open(BytesIO(img_response.content))
                    image.thumbnail((100, 100))  # Reduir la mida de la imatge
                    st.image(image)

                    # Convertir la imatge a blob binari
                    buffer = BytesIO()
                    image.save(buffer, format="JPEG")
                    blob = buffer.getvalue()

            # Crear el DataFrame
            df_insert = pd.DataFrame({
                "Titol": [title2],
                "Link": [pasted_text],
                "Foto": [blob],
                "Logo": [font],
                "Meal": [meal]
            })

            # Inserir registres a la base de dades
            records = df_insert.to_records(index=False).tolist()
            query_insert = "INSERT INTO Externs (Titol, Link, Foto, Logo, Meal) VALUES (?, ?, ?, ?, ?)"
            conn.executemany(query_insert, records)
            conn.commit()
            st.success("Guardat!")
        else:
            st.error(f"No s'ha pogut carregar la URL. Codi d'error: {response.status_code}")
