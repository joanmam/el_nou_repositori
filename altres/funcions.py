import re
import streamlit as st
import emoji
from altres.manteniment import emojis
import base64
import sqlite3
from altres.variables import path
from altres.variables import background_image_url



# Funció per obtenir l'emoji basat en el valor de la cel·la
emoji_per_defecte = "\u2753"

def obtenir_emoji(components):
    if components is None:
        return [emoji_per_defecte]
    emoji_noms = re.findall(r'(\w+)\s*\(([^)]+)\)', components)
    resultat_emoji = []

    for nom, quantitat in emoji_noms:
        emoji_nom = emojis.get(nom.lower(), emoji_per_defecte)
        resultat_emoji.append(f"{emoji_nom} {nom} ({quantitat})")

    return resultat_emoji


#_____________________________________________________________

# Función para agregar estilos CSS
def agregar_estilos_css():
    st.markdown(
        """
        <style>
        .etiqueta {
            display: inline-block;
            border: 1px solid black;
            background-color: #ff9933;
            padding: 2px 5px;
            margin: 2px;
            border-radius: 5px;
        }
        .card {
            background-color: #ffffff; 
            padding: 10px; 
            border-radius: 5px; 
            margin: 10px; 
            border: 1px solid #ccc;
        }
        .card-table {
            width: 100%; 
            border-collapse: collapse;
        }
        .card-table td {
            border-bottom: 1px solid #ccc;
            padding: 5px;
        }
        .card-separator {
            width: 100%; 
            height: 2px; 
            background-color: #123456; 
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Función para crear etiquetas HTML con estilo
def crear_etiquetas_html(etiquetas):
    return " ".join([f'<span class="etiqueta">{etiqueta.strip()}</span>' for etiqueta in etiquetas.split(' ')])

# Función para crear una tarjeta HTML
def crear_tarjeta_html(data):
    ID_Recepte = data['ID_Recepte']
    Data_formatejada = data['Data_formatejada']
    Titol = data['Titol']
    img_base64 = data['img_base64']
    Metode = data['Metode']
    Temps = data['Temps']
    Preparacio = data['Preparacio']
    components = data['components']
    Categoria = data['Categoria']
    Etiquetes = crear_etiquetas_html(data['Etiquetes'])

    return f'''
    <div class="card">
        <table class="card-table">
            <tr>
                <td style="width: 33%;">ID: {ID_Recepte}</td>
                <td style="width: 33%;">Data: {Data_formatejada}</td>
                <td style="width: 33%;">Categoria: {Categoria}</td>
            </tr>
        </table>
        <div style="padding-top: 10px; margin-bottom: 10px;">Titol: <strong>{Titol}</strong></div>
        <table class="card-table">
            <tr>
                <td style="width: 80%; text-align: left;">
                    <img src="data:image/jpeg;base64,{img_base64}" alt="Imatge" style="width: 100%; height: auto; border-radius: 5px;"/>
                </td>
                <td style="width: 20%; vertical-align: top;">
                    <table style="width: 100%; height: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 10px;">Temps: {Temps}</td></tr>
                        <tr><td style="padding: 10px;">Preparació: {Preparacio}</td></tr>
                        <tr><td style="padding: 10px;">Etiquetes: {Etiquetes}</td></tr>
                    </table>
                </td>
            </tr>
        </table>
        <div style="padding-top: 10px; margin-bottom: 10px;">Mètode: {Metode}</div>
        <table class="card-table">
            <tr>
                <td style="width: 33%;">Temps: {Temps}</td>
                <td style="width: 33%;">Ingredients: {components}</td>
                <td style="width: 33%; text-align: right;">Categoria: {Categoria}</td>
            </tr>
        </table>
        <div style="padding-top: 10px; margin-bottom: 10px;">Ingredients: {components}</div>
    </div>
    <div class="card-separator"></div>
    '''

#__________________________________________________________
#Convert_blob_to_base64
def convert_blob_to_base64(blob):
    if blob:
        return base64.b64encode(blob).decode('utf-8')
    return ''

#__________________________________________________________
# Funció per obtenir la llista d'ingredients de la base de dades
def obtenir_ingredients():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

#________________________________________________________________
def estils_marc_home():
    st.markdown(
    '''
    <style>
    .marco {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        align-self: flex-start;
        width: 300px;
        height: 300px;
        border: 2px solid #003366;  /* Borde de color negre */
        border-radius: 15px;  /* Bordes arrodonits */
        font-size: 24px;  /* Mida de la font */
        font-weight: bold;
        color: #003366;  /* Color del text */
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);  /* Una mica d'ombra per a millorar la visibilitat */
        text-align: top;  /* Text centrat */
        padding: 10px;  /* Espai intern al voltant del contingut */
        margin: 20px auto;  /* Centrar el marc horitzontalment */
        float: left;  /* Flota a l'esquerra */
    }    
    .text-personalitzat {
        position: relative;
        top: 5px;  /* Desplaça el text cap avall */
    }
    .resultat {
        font-size: 175px;  /* Mida del text del resultat */
        line-height: 1; /* Assegura que el resultat es mantingui centrat */
    }
    </style>
    ''',
    unsafe_allow_html=True
    )

#___________________________________________________
# def background_estil():
#     st.markdown(
#     '''
#     <style>
#     .stApp {{
#         background: url("{background_image_url}") no-repeat center center;
#         background-size: 70%;
#         height: 100vh;
#         display: flex;
#         justify-content: flex-end;
#         align-items: flex-end;
#         position: relative;
#     }}
#     .title-container {{
#         display: flex;
#         justify-content: flex-end;
#         align-items: flex-end;
#         height: 100vh;
#         width: 100%;
#         position: fixed;
#         top: 0;
#         left: 0;
#         padding: 1em;
#     }}
#     .title {{
#         color: white;
#         font-size: 3em;
#         text-align: right;
#         background: rgba(0, 0, 0, 0.5);
#         padding: 0.5em;
#         border-radius: 0.5em;
#     }}
#     .custom-text {{
#         position: fixed;
#         bottom: 200px;
#         right: 200px;
#         font-size: 100px; /* Augmenta la mida de la font */
#         font-weight: bold;
#         color: #003366; /* Pots canviar el color segons les teves necessitats */
#         background-color: transparent;
#         padding: 10px;
#         border: 2px solid #003366;
#         border-radius: 15px; /* Bordes arrodonits */
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Afegir una mica d'ombra per a millorar la visibilitat */
#     }}
#     </style>
#     ''',
#     unsafe_allow_html=True
#     )
#
