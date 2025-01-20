import streamlit as st

# URL de la imatge de fons
background_image_url = "https://cuidateplus.marca.com/sites/default/files/styles/natural/public/cms/platanos_0.jpg.webp?itok=HEwfKdcm"

# CSS personalitzat per posar la imatge de fons i centrar el títol perfectament
background_css = f"""
<style>
.stApp {{
    background: url("{background_image_url}") no-repeat center center;
    background-size: cover;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: relative;
    z-index: 1;
}}
.centered-title-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
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
st.write("Aquesta aplicació té una imatge de fons personalitzada.")


