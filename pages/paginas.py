import streamlit as st
import os

# Llistat de fitxers al subdirectori 'pages'
pages = sorted([page for page in os.listdir("pages") if page.endswith(".py")])

# Crea un diccionari per mapear noms de fitxers a títols de pàgines
page_titles = {page.replace('.py', '').capitalize(): page for page in pages}

# Selecciona una pàgina
selected_page = st.sidebar.selectbox("Selecciona una pàgina", list(page_titles.keys()))


# Funció per carregar la pàgina seleccionada
def load_page(page):
    with open(os.path.join("pages", page), "r") as file:
        exec(file.read(), globals())


# Afegeix els enllaços de pàgines amb separadors al menú lateral
for i, page in enumerate(page_titles.keys()):
    if page == selected_page:
        st.sidebar.write(f"**{page}**")
    else:
        st.sidebar.write(page)

    if i < len(page_titles) - 1:  # No afegeix separador després de l'última pàgina
        st.sidebar.markdown("---")

# Carrega la pàgina seleccionada
load_page(page_titles[selected_page])
