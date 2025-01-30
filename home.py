import os
import sys
import base64
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import sqlite3


sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"

cursor.execute(query)
num_registres = cursor.fetchone()[0]

cursor.execute(query)
result = cursor.fetchone()

# Mostra el resultat dins d'un quadrat gran amb estil CSS ajustat
st.markdown(f'''
    <div style="display: flex; justify-content: center; align-items: center; height: 300px; width: 300px; border: 5px solid black; position: absolute; left: 20px;">
        <h1 style="font-size: 175px;">{result[0]}</h1>
    </div>
''', unsafe_allow_html=True)
conn.commit()


#_____________________________

# URL de la imatge de fons
background_image_url= "https://cuidateplus.marca.com/sites/default/files/styles/natural/public/cms/platanos_0.jpg.webp?itok"

# CSS personalitzat per posar la imatge de fons
background_css = f"""
<style>
.stApp {{
    background: url("{background_image_url}") no-repeat center center;
    background-size: 70%;
    height: 100vh;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    position: relative;
}}
.title-container {{
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    height: 100vh;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    padding: 1em;
}}
.title {{
    color: white;
    font-size: 3em;
    text-align: right;
    background: rgba(0, 0, 0, 0.5);
    padding: 0.5em;
    border-radius: 0.5em;
}}
.custom-text {{
    position: fixed;
    bottom: 200px;
    right: 200px;
    font-size: 100px; /* Augmenta la mida de la font */
    font-weight: bold;
    color: #003366; /* Pots canviar el color segons les teves necessitats */
    background-color: transparent; 
    padding: 10px;
    border: 2px solid #003366;
    border-radius: 15px; /* Bordes arrodonits */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Afegir una mica d'ombra per a millorar la visibilitat */
}}
</style>
"""

# Aplica el CSS utilitzant st.markdown
st.markdown(background_css, unsafe_allow_html=True)



# Afegir text personalitzat a l'extrem inferior dret
st.markdown('<div class="custom-text">Les Receptes de la Mamen</div>', unsafe_allow_html=True)


# _________________________________________________________________________

