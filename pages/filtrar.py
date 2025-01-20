import sqlite3
import streamlit as st
import base64
import pandas as pd
from visualizar import create_card, get_image_base64
import streamlit.components.v1 as components
from datetime import datetime

# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

conn.commit()


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


# Interfaz de usuario con Streamlit
st.title('Filtro de Recetas por Ingredientes')

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
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, GROUP_CONCAT(ingredients.nom, ', ') as ingredients
    FROM Receptes
    LEFT JOIN ingredients
    ON Receptes.ID_Recepte = ingredients.ID_Recepte'''

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
