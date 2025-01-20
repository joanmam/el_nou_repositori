import os
import sys
import base64
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime


sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))




# URL de la imatge de fons
background_image_url= "https://cuidateplus.marca.com/sites/default/files/styles/natural/public/cms/platanos_0.jpg.webp?itok"

# CSS personalitzat per posar la imatge de fons
background_css = f"""
<style>
.stApp {{
    background: url("{background_image_url}") no-repeat center center;
    background-size: 60%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: relative;
}}
.centered-title-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
}}
.centered-title {{
    color: white;
    font-size: 3em;
    text-align: center;
    background: rgba(0, 0, 0, 0.5);
    padding: 0.5em;
    border-radius: 0.5em;
}}
</style>
"""

# Aplicar el CSS personalitzat a l'aplicació utilitzant st.markdown
st.markdown(background_css, unsafe_allow_html=True)

# Contingut de l'aplicació
st.markdown("<div class='centered-title-container'><div class='centered-title'>Aplicació Streamlit amb Imatge de Fons</div></div>", unsafe_allow_html=True)



# _________________________________________________________________________
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

