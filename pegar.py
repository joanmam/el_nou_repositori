import streamlit as st
import pandas as pd
import sqlite3

def row_style(row):
    return ['background-color: #f0f0f0' if row.name % 2 == 0 else 'background-color: #ffffff' for _ in row]

conn = sqlite3.connect('la_teva_base_de_dades.db')  # Ajusta això segons la teva connexió

receptes_seleccionades = 1  # Ajusta això segons el teu paràmetre de selecció

def dataframe_pagina(html):
    taula = f"""
    <style>
    .dataframe-container {{
        width: 100%;
        overflow-x: auto;
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
    }}
    </style>
    <div class="dataframe-container">{html}</div>
    """
    return taula

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[receptes_seleccionades])

    # Defineix l'amplada de les columnes directament
    column_styles = [
        dict(selector=f"th.col{i}", props=[("min-width", "150px"), ("max-width", "150px")])
        for i in range(len(df.columns))
    ]

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1).set_table_styles(column_styles)

    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_pagina(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.markdown(taula, unsafe_allow_html=True)

