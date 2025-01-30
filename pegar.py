import sqlite3
import streamlit as st

# Connecta a la base de dades
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
cursor = conn.cursor()

# Consulta SQL per comptar el nombre de registres
query = "SELECT COUNT(*) FROM Receptes"

# Executa la consulta
cursor.execute(query)
num_registres = cursor.fetchone()[0]

# Aplica el CSS utilitzant st.write per assegurar la mida de la font
st.write(f"""
    <div style='
        display: flex;
        justify-content: center;
        align-items: center;
        width: 300px;
        height: 300px;
        border: 5px solid #000000;  /* Afegir un marc */
        border-radius: 15px;  /* Bordes arrodonits */
        font-size: 48px;  /* Augmenta la mida de la font */
        font-weight: bold;
        color: #000000;  /* Color del text */
        background-color: #FFFFFF;  /* Fons blanc */
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);  /* Una mica d'ombra per a millorar la visibilitat */
        text-align: center;
        line-height: 300px;  /* Assegura que el text estigui centrat verticalment */
    '>
        {num_registres}
    </div>
""", unsafe_allow_html=True)

# Tanca la connexió a la base de dades
conn.close()

