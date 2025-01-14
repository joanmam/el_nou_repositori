import sqlite3
import streamlit as st

# Conectar a la base de datos (crear si no existe)
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Crear una tabla para los ingredientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    IDingredient INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    quantitat TEXT NOT NULL,
    IDRecepte INTEGER,
    FOREIGN KEY (IDRecepte) REFERENCES Receptes(id)
)
''')


# Función para insertar ingredientes en la base de datos
def agregar_component(nom, quantitat, IDRecepte):
    conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ingredients (nom, quantitat, IDRecepte) VALUES (?,?,?)', (nom, quantitat, IDRecepte))
    conn.commit()
    conn.close()

# Función para visualizar ingredientes
def mostrar_component():
    conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ingredients.nom, ingredients.quantitat, Receptes.Titol
        FROM ingredients
        JOIN Receptes ON ingredients.IDRecepte = Receptes.IDREcepte
    ''')
    components = cursor.fetchall()
    conn.close()
    return components


def obtener_ingredients_amb_receptes():
    conn = sqlite3.connect('receptes.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT ingredients.nom, ingredients.quantitat, Receptes.Titol
        FROM ingredients
        JOIN Receptes ON ingredients.IDRecepte = Receptes.IDREcepte
    ''')
    resultats = cur.fetchall()
    conn.close()
    return resultats


# Streamlit interface
st.title('Gestor de Ingredientes de Recetas')

nom = st.text_input('Nombre del ingrediente')
quantitat = st.text_input('Cantidad')
IDRecepte = st.number_input('ID de la Receta', min_value=1, step=1)

if st.button('Agregar Ingrediente'):
    agregar_component(nom, quantitat, IDRecepte)
    st.success('Ingrediente agregado con éxito!')

st.write('Lista de Ingredientes:')
components = mostrar_component()

for idx, component in enumerate(components, start=1):
    st.write(f'{idx}. Ingredient: {component[0]}, Quantitat: {component[1]}, Recepta: {component[2]}')



conn.commit()
conn.close()
