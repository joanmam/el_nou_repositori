import pandas as pd
import streamlit as st

# Función para convertir BLOB a base64
def convert_blob_to_base64(blob):
    # Implementa tu lógica aquí
    pass

# Función para obtener emojis
def obtenir_emoji(ingredients):
    # Implementa tu lógica aquí
    pass

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

# Ejemplo de resultados
resultados = [
    # Añade tus datos aquí
]

# Agregar estilos CSS
agregar_estilos_css()

# Bucle a través de los resultados para crear tarjetas
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

    # Crear la tarjeta con la opción seleccionada
    card_html = crear_tarjeta_html(data)
    st.markdown(card_html, unsafe_allow_html=True)

# Cerrar la conexión a la base de datos si corresponde
# conn.close()
