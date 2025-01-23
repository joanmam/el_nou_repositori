import streamlit as st
import sqlite3
import base64

# Connexió a la base de dades
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()


# Funció per obtenir la llista d'ingredients de la base de dades
def obtenir_ingredients():
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]


# Obtenir la llista d'ingredients
llista_ingredients = obtenir_ingredients()

# Widgets de Streamlit per obtenir les condicions
categoria = st.multiselect('Categoria', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
temps_prep = st.slider('Preparació', 0, 240, (0, 240), step=1)
ingredients_seleccionats = st.multiselect('Selecciona els ingredients:', llista_ingredients)

# Definir la consulta SQL amb els paràmetres necessaris
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, GROUP_CONCAT(ingredients.nom, ', ') as ingredients
    FROM Receptes
    LEFT JOIN ingredients
    ON Receptes.ID_Recepte = ingredients.ID_Recepte
'''

params = []
conditions = []

# Afegir condicions a la consulta SQL
if 'Tots' not in categoria:
    conditions.append("Receptes.Categoria IN ({})".format(', '.join('?' * len(categoria))))
    params.extend(categoria)

if temps_prep != (0, 240):
    conditions.append("Receptes.Preparació BETWEEN ? AND ?")
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

# Executar la consulta
cursor.execute(query, params)
resultados = cursor.fetchall()


# Funció per crear targetes amb taules HTML
def create_card(data):
    ID_Recepte = data['ID_Recepte']
    Data_formatejada = data['Data_formatejada']
    Titol = data['Titol']
    img_base64 = data['img_base64']
    Metode = data['Metode']

    html_card_template = f'''
    <div style="background-color:#ffffff; padding:10px; border-radius:5px; margin:10px; border:1px solid #ccc;">
        <!-- Taula amb dues columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>ID:</strong></td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ccc;">{ID_Recepte}</td>
            </tr>
            <tr>
                <td style="padding: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Data:</strong></td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ccc;">{Data_formatejada}</td>
            </tr>
        </table>
        <!-- Segona fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>{Titol}</strong>
        </div>
        <!-- Tercera fila: una columna amb imatge centrada -->
        <div style="text-align: center; padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <img src="data:image/jpeg;base64,{img_base64}" alt="Imatge" style="max-width: 100%; height: auto; border-radius: 5px;"/>
        </div>
        <!-- Quarta fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>{Metode}</strong>
        </div>
    </div>
    <!-- Separador -->
    <div style="width: 100%; height: 2px; background-color: #123456; margin: 20px 0;"></div>
    '''
    return html_card_template


# Mostrar targetes a Streamlit amb depuració
for row in resultados:
    data = {
        'ID_Recepte': row[0],
        'Data_formatejada': row[1],
        'Titol': row[2],
        'img_base64': base64.b64encode(row[6]).decode('utf-8') if isinstance(row[6], bytes) else "",
        'Metode': row[3]
    }
    card_html = create_card(data)
    st.markdown(card_html, unsafe_allow_html=True)

    # Depuració: Mostra els valors individuals per assegurar-se que es passen correctament
    st.write("ID_Recepte:", data['ID_Recepte'])
    st.write("Data_formatejada:", data['Data_formatejada'])
    st.write("Titol:", data['Titol'])
    st.write("Metode:", data['Metode'])
    st.write("img_base64:", data['img_base64'][:50])  # Mostra una part de la cadena base64 per confirmar

# Tancar la connexió a la base de dades
conn.close()


