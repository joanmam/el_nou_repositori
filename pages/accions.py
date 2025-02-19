import sqlitecloud
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from datetime import date
from io import BytesIO, StringIO
from PIL import Image
import pandas as pd
import base64
import io
import requests
from streamlit import date_input
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_resumida
from altres.funcions import agregar_estilos_css, crear_tarjeta_html_fet
from altres.funcions import lletra_variable
from altres.funcions import rellotge
from altres.funcions import banner
from altres.funcions import separador
from altres.variables import cami_db
import emoji
import sqlitecloud
from altres.funcions import cropping
from altres.funcions import row_style
from altres.funcions import dataframe_accions

st.set_page_config(layout="wide")


# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________

rellotge()
st.header("Accions")
base64_image, cropped_image = cropping()
banner(base64_image)

#___________________________________________________________________________________



#_________________________________________________________________________________________


#__________________________________________________________
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Accio:</p>', unsafe_allow_html=True)
accio = st.text_input("")
today = date.today()
st.markdown('<div class="custom-element"><p class="custom-title">Data:</p>', unsafe_allow_html=True)
data_accio = st.date_input('', today)




# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres:</p>', unsafe_allow_html=True)
ids_to_action = st.text_input("", "1")
n_limit = 5



if st.button('**Resum**'):
    df_insert = pd.DataFrame({
        'ID_Recepte': [ids_to_action],
        'Accio': [accio],
        'Data_accio': [data_accio]
    })

    # Convertir el DataFrame a una llista de tuples
    records = df_insert.to_records(index=False).tolist()

    # Inserir els registres directament a la taula Accions utilitzant SQL
    query_insert = "INSERT INTO Accions (ID_Recepte, Accio, Data_accio) VALUES (?, ?, ?)"
    conn.executemany(query_insert, records)
    conn.commit()

    query2 = """
        SELECT Accions.ID_Accions, Receptes.Titol, Accions.Accio, Accions.Data_accio
        FROM Receptes
        JOIN Accions ON Receptes.ID_Recepte = Accions.ID_Recepte
        WHERE Receptes.ID_Recepte = ?
        ORDER BY Accions.ID_Accions DESC
        LIMIT ?
    """
    df = pd.read_sql(query2, conn, params=[ids_to_action, n_limit])

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1)



    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_accions(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.components.v1.html(taula, height=600, scrolling=True)

conn.close()