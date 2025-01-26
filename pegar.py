import streamlit as st
import sqlite3
import base64

# Funció per convertir blob a base64
def convert_blob_to_base64(blob):
    if blob:
        return base64.b64encode(blob).decode('utf-8')
    return ''

# Funció per crear la targeta HTML
def create_card(data):
    ID_Recepte = data.get('ID_Recepte', 'Desconegut')
    Data_formatejada = data.get('Data_formatejada', 'Data no disponible')
    Titol = data.get('Titol', 'Títol no disponible')
    img_base64 = data.get('img_base64', '')
    Metode = data.get('Metode', 'Mètode no disponible')
    Temps = data.get('Temps', 'Temps no disponible')
    Components = data.get('components', 'Components no disponibles')
    Categoria = data.get('Categoria', 'Categoria no disponible')

    html_card_template = f'''
    <div style="background-color:#ffffff; padding:10px; border-radius:5px; margin:10px; border:1px solid #ccc;">
        <!-- Taula amb dues columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 50%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>ID:</strong> {ID_Recepte}</td>
                <td style="width: 50%; padding-left: 10px; text-align: right; border-bottom: 1px solid #ccc;"><strong>Data:</strong> {Data_formatejada}</td>
            </tr>
        </table>
        <!-- Segona fila: una columna -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>{Titol}</strong>
        </div>
        <!-- Tercera fila: una columna amb imatge centrada -->
        <div style="text-align: center; padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <img src="data:image/jpeg;base64,{img_base64}" alt="Imatge" style="max-width: 50%; height: auto; border-radius: 5px;"/>
        </div>
        <!-- Quarta fila: una columna amb nou paràgraf -->
        <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
            <strong>{Metode}</strong>
            <p>Aquí pots afegir el contingut del teu nou paràgraf. Pots posar qualsevol informació addicional que desitgis afegir després del títol Metode.</p>
        </div>
        <!-- Última fila amb tres columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Temps:</strong> {Temps}</td>
                <td style="width: 33.33%; padding: 0 10px; text-align: center; border-bottom: 1px solid #ccc;"><strong>Components:</strong> {Components}</td>
                <td style="width: 33.33%; padding-left: 10px; text-align: right; border-bottom: 1px solid #ccc;"><strong>Categoria:</strong> {Categoria}</td>
            </tr>
        </table>
    </div>
    <!-- Separador -->
    <div style="width: 100%; height: 2px; background-color: #123456; margin: 20px 0;"></div>
    '''
    return html_card_template

# Connectar-se a la base de dades
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Consulta SQL amb paràmetres
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Metode, 
           Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps, 
           GROUP_CONCAT(Ingredients.nom || ' (' || Ingredients.quantitat || ')', ', ') AS components
    FROM Receptes
    LEFT JOIN Ingredients ON Receptes.ID_Recepte = Ingredients.ID_Recepte
    GROUP BY Receptes.ID_Recepte
'''

# Executar la consulta i obtenir els resultats
cursor.execute(query)
resultados = cursor.fetchall()

# Crear targetes HTML amb els resultats obtinguts
for resultado in resultados:
    data = {
        'ID_Recepte': resultado[0],
        'Data_formatejada': resultado[1],
        'Titol': resultado[2],
        'Metode': resultado[3],
        'Categoria': resultado[4],
        'Preparacio': resultado[5],
        'img_base64': convert_blob_to_base64(resultado[6]),  # Convertir el blob a base64
        'Temps': resultado[7],
        'components': resultado[8]  # Utilitzar el nom de la variable components
    }
    card_html = create_card(data)
    st.markdown(card_html, unsafe_allow_html=True)

# Tancar la connexió
conn.close()

