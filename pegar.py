import streamlit as st
from PIL import Image
import io
import sqlite3
from datetime import datetime

# Definir les funcions addicionals (lletra_variable, separador, add_pas, break_pas)
def lletra_variable():
    pass

def separador():
    st.write("---")

# Funcions per afegir i aturar els passos
def add_pas():
    st.session_state.num_passos += 1

def break_pas():
    st.session_state.break_loop = True

# Inicialitzar les variables de sessió per emmagatzemar el nombre de passos i l'estat del bucle
if 'num_passos' not in st.session_state:
    st.session_state.num_passos = 1
if 'break_loop' not in st.session_state:
    st.session_state.break_loop = False

# Inicialitzar llistes de sessió per emmagatzemar imatges i passos
if 'imatges' not in st.session_state:
    st.session_state.imatges = []
if 'passos' not in st.session_state:
    st.session_state.passos = []

# Connexió a la base de dades (ajusta la teva base de dades aquí)
conn = sqlite3.connect('receptes.db')
cursor = conn.cursor()

# Obtenir els IDs de la recepte per introduir els passos
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Recepte seleccionada:</p>', unsafe_allow_html=True)
recepte_seleccionada = st.number_input("", min_value=3, step=1)

st.write(f"La recepte seleccionada per afegir passos es la numero **{recepte_seleccionada}**")
separador()

# Llistes temporals per emmagatzemar les imatges i passos d'aquesta sessió
imatges_temp = []
passos_temp = []

for i in range(st.session_state.num_passos):
    if st.session_state.break_loop:
        break
    st.write("")
    st.write("")
    lletra_variable()
    st.markdown(f'<div class="custom-element"><p class="custom-title">Pas: {i+1}</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 7])

    with col1:
        lletra_variable()
        st.markdown('<div class="custom-element2"><p class="custom-title2">Imatge:</p>', unsafe_allow_html=True)
        image = st.file_uploader(f"Imatge {i + 1}", type=["jpg", "png"], key=f"image_{i}")

        if image is not None:
            imatges_temp.append(image)
        elif len(st.session_state.imatges) > i:
            imatges_temp.append(st.session_state.imatges[i])

    with col2:
        lletra_variable()
        st.markdown('<div class="custom-element2"><p class="custom-title2">Pas:</p>', unsafe_allow_html=True)
        pas = st.text_area(f"Pas {i + 1}", key=f"pas_{i}")

        if pas:
            passos_temp.append(pas)
        elif len(st.session_state.passos) > i:
            passos_temp.append(st.session_state.passos[i])

# Actualitzar les llistes de sessió amb les llistes temporals
st.session_state.imatges = imatges_temp
st.session_state.passos = passos_temp

separador()
col1, col2 = st.columns([1, 9])

with col1:
    st.button("Afegir Pas", on_click=add_pas, key="add_pas")
with col2:
    st.button("Aturar", on_click=break_pas, key="break_pas")

separador()

if st.button("Guardar", key="save_data"):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.write("Inici del procés de guardat")
    st.write(f"imatges: {st.session_state.imatges}")
    st.write(f"passos: {st.session_state.passos}")

    for i in range(len(st.session_state.imatges)):
        image = st.session_state.imatges[i]
        pas = st.session_state.passos[i]

        if image and pas:
            img = Image.open(image)
            buf = io.BytesIO()
            img.save(buf, format="png")
            imatge = buf.getvalue()

            st.write(f"Inserting: ID_Recepte={recepte_seleccionada}, Imatge_passos={imatge}, Pas={pas}, Data_passos={current_date}")

            cursor.execute('''
                INSERT INTO Passos (ID_Recepte, Data_passos, Imatge_passos, Pas) VALUES (?, ?, ?, ?)
            ''', (recepte_seleccionada, current_date, imatge, pas))

    conn.commit()
    st.success("Guardado")

    # Reiniciar les variables de sessió
    st.session_state.num_passos = 1
    st.session_state.break_loop = False
    st.session_state.imatges = []
    st.session_state.passos = []
