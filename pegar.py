import streamlit as st

# Exemple de resultats
resultados = [
    (1, '2025-01-01', 'Recepta 1', 'Metode 1', 'radio 1', 'Preparacio 1', b'imatge1', '10 min', 'Components 1'),
    (2, '2025-01-02', 'Recepta 2', 'Metode 2', 'radio 2', 'Preparacio 2', b'imatge2', '20 min', 'Components 2'),
]

# Inicialitzar l'estat de les pàgines si no està inicialitzat
if 'page' not in st.session_state:
    st.session_state.page = {}


# Funció per convertir blob a base64
def convert_blob_to_base64(blob):
    return "base64"


# Funció per obtenir emojis (dummy function for the example)
def obtenir_emoji(components):
    return components.split(', ')


# Funció per crear la targeta HTML amb el botó de ràdio dins la cel·la 'radio'
def create_card(data, radio_html):
    ID_Recepte = data['ID_Recepte']
    Data_formatejada = data['Data_formatejada']
    Titol = data['Titol']
    img_base64 = data['img_base64']
    Metode = data['Metode']
    Temps = data['Temps']
    Preparacio = data['Preparacio']
    components = data['components']

    html_card_template = f'''
    <div style="background-color:#ffffff; padding:10px; border-radius:5px; margin:10px; border:1px solid #ccc;">
        <!-- Taula amb tres columnes -->
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>ID:</strong> {ID_Recepte}</td>
                <td style="width: 33.33%; padding-left: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Data:</strong> {Data_formatejada}</td>
                <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Radio:</strong> {radio_html}</td>
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
                                <strong>Radio:</strong> <br> {radio_html}
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
                <td style="width: 33.33%; padding-left: 10px; text-align: right; border-bottom: 1px solid #ccc;"><strong>Radio:</strong> {radio_html}</td>
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
        'img_base64': convert_blob_to_base64(resultado[6]),
        'Temps': resultado[7],
        'components': ', '.join(obtenir_emoji(resultado[8]))  # Convertir components a cadena amb emojis
    }

    # Inicialitzar l'estat de la pàgina de cada targeta si no està inicialitzat
    if str(data['ID_Recepte']) not in st.session_state.page:
        st.session_state.page[str(data['ID_Recepte'])] = "Crear"

    # Crear una radio button amb opcions de redirecció de pàgines per a cada targeta
    with st.form(key=f"radio_form_{data['ID_Recepte']}"):
        radio = st.radio(
            f"Selecciona una opció per {data['Titol']}:",
            ("Crear", "Borrar"),
            index=("Crear", "Borrar").index(st.session_state.page[str(data['ID_Recepte'])]),
            key=f"radio_{data['ID_Recepte']}"
        )
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.session_state.page[str(data['ID_Recepte'])] = radio

        # Generar el codi HTML del botó de ràdio per incloure'l a la cel·la 'radio'
        radio_html = f'''
        <div>
            <input type="radio" id="crear_{data['ID_Recepte']}" name="radio_{data['ID_Recepte']}" value="Crear" {'checked' if st.session_state.page[str(data['ID_Recepte'])] == "Crear" else ''}>
            <label for="crear_{data['ID_Recepte']}">Crear</label><br>
            <input type="radio" id="borrar_{data['ID_Recepte']}" name="radio_{data['ID_Recepte']}" value="Borrar" {'checked' if st.session_state.page[str(data['ID_Recepte'])] == "Borrar" else ''}>
            <label for="borrar_{data['ID_Recepte']}">Borrar</label><br>
        </div>
        '''

    # Crear la targeta amb l'opció seleccionada
    card_html = create_card(data, radio_html)
    st.markdown(card_html, unsafe_allow_html=True)

    # Mostrar el contingut segons la pàgina seleccionada per a cada target
