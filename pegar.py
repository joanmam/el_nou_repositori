import streamlit as st
import sqlite3

# Connexió a la base de dades
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

if 'ingredientes' not in st.session_state:
    st.session_state.ingredientes = []

# Estil CSS per personalitzar el botó "Finalizar"
st.markdown("""
    <style>
    .button_finalizar {
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
        finalizar_button = st.form_submit_button("Finalizar")

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

if finalizar_button:
    if 'ultimo_id' in st.session_state:
        # Inserir ingredients a la base de dades només quan es pressiona "Finalizar"
        for nom, quantitat in st.session_state.ingredientes:
            cursor.execute('INSERT INTO ingredients (nom, quantitat, ID_Recepte) VALUES (?, ?, ?)',
                           (nom, quantitat, st.session_state.ultimo_id))
            conn.commit()

        st.success('Todos los ingredientes han sido guardados con éxito!')
        st.session_state.ingredientes = []

        # Fer un SELECT per mostrar els ingredients de l'última recepta
        cursor.execute('SELECT nom, quantitat FROM ingredients WHERE ID_Recepte = ?', (st.session_state.ultimo_id,))
        ingredients = cursor.fetchall()

        st.write("Ingredientes de la última receta guardada:")
        if ingredients:
            for idx, (nom, quantitat) in enumerate(ingredients, start=1):
                st.write(f"{idx}. Ingrediente: {nom}, Cantidad: {quantitat}")
    else:
        st.error("Primero debe guardar una receta.")

# Tancar la connexió
conn.close()
