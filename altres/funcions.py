import re
import streamlit as st
import base64
from altres.variables import background_image_url
from datetime import datetime
import streamlit.components.v1 as components
from PIL import Image
import io
import html
from altres.variables import cami_db
import emoji
from altres.manteniment import emojis
import sqlitecloud
import requests
from altres.variables import img_url
from io import BytesIO, StringIO




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
    Observacions = data['Observacions']
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
        <div style="padding-top: 10px; margin-bottom: 10px;">Observacions: {Observacions}</div>
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
    conn = sqlitecloud.connect(cami_db)
    cursor = conn.cursor()
    cursor.execute("SELECT nom FROM ingredients")
    return [row[0] for row in cursor.fetchall()]

#________________________________________________________________
def estils_marc():
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
        color: #00001a;  /* Color del text */
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
def background_home():
    # URL de la imatge de fons
   # background_image_url = "https://cuidateplus.marca.com/sites/default/files/styles/natural/public/cms/platanos_0.jpg.webp?itok"
    background_image_url = "https://static01.nyt.com/images/2024/04/24/multimedia/aw-tomato-beansrex-mwfq/aw-tomato-beansrex-mwfq-threeByTwoMediumAt2X.jpg?quality=75&auto=webp"
    # CSS personalitzat per posar la imatge de fons
    background_css = f"""
<style>
.stApp {{
    background: url("{background_image_url}") no-repeat center center;
    background-size: 70%;
    height: 100vh;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    position: relative;
}}
.title-container {{
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    height: 100vh;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    padding: 1em;
}}
.title {{
    color: white;
    font-size: 3em;
    text-align: right;
    background: rgba(0, 0, 0, 0.5);
    padding: 0.5em;
    border-radius: 0.5em;
}}
.custom-text {{
    position: fixed;
    bottom: 200px;
    right: 200px;
    font-size: 100px; /* Augmenta la mida de la font */
    font-weight: bold;
    color: #00001a; /* Pots canviar el color segons les teves necessitats */
    background-color: transparent;
    padding: 10px;
    border: 2px solid #003366;
    border-radius: 15px; /* Bordes arrodonits */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Afegir una mica d'ombra per a millorar la visibilitat */
}}
</style>
"""
    # Aplica el CSS utilitzant st.markdown
    st.markdown(background_css, unsafe_allow_html=True)
    # Afegir text personalitzat a l'extrem inferior dret
    st.markdown('<div class="custom-text">Mamen i les seves receptes</div>', unsafe_allow_html=True)

#________________________________________________________________________
#Rellotge
def rellotge():
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

#__________________________________________________________________
def banner(base64_image):
    # Injectar CSS per a la imatge de fons
    background_css = f"""
<style>
body .custom-background {{
    background-image: url('data:image/png;base64,{base64_image}');
    background-size: 100% ;  /* Ajusta l'amplada al 100% i l'alçada a 113 píxels (3 cm) */
    background-repeat: no-repeat;
    background-position: top;
    margin: 0;
    padding: 0;
    height: 150px;  /* Assegura que l'alçada sigui la desitjada */
}}
</style>
"""
    st.markdown(background_css, unsafe_allow_html=True)
    # Aplicar la classe CSS específica al contenidor principal
    st.markdown('<div class="custom-background"></div>', unsafe_allow_html=True)

#___________________________________________________________________
def lletra_variable():
    st.markdown(
        """
        <style>
        .custom-title {
            font-size: 24px; /* Ajusta aquesta mida segons les teves necessitats */
            font-weight: bold;
            margin-bottom: 0.002em;
        }
        .custom-title2 {
            font-size: 18px; /* Ajusta aquesta mida segons les teves necessitats */
            font-weight: bold;
            margin-bottom: 0.002em;
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
            margin-bottom: 1px; /* Ajusta el marge inferior */
        }
        .custom-element2 {
            background-color: #cc66ff; /* Tono gris clar */
            padding: 5px;
            border-radius: 5px;
            margin-bottom: 1px; /* Ajusta el marge inferior */
        </style>
        """,
        unsafe_allow_html=True
    )
#_____________________________________________________________________
def crear_tarjeta_html_resumida(data):
    ID_Recepte = data['ID_Recepte']
    Titol = data['Titol']
    return f'''
    <div class="card" style="width: 100%; border: 1px solid #ccc; padding: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 10px; font-weight: bold">
        <table class="card-table" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 10%;">ID: {ID_Recepte}</td>
                <td style="width: 90%;">Titol: {Titol}</td>
            </tr>
        </table>
    </div>
    <div class="card-separator"></div>
    '''


def crear_tarjeta_html_fet(data):
    ID_Recepte = data['ID_Recepte']
    Titol = data['Titol']
    Accio = data['Accio']
    Data_accio = data['Data_accio']
    return f'''
    <div class="card">
        <table class="card-table">
            <tr>
                <td style="width: 10%;">ID: {ID_Recepte}</td>
                <td style="width: 60%;">Titol: {Titol}</td>
                <td style="width: 15%;">Accio: {Accio}</td>
                <td style="width: 15%;">Data Accio: {Data_accio}</td>
            </tr>
        </table>
    </div>
    <div class="card-separator"></div>
    '''

def separador():
    st.markdown(
        '''
        <style>
        .separator {
            width: 100%;
            height: 10px;
            background-color: #123456; /* Pots canviar el color segons les teves necessitats */
            margin: 5px 0; /* Ajusta el marge segons les teves necessitats */
        }
        </style>
        <div class="separator"></div>
        ''',
        unsafe_allow_html=True
    )

def crear_tarjeta_html_pas(data):
    ID_Recepte = data['ID_Recepte']
    Titol = data['Titol']
    Numero = data['Numero']
    Pas = data['Pas']
    return f'''
    <div class="card">
        <table class="card-table">
            <tr>
                <td style="width: 10%;">ID: {ID_Recepte}</td>
                <td style="width: 70%;">Titol: {Titol}</td>
                <td style="width: 5%;">Numero: {Numero}</td>
                <td style="width: 15%;">Pas: {Pas}</td>
            </tr>
        </table>
    </div>
    <div class="card-separator"></div>
    '''


def crear_tarjeta_html_protocol(data):
    ID_Recepte = data['ID_Recepte']
    Titol = data['Titol']
    Numero = data['Numero']
    Pas = data['Pas']
    img_base64 = data['Imatge']
    return f'''
    <div class="card">
        <table class="card-table">
            <tr>
                <td style="width: 10%;">ID: {ID_Recepte}</td>
                <td style="width: 65%;">Titol: {Titol}</td>
                <td style="width: 5%;">Numero: {Numero}</td>
                <td style="width: 5%;"><img src="data:image/png;base64,{img_base64}" alt="Imatge del pas" /></td>
                <td style="width: 15%;">Pas: {Pas}</td>
            </tr>
        </table>
    </div>
    <div class="card-separator"></div>
    '''



# Funcions de conversió d'imatges
def convert_blob_to_image(blob_data):
    try:
        if isinstance(blob_data, bytes):
            image = Image.open(io.BytesIO(blob_data))
            return image
        else:
            st.error("El blob_data no està en bytes")
            return None
    except Exception as e:
        st.error(f"Error convertint el blob a imatge: {e}")
        return None

def create_thumbnail(image, size=(100, 100)):
    try:
        thumbnail = image.copy()
        thumbnail.thumbnail(size)
        return thumbnail
    except Exception as e:
        st.error(f"Error creant la miniatura: {e}")
        return None

def convert_image_to_base64(image):
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error convertint la imatge a base64: {e}")
        return

# Funció per crear la taula HTML


def crear_taula_html_protocol2(encapcalat, passos):
    html = f"""
    <div style='border: 1px solid #ccc; padding: 20px; margin: 20px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);'>
        <h2>{encapcalat['Titol']}</h2>
        <h4>ID Recepta: {encapcalat['ID_Recepte']}</h4>
        <table style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr>
                    <th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>Número</th>
                    <th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>Imatge</th>
                    <th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>Pas</th>
                </tr>
            </thead>
            <tbody>
    """

    for pas in passos:
        imatge_html = f'<img src="data:image/png;base64,{pas["Imatge"]}" alt="Imatge del pas" style="width: 100px; height: auto;" />'
        html += f"""
        <tr>
          <td style="border: 1px solid #ddd; padding: 8px;">{pas['Numero']}</td>
          <td style="border: 1px solid #ddd; padding: 8px;">{imatge_html}</td>
          <td style="border: 1px solid #ddd; padding: 8px;">{pas['Pas']}</td>
        </tr>
        """

    html += """
            </tbody>
        </table>
    </div>
    """
    return html


def crear_taula_markdown(encapcalat, passos):
    # Inicia el markdown amb el títol i l'encapçalament de la taula
    markdown = f"""
    ### {encapcalat['Titol']}
    **ID Recepta**: {encapcalat['ID_Recepte']}

    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Número</th>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Imatge</th>
                <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Pas</th>
            </tr>
        </thead>
        <tbody>
    """
    st.write("Inici de la taula markdown:")
    st.write(markdown)

    # Afegeix les files de la taula amb els passos
    for pas in passos:
        imatge_html = f'<img src="data:image/png;base64,{pas["Imatge"]}" alt="Imatge del pas" style="width: 100px; height: auto;" />'
        fila = f"""
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">{pas['Numero']}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{imatge_html}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{pas['Pas']}</td>
        </tr>
        """
        st.write("Afegint fila markdown:")
        st.write(fila)
        markdown += fila

    # Tanca la taula
    markdown += """
        </tbody>
    </table>
    """
    return markdown




def crear_taula_encapcalat(encapcalat):
    html = f"""
    <div>
        <table style="width: 100%; border-collapse: collapse; padding: 0; margin: 0;">
            <tr style="border-top: 1px solid black; border-bottom: 1px solid black;">
                <th style="width: 10%; border: none; padding: 0; margin: 0;">ID Recepta</th>
                <th style="width: 80%; border: none; padding: 0; margin: 0;">Títol</th>
            </tr>
            <tr style="border-bottom: 1px solid black;">
                <td style="border: none; padding: 0; margin: 0;">{encapcalat['ID_Recepte']}</td>
                <td style="border: none; padding: 0; margin: 0;">{encapcalat['Titol']}</td>
            </tr>
        </table>
    </div>
    """
    return html



def crear_taula_passos_sense_encapcalat(passos):
    html_table = """
    <div>
        <table style="width: 100%; border-collapse: collapse; padding: 5; margin: 5; border-top: 1px solid black;">
    """
    for pas in passos:
        numero = pas.get('Numero', 'N/A')
        descripcio_pas = html.escape(pas.get('Pas', 'Sense descripció'))
        imatge_base64 = pas.get('Imatge', None)

        if imatge_base64:
            imatge_html = f'<img src="data:image/png;base64,{imatge_base64}" alt="Imatge del pas" style="width: 100px;" />'
        else:
            imatge_html = "No hi ha imatge"

        html_table += f"""
        <tr style="border-bottom: 1px solid black;">
            <td style="width: 10%; border: none; padding: 5; margin: 0;">{numero}</td>
            <td style="width: 10%; border: none; padding: 5; margin: 0;">{imatge_html}</td>
            <td style="width: 80%; border: none; padding: 5; margin: 0;">{descripcio_pas}</td>
        </tr>
        """
    html_table += """
        </table>
    </div>
    """
    return html_table


def row_style(row):
    return ['background-color: #f0f0f0'
            if row.name % 2 == 0 else 'background-color: #ffffff' for _ in row]



def dataframe_pagina(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
        margin: 0;  /* Elimina márgenes innecesarios */
        padding: 0;  /* Elimina espacios innecesarios */
    }}
    .dataframe-container table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }}
    .dataframe-container th, .dataframe-container td {{
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        font-family: Arial, sans-serif;  /* Canviar el tipus de lletra aquí */
        font-size: 14px;  /* Canviar la mida de la lletra aquí */
    }}
    .dataframe-container th.col0 {{
        width: 10%;  /* Amplada de la primera columna */
    }}
    .dataframe-container th.col1 {{
        width: 90%;  /* Amplada de la segona columna */
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula


def dataframe_passos(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
        margin: 0;  /* Elimina márgenes innecesarios */
        padding: 0;  /* Elimina espacios innecesarios */
    }}
    .dataframe-container table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }}
    .dataframe-container th, .dataframe-container td {{
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        # border-left: 1px solid #000;
        font-family: Arial, sans-serif;  /* Canviar el tipus de lletra aquí */
        font-size: 14px;  /* Canviar la mida de la lletra aquí */
    }}
    .dataframe-container th.col0, .dataframe-container td.col0 {{
        width: 10%;  /* Amplada de la primera columna */
    }}
    .dataframe-container th.col1, .dataframe-container td.col1 {{
        width: 10%;  /* Amplada de la segona columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col2 {{
        width: 80%;  /* Amplada de la tercera columna */
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula


# Funció per convertir el blob a una imatge
def blob_to_image(blob):
    image = Image.open(io.BytesIO(blob))
    return image

# Funció per convertir el blob a una miniatura
def create_thumbnail2(blob):
    image = Image.open(io.BytesIO(blob))
    image.thumbnail((100, 100))  # Redueix la mida de la imatge
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img_str}" alt="Imatge"/>'


def cropping():
    # Descarregar la imatge
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))
    # Definir les coordenades del crop (left, top, right, bottom)
    left = 100
    top =50
    right = 400
    bottom = 200
    cropped_image = image.crop((left, top, right, bottom))
    buffered = BytesIO()
    cropped_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str, cropped_image

def dataframe_accions(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
        margin: 0;  /* Elimina márgenes innecesarios */
        padding: 0;  /* Elimina espacios innecesarios */
    }}
    .dataframe-container table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }}
    .dataframe-container th, .dataframe-container td {{
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        # border-left: 1px solid #000;
        font-family: Arial, sans-serif;  /* Canviar el tipus de lletra aquí */
        font-size: 14px;  /* Canviar la mida de la lletra aquí */
    }}
    .dataframe-container th.col0, .dataframe-container td.col0 {{
        width: 10%; 
    }}   
    .dataframe-container th.col1, .dataframe-container td.col1 {{
        width: 60%; 
    }}
    .dataframe-container th.col2, .dataframe-container td.col2 {{
        width: 15%; 
    }}
    .dataframe-container th.col3, .dataframe-container td.col3 {{
        width: 15%;  
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula

def inici():
    rellotge()
    st.header("Accions")
    base64_image, cropped_image = cropping()
    banner(base64_image)

def connexio():
    conn = sqlitecloud.connect(cami_db)
    return conn


def process_observacions(observacions):
    url = find_url(observacions)
    if url:
        return observacions.replace(url, f'<a href="{url}" target="_blank">{url}</a>')
    return observacions

def find_url(text):
    url_pattern = re.compile(r'(https?://\S+)')
    url = url_pattern.search(text)
    return url.group(0) if url else ''


def dataframe_estadistiques(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
        margin: 0;  /* Elimina márgenes innecesarios */
        padding: 0;  /* Elimina espacios innecesarios */
    }}
    .dataframe-container table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }}
    .dataframe-container th, .dataframe-container td {{
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        # border-left: 1px solid #000;
        font-family: Arial, sans-serif;  /* Canviar el tipus de lletra aquí */
        font-size: 14px;  /* Canviar la mida de la lletra aquí */
    }}
    .dataframe-container th.col0, .dataframe-container td.col0 {{
        width: 10%;  /* Amplada de la primera columna */
    }}
    .dataframe-container th.col1, .dataframe-container td.col1 {{
        width: 30%;  /* Amplada de la segona columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col2 {{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col3 {{
        width: 45%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col4 {{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col5{{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula

def dataframe_actualitzar(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
        margin: 0;  /* Elimina márgenes innecesarios */
        padding: 0;  /* Elimina espacios innecesarios */
    }}
    .dataframe-container table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }}
    .dataframe-container th, .dataframe-container td {{
        padding: 8px;
        text-align: left;
        vertical-align: top;
        border-bottom: 1px solid #ddd;
        # border-left: 1px solid #000;
        font-family: Arial, sans-serif;  /* Canviar el tipus de lletra aquí */
        font-size: 14px;  /* Canviar la mida de la lletra aquí */
    }}
    .dataframe-container th.col0, .dataframe-container td.col0 {{
        width: 10%;  /* Amplada de la primera columna */
    }}
    .dataframe-container th.col1, .dataframe-container td.col1 {{
        width: 55%;  /* Amplada de la segona columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col2 {{
        width: 15%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col3 {{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col4 {{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col5{{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    .dataframe-container th.col2, .dataframe-container td.col6{{
        width: 5%;  /* Amplada de la tercera columna */
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula

# Función para agregar el enlace a la biblioteca de iconos de Google
def agregar_iconos_google():
    st.markdown(
        '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
        unsafe_allow_html=True)


def procesar_fila(row):
    # Simular la conversión del blob de imagen a base64
    img_base64 = convert_blob_to_base64(row['blob'])

    # Procesar componentes (por ejemplo, concatenar ingredientes con cantidades)
    components = row['components']  # Ya viene procesado si usaste GROUP_CONCAT en la consulta

    # Crear una estructura de datos final con todos los campos requeridos
    return {
        'ID_Recepte': row['ID_Recepte'],
        'Data_formatejada': row['Data_formatejada'],
        'Titol': row['Titol'],
        'Observacions': row['Observacions'],
        'Categoria': row['Categoria'],
        'Preparacio': row['Preparacio'],
        'img_base64': img_base64,
        'Temps': row['Temps'],
        'components': components,
        'Etiquetes': row['Etiquetes']  # Si necesitas convertirlo, usa ', '.join(row['Etiquetes'])
    }


def convert_blob_to_base64_2(blob, width=100, max_height=150):
    """
    Convierte un blob de imagen de la base de datos a una imagen redimensionada en base64.

    Args:
    - blob: Datos binarios de la imagen.
    - width: Ancho deseado para la imagen redimensionada.
    - height: Altura deseada. Si no se proporciona, se calcula manteniendo la proporción.

    Returns:
    - str: Imagen en base64 lista para usar en HTML.
    """
    try:
        # Convertir el blob en un objeto de imagen usando Pillow
        image = Image.open(io.BytesIO(blob))

        # Redimensionar la imagen
        if height > max_height:
            aspect_ratio = image.height / image.width
            height = int(width * aspect_ratio)
        resized_image = image.resize((width, height), Image.ANTIALIAS)

        # Convertir la imagen redimensionada a base64
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error al procesar el blob de imagen: {e}")
        return None

def agregar_espaciado_css():
    """
    Agrega estilos CSS globales para separar las tarjetas con espaciado uniforme.
    """
    css = """
    <style>
    .card-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* Dos columnas */
        gap: 20px; /* Espaciado entre tarjetas */
        padding: 20px;
    }
    .card {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        background-color: #fff;
    }
    </style>
    """

def generar_targeta(titol, data_formatejada, imatge_base64, ingredients, temps_preparacio, temps_total, observacions, etiquetes):
    return f"""
    <div style="display: grid; grid-template-columns: 1fr; grid-template-rows: auto auto auto auto; gap: 10px; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background-color: #f9f9f9;">
        <!-- Primera fila: Imatge i Títol (títol justificat a dalt) -->
        <div style="display: flex; align-items: flex-start; grid-column: 1 / span 1;">
            <img src="data:image/jpeg;base64,{imatge_base64}" alt="Imatge" style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px; margin-right: 10px;">
            <div>
                <h3 style="margin: 0;">{titol}</h3>
                <small style="color: #888;">{data_formatejada}</small>
            </div>
        </div>
        <!-- Segona fila: Ingredients amb icona "grocery", Temps de Preparació amb icona "timer" i Temps Total -->
        <div style="grid-column: 1 / span 1; display: flex; justify-content: space-between; gap: 20px; align-items: center;">
            <p style="display: flex; align-items: center; gap: 5px;">
                <span class="material-symbols-outlined" style="font-size: 18px; vertical-align: middle;">grocery</span>
                {ingredients}
            </p>
            <p style="display: flex; align-items: center; gap: 5px;">
                <span class="material-symbols-outlined" style="font-size: 18px; vertical-align: middle;">timer</span>
                {temps_preparacio} min
            </p>
            <p><strong>Temps Total:</strong> {temps_total} min</p>
        </div>
        <!-- Tercera fila: Etiquetes -->
        <div style="grid-column: 1 / span 1; text-align: center; color: #555;">
            <p><strong>Etiquetes:</strong> {etiquetes}</p>
        </div>
        <!-- Quarta fila: Observacions -->
        <div style="grid-column: 1 / span 1; text-align: center; font-style: italic;">
            <p><strong>Observacions:</strong> {observacions}</p>
        </div>
    </div>
    """


def generar_html_fontawesome(titol, data_formatejada, imatge_base64, ingredients, temps_preparacio, temps_total, observacions, etiquetes):
    return f"""
    <div style="display: grid; grid-template-columns: 1fr; grid-template-rows: auto auto auto auto; gap: 10px; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background-color: #f9f9f9;">
        <!-- Primera fila: Imatge i Títol -->
        <div style="display: flex; align-items: flex-start; grid-column: 1 / span 1;">
            <img src="data:image/jpeg;base64,{imatge_base64}" alt="Imatge" style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px; margin-right: 10px;">
            <div>
                <h3 style="margin: 0;">{titol}</h3>
                <small style="color: #888;">{data_formatejada}</small>
            </div>
        </div>
        <!-- Segona fila: Ingredients amb icona Font Awesome, Temps de Preparació i Temps Total -->
        <div style="grid-column: 1 / span 1; display: flex; justify-content: space-between; gap: 20px; align-items: center;">
            <p style="display: flex; align-items: center; gap: 5px;">
                <i class="fas fa-shopping-cart" style="font-size: 18px; vertical-align: middle;"></i>
                {ingredients}
            </p>
            <p style="display: flex; align-items: center; gap: 5px;">
                <i class="fas fa-clock" style="font-size: 18px; vertical-align: middle;"></i>
                {temps_preparacio} min
            </p>
            <p style="display: flex; align-items: center; gap: 5px;">
                <i class="fas fa-hourglass" style="font-size: 18px; vertical-align: middle;"></i>
                {temps_total} min
        </div>
        <!-- Tercera fila: Etiquetes -->
        <div style="grid-column: 1 / span 1; text-align: center; color: #555;">
            <p><strong>Etiquetes:</strong> {etiquetes}</p>
        </div>
        <!-- Quarta fila: Observacions -->
        <div style="grid-column: 1 / span 1; text-align: center; font-style: italic;">
            <p><strong>Observacions:</strong> {observacions}</p>
        </div>
    </div>
    """

def font_awesome():
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)