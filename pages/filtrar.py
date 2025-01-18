import sqlite3
import streamlit as st
import pandas as pd
from visualizar import create_card, get_image_base64

# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

conn.commit()

query = 'SELECT ID_Recepte, Data_formatejada, Titol, Descripcio, blob, Etiquetes FROM Receptes'
df = pd.read_sql_query(query, conn)

# Función para obtener la lista de ingredientes
def obtener_ingredientes():
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

# Función para obtener recetas con los ingredientes seleccionados
def obtener_recetas(ingredients_seleccionats):
    placeholders = ', '.join(['?']*len(ingredients_seleccionats))
    query = f"""
    SELECT Receptes.Titol, Receptes.Data_formatejada, Receptes.ID_Recepte, Receptes.Descripcio,
    Receptes.Etiquetes, Receptes.blob
    FROM Receptes
    JOIN ingredients ON Receptes.ID_Recepte = ingredients.ID_Recepte
    WHERE ingredients.nom IN ({placeholders})
    GROUP BY Receptes.Titol
    HAVING COUNT(DISTINCT ingredients.nom) = ?
    """
    cursor.execute(query, (*ingredients_seleccionats, len(ingredients_seleccionats)))
    return cursor.fetchall()

# Interfaz de usuario con Streamlit
st.title('Filtro de Recetas por Ingredientes')

# Obtener lista de ingredientes
llista_ingredients = obtener_ingredientes()

# Selección de ingredientes
ingredients_seleccionats = st.multiselect('Selecciona los ingredientes:', llista_ingredients)

# Mostrar recetas
if ingredients_seleccionats:
    receptes = obtener_recetas(ingredients_seleccionats)
    if receptes:
        st.write("Recetas encontradas:")
        for recepte in receptes:
            row = {
                'Titol': recepte[0],
                'Data_formatejada': recepte[1],
                'ID_Recepte': recepte[2],
                'Descripcio': recepte[3],
                'Etiquetes': recepte[4],
                'blob': recepte[5],
            }
            tarjeta = create_card(row)
            st.markdown(tarjeta, unsafe_allow_html=True)
else:
    st.write("Selecciona uno o más ingredientes para ver las recetas.")

