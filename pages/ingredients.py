import sqlite3
import streamlit as st

# # Conectar a la base de datos (crear si no existe)
# conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
# cursor = conn.cursor()
#
# # Crear una tabla para los ingredientes
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS ingredients (
#     ID_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
#     nom TEXT NOT NULL,
#     quantitat TEXT NOT NULL,
#     ID_Recepte INTEGER,
#     FOREIGN KEY (ID_Recepte) REFERENCES Receptes(id)
# )
# ''')
#
#
# # Función para insertar ingredientes en la base de datos
# def agregar_component(nom, quantitat, ID_Recepte):
#     conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO ingredients (nom, quantitat, ID_Recepte) VALUES (?,?,?)', (nom, quantitat, ID_Recepte))
#     conn.commit()
#     conn.close()
#
# # Función para visualizar ingredientes
# def mostrar_component():
#     conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT ingredients.nom, ingredients.quantitat, Receptes.Titol
#         FROM ingredients
#         JOIN Receptes ON ingredients.ID_Recepte = Receptes.ID_Recepte
#     ''')
#     components = cursor.fetchall()
#     conn.close()
#     return components
#
#
# def obtener_ingredients_amb_receptes():
#     conn = sqlite3.connect('receptes.db')
#     cur = conn.cursor()
#     cur.execute('''
#         SELECT ingredients.nom, ingredients.quantitat, Receptes.Titol
#         FROM ingredients
#         JOIN Receptes ON ingredients.ID_Recepte = Receptes.ID_Recepte
#     ''')
#     resultats = cur.fetchall()
#     conn.close()
#     return resultats
#
#
# # Streamlit interface
# st.title('Gestor de Ingredientes de Recetas')
#
# nom = st.text_input('Nombre del ingrediente')
# quantitat = st.text_input('Cantidad')
# ID_Recepte = st.number_input('ID de la Receta', min_value=1, step=1)
#
# if st.button('Agregar Ingrediente'):
#     agregar_component(nom, quantitat, ID_Recepte)
#     st.success('Ingrediente agregado con éxito!')
#
# st.write('Lista de Ingredientes:')
# components = mostrar_component()
#
# for idx, component in enumerate(components, start=1):
#     st.write(f'{idx}. Ingredient: {component[0]}, Quantitat: {component[1]}, Recepta: {component[2]}')
#
#
#
# conn.commit()
# conn.close()


import streamlit as st

# Conectar a la base de datos
conn = sqlite3.connect('recetas.db')
c = conn.cursor()



# Generar la consulta dinámica


query = "SELECT * FROM recetas"
params = []

if 'Tots' not in Categoria or Preparacio != (0, 240) or ingredients_seleccionats:
    query += " WHERE "
    conditions = []

    if 'Tots' not in categorias:
        conditions.append("Categoria IN ({})".format(', '.join('?' * len(Categoria))))
        params.extend(Categoria)

    if Preparacio != (0, 240):
        conditions.append("Preparacio BETWEEN ? AND ?")
        params.extend(Preparacio)

    if ingredients_seleccionats:
        conditions.append(" AND ".join(["ingredientes LIKE ?"] * len(ingredients_seleccionats)))
        params.extend(['%' + ing + '%' for ing in ingredients_seleccionats])

    query += " AND ".join(conditions)

c.execute(query, params)
resultados = c.fetchall()

# Mostrar los resultados en la aplicación de Streamlit
st.write('### Resultados de la búsqueda:')
for fila in resultados:
    st.write(f'Nombre: {fila[1]}, Categoría: {fila[2]}, Tiempo: {fila[3]} minutos, Ingredientes: {fila[4]}')
