import sqlite3
import streamlit as st
import base64
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO
from altres.funcions import obtenir_emoji
import re
import emoji
from altres.manteniment import emojis
from altres.funcions import redirigir_opcio


st.set_page_config(layout="wide")




# Conectarse a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
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
#___________________________________________________________________________________
st.header('Filtre de Receptes')

#______________________________________________________________________________________

# URL de la imatge
img_url = "https://imagenes.20minutos.es/files/image_990_556/uploads/imagenes/2024/05/07/pimientos.jpeg"  # Utilitza una imatge amb l'amplada de la pàgina (1920px) i l'alçada (113px)

# Injectar CSS per a la imatge de fons
background_css = f"""
<style>
body .custom-background {{
    background-image: url('{img_url}');
    background-size: 100% ;  /* Ajusta l'amplada al 100% i l'alçada a 113 píxels (3 cm) */
    background-repeat: no-repeat;
    background-position: top;
    margin: 0;
    padding: 0;
    height: 256px;  /* Assegura que l'alçada sigui la desitjada */
}}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Aplicar la classe CSS específica al contenidor principal
st.markdown('<div class="custom-background"></div>', unsafe_allow_html=True)

#_________________________________________________________________________________________
# Funció per convertir blob a base64
def convert_blob_to_base64(blob):
    if blob:
        return base64.b64encode(blob).decode('utf-8')
    return ''

#_____________________________________________________________________________

conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Funció per obtenir la llista d'ingredients de la base de dades
def obtenir_ingredients():
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

# Obtenir la llista d'ingredients
llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

# Widgets de Streamlit per obtenir les condicions
st.text("")
st.text("")


# CSS per canviar la mida de la lletra del nom de la variable
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 24px; /* Ajusta aquesta mida segons les teves necessitats */
        font-weight: bold;
        margin-bottom: 0.02em;
    }
    .slider-title {
        font-size: 24px; /* Ajusta aquesta mida segons les teves necessitats */
        font-weight: bold;
        margin-bottom: 0.2em; /* Utilitza una unitat més petita per ajustar la separació */
    }
    .separator {
        width: 100%;
        height: 2px;
        background-color: #123456; /* Pots canviar el color segons les teves necessitats */
        margin: 20px 0; /* Ajusta el marge segons les teves necessitats */
    }
    .custom-element {
        background-color: #d4edda; /* Tono gris clar */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px; /* Ajusta el marge inferior */
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Utilitza HTML per aplicar la classe CSS al títol
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
categoria = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona un valor:</p>', unsafe_allow_html=True)
temps_prep = st.slider('', 0, 240, (0, 240), step=1)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
ingredients_seleccionats = st.multiselect('',llista_ingredients)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)



# Definir la consulta SQL amb els paràmetres necessaris
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps, Receptes.Etiquetes,
    GROUP_CONCAT(Ingredients.nom || ' (' || Ingredients.quantitat || ')', ', ') AS components
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



#____________________________________________________________________
# Funció per crear targetes amb classes CSS específiques
# Funció per crear la targeta HTML amb el botó de ràdio
def create_card(data):
    ID_Recepte = data['ID_Recepte']
    Data_formatejada = data['Data_formatejada']
    Titol = data['Titol']
    img_base64 = data['img_base64']
    Metode = data['Metode']
    Temps = data['Temps']
    Preparacio = data['Preparacio']
    components = data['components']
    Categoria = data['Categoria']
    Etiquetes = data['Etiquetes']




    html_card_template = f'''
    <div style="background-color:#ffffff; padding:10px; border-radius:5px; margin:10px; border:1px solid #ccc;">
        <!-- Taula amb tres columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 33,33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>ID:</strong> {ID_Recepte}</td>
                <td style="width: 33,33%; padding-left: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Data:</strong> {Data_formatejada}</td>
                <td style="width: 33,33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Categoria:</strong> {Categoria}</td>
            </tr>
        </table>
        <!-- Segona fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>Titol: <strong>{Titol}</strong>
        </div>
        <!-- Tercera fila: dues columnes amb relació 80% - 20% -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <!-- Columna d'imatge (80%) -->
                <td style="width: 80%; padding: 10px; text-align: left; border: 1px solid #000;">
                    <img src="data:image/jpeg;base64,{img_base64}" alt="Imatge" style="width: 100%; height: auto; border-radius: 5px;"/>
                </td>
                <!-- Columna de detalls (20%) dividida en tres files amb encapçalaments a dalt -->
                <td style="width: 20%; padding: 0; text-align: left; border: 1px solid #000; height: 300px; vertical-align: top;">
                    <table style="width: 100%; height: 100%; border-collapse: collapse;">
                        <tr style="height: 33.33%;">
                            <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                                <strong>Temps:</strong> <br> {Temps}
                            </td>
                        </tr>
                        <tr style="height: 33.33%;">
                            <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                                <strong>Preparació:</strong> <br> {Preparacio}
                            </td>
                        </tr>
                        <tr style="height: 33.33%;">
                            <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                                <strong>Etiquetes:</strong> <br> {Etiquetes}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
         <!-- Quarta fila: una columna -->
        <div style="padding-top: 10px; padding-right: 10px; padding-left: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;"><strong>Mètode:
            <strong>
            <p>{Metode}</p>
        </div>
        <!-- Cinquena fila amb tres columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Temps:</strong> {Temps}</td>
                <td style="width: 33.33%; padding: 0 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Ingredients: </strong> {components}</td>
                <td style="width: 33.33%; padding-left: 10px; text-align: right; border-bottom: 1px solid #ccc;"><strong>Categoria:</strong> {Categoria}</td>
            </tr>
        </table>
        <!-- Sisena fila amb una columna -->
        <div style="padding-top: 10px; padding-right: 10px; padding-left: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;"><strong>Ingredients:
            <strong>{components}
        </div>
    </div>
    <!-- Separador -->
    <div style="width: 100%; height: 2px; background-color: #123456; margin: 20px 0;"></div>
    '''
    return html_card_template


# Bucle a través dels resultats per crear targetes
for resultado in resultados:
    data = {
        'ID_Recepte': resultado[0],
        'Data_formatejada': resultado[1],
        'Titol': resultado[2],
        'Metode': resultado[3],
        'Categoria': resultado[4],
        'Preparacio': resultado[5],
        'Etiquetes': resultado[8],
        'img_base64': convert_blob_to_base64(resultado[6]),
        'Temps': resultado[7],
        'components': ', '.join(obtenir_emoji(resultado[9]))  # Convertir components a cadena amb emojis
    }


    # crear la targeta amb l'opció seleccionada
    card_html = create_card(data)
    st.markdown(card_html, unsafe_allow_html=True)


# Tancar la connexió a la base de dades
conn.close()
