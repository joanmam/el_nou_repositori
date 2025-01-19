import sqlite3
import streamlit as st
import base64
import pandas as pd
from visualizar import create_card, get_image_base64

# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

conn.commit()


# Función para obtener la lista de ingredientes
def obtener_ingredientes():
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

llista_ingredients = obtener_ingredientes()

# Obtener lista de recetas e ingredientes
categoria = st.multiselect('Categoria', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
temps_prep = st.slider('Preparacio', 0, 240, (0, 240), step=1)
ingredients_seleccionats = st.multiselect('Selecciona los ingredientes:', llista_ingredients)

# Generar la consulta dinámica
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, Receptes.Categoria, Receptes.Preparacio, GROUP_CONCAT(ingredients.nom, ', ') as ingredients, Receptes.blob
    FROM Receptes
    LEFT JOIN ingredients ON Receptes.ID_Recepte = ingredients.ID_Recepte'''

params = []
conditions = []

if 'Tots' not in categoria:
    conditions.append("Receptes.Categoria IN ({})".format(', '.join('?' * len(categoria))))
    params.extend(categoria)

if temps_prep != (0, 240):
    conditions.append("Receptes.Preparacio BETWEEN ? AND ?")
    params.extend([temps_prep[0], temps_prep[1]])

if ingredients_seleccionats:
    ingredient_conditions = []
    for ing in ingredients_seleccionats:
        ingredient_conditions.append("ingredients.nom LIKE ?")
        params.append(f'%{ing}%')
    conditions.append("(" + " OR ".join(ingredient_conditions) + ")")

if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += " GROUP BY Receptes.ID_Recepte"

cursor.execute(query, params)
resultados = cursor.fetchall()

# Interfaz de usuario con Streamlit
st.title('Filtro de Recetas por Ingredientes')

# Selección de ingredientes
# llista_ingredients = obtener_ingredientes()

#Mostrar recetas
if resultados:
    for row in resultados:
        try:
            img_base64 = get_image_base64(row['blob'])  # Suponiendo que el blob está en la columna 7
            tarjeta = create_card(row['ID_Recepte'], row['Data_formatejada'], row['Titol'], img_base64, row['Metode'])
            st.markdown(tarjeta, unsafe_allow_html=True)
        except KeyError:
            st.write(f"Error: los datos de la receta no están completos. Faltante: {e}")
else:
    st.write('No se encontraron resultados con los filtros seleccionados.')
