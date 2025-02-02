import sqlite3
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from altres.funcions import obtenir_emoji
from altres.funcions import agregar_estilos_css
from altres.funcions import crear_tarjeta_html
from altres.funcions import convert_blob_to_base64
from altres.funcions import obtenir_ingredients
from altres.variables import path

st.set_page_config(layout="wide")




# Conectarse a la base de datos



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


#_____________________________________________________________________________
#connexio a la base de dades
conn = sqlite3.connect(path)
cursor = conn.cursor()



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

#____________________________________________________________



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
agregar_estilos_css()

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
    card_html = crear_tarjeta_html(data)
    st.markdown(card_html, unsafe_allow_html=True)


# Tancar la connexió a la base de dades
conn.close()
