import streamlit as st
import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

conn.commit()

# Función para obtener la lista de ingredientes
def obtener_ingredientes():
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

# Función para obtener recetas con los ingredientes seleccionados
def obtener_recetas(ingredients_seleccionats):
    placeholders = ', '.join(['?']*len(ingredients_seleccionats))
    query = f"""
    SELECT Receptes.Titol, Receptes.Data_formatejada, Receptes.ID_Recepte
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
            Titol, Data_formatejada, ID_Recepte = recepte
            st.markdown(f"### {Titol}")
            st.write(f"**Fecha de Publicación:** {Data_formatejada}")
            st.write(f"**ID de la Receta:** {ID_Recepte}")
    else:
        st.write("No se encontraron recetas con los ingredientes seleccionados.")
else:
    st.write("Selecciona uno o más ingredientes para ver las recetas.")


