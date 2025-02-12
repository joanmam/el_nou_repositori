import sqlite3
import streamlit as st
from PIL import Image
import base64
import io

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
        return ""

# Conexión a la base de datos
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Consulta per obtenir el títol i l'ID de la recepta
query_encapcalat = ('SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?;')
cursor.execute(query_encapcalat, (recepte_seleccionada,))
encapcalat_record = cursor.fetchone()

if not encapcalat_record:
    st.error("No s'ha trobat el títol i l'ID de la recepta seleccionada.")
else:
    encapcalat = {
        'ID_Recepte': encapcalat_record[0],
        'Titol': encapcalat_record[1]
    }

    # Consulta per obtenir els passos de la recepta
    query_passos = ('SELECT Numero, Pas, Imatge_passos '
                    'FROM Passos '
                    'WHERE ID_Recepte = ?;')
    cursor.execute(query_passos, (recepte_seleccionada,))
    passos_records = cursor.fetchall()

    if not passos_records:
        st.error("No s'han trobat passos per a la recepta seleccionada.")
    else:
        passos = []

        for record in passos_records:
            imatge_blob = record[2]

            Imatge = convert_blob_to_image(imatge_blob)
            if Imatge is not None:
                thumbnail = create_thumbnail(Imatge)
                imatge_base64 = convert_image_to_base64(thumbnail)
            else:
                imatge_base64 = ""  # Valor buit en cas d'error

            passos.append({
                'Numero': record[0],
                'Pas': record[1],
                'Imatge': imatge_base64
            })

        # Funció per crear la taula HTML
        def crear_taula_html_protocol2(encapcalat, passos):
            html = f"""
            <style>
                .recepta-card {{
                    border: 1px solid #ccc;
                    padding: 20px;
                    margin: 20px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
                }}
                .recepta-card table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .recepta-card th, .recepta-card td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .recepta-card th {{
                    background-color: #f2f2f2;
                }}
                .recepta-card img {{
                    width: 100px;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }}
            </style>
            <div class="recepta-card">
                <h2>{encapcalat['Titol']}</h2>
                <h4>ID Recepta: {encapcalat['ID_Recepte']}</h4>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 10%;">Número</th>
                            <th style="width: 20%;">Imatge</th>
                            <th style="width: 70%;">Pas</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for pas in passos:
                imatge_html = ""
                if pas['Imatge']:
                    imatge_html = f'<img src="data:image/png;base64,{pas["Imatge"]}" alt="Imatge del pas {pas["Numero"]}"/>'
                else:
                    imatge_html = "No hi ha imatge"

                html += f"""
                <tr>
                    <td>{pas['Numero']}</td>
                    <td>{imatge_html}</td>
                    <td>{pas['Pas']}</td>
                </tr>
                """

            html += """
                    </tbody>
                </table>
            </div>
            """
            return html

        # Genera el HTML de la taula
        card_html = crear_taula_html_protocol2(encapcalat, passos)

        # Assegura que Streamlit processi el codi HTML correctament
        st.markdown(card_html, unsafe_allow_html=True)

