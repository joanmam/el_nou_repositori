import streamlit as st
import sqlite3
import emoji
import re


# Funció per convertir blob a base64
def convert_blob_to_base64(blob):
    # La teva implementació aquí
    pass


# Funció per crear una card HTML
def create_card(data):
    # La teva implementació aquí
    pass


# Conectar a la base de dades
connexio = sqlite3.connect('base_de_dades.db')
cursor = connexio.cursor()

# Consulta SQL per obtenir les dades
consulta_sql = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps,
    GROUP_CONCAT(Ingredients.nom || ' (' || Ingredients.quantitat || ')', ', ') AS components
    FROM Receptes
    LEFT JOIN Ingredients
    ON Receptes.ID_Recepte = Ingredients.ID_Recepte
'''
cursor.execute(consulta_sql)
resultados = cursor.fetchall()

# Diccionari de emojis
emojis = {
    'fresas': emoji.emojize(':strawberry:'),
    'manzanas': emoji.emojize(':apple:'),
    'platanos': emoji.emojize(':banana:'),
    'uvas': emoji.emojize(':grapes:'),
    'sandia': emoji.emojize(':watermelon:'),
    'carbasso': emoji.emojize(':cucumber:'),
    'tomates': emoji.emojize(':tomato:'),
    'patatas': emoji.emojize(':potato:')
    # Afegeix més valors i emojis aquí
}


# Funció per obtenir l'emoji basat en el valor de la cel·la
def obtenir_emoji(components):
    if not isinstance(components, str):
        raise TypeError("Expected string or bytes-like object, got {}".format(type(components).__name__))

    emoji_noms = re.findall(r'(\w+)\s*\(([^)]+)\)', components)
    resultat_emoji = []

    for nom, quantitat in emoji_noms:
        emoji_nom = emojis.get(nom.lower(), '')  # Canviat per retornar una cadena buida si no es troba un emoji
        if emoji_nom:
            resultat_emoji.append(f"{nom} {emoji_nom} ({quantitat})")
        else:
            resultat_emoji.append(f"{nom} ({quantitat})")  # Només mostra el nom i la quantitat

    return resultat_emoji


# Interfície d'usuari en Streamlit
st.title("Productes amb Icones")

# Mostrar les dades amb icones
for resultado in resultados:
    ID_Recepte, Data_formatejada, Titol, Metode, Categoria, Preparacio, blob, Temps, Components = resultado
    if not isinstance(Components, str):
        st.error("Expected string or bytes-like object, got {}".format(type(Components).__name__))
        continue

    components_amb_emojis = obtenir_emoji(Components)
    components_amb_emoji_str = ', '.join(components_amb_emojis)

    # Actualitzar el valor de 'components' en el diccionari 'data'
    data = {
        'ID_Recepte': resultado[0],
        'Data_formatejada': resultado[1],
        'Titol': resultado[2],
        'Metode': resultado[3],
        'Categoria': resultado[4],
        'Preparacio': resultado[5],
        'img_base64': convert_blob_to_base64(resultado[6]),
        'Temps': resultado[7],
        'components': components_amb_emoji_str  # Utilitzar components_amb_emoji_str
    }
    card_html = create_card(data)
    st.markdown(card_html, unsafe_allow_html=True)

# Tancar la connexió a la base de dades
connexio.close()



