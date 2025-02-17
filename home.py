import os
import sys
import base64
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from altres.funcions import estils_marc
from altres.funcions import background_home
from altres.variables import cami_db
import sqlitecloud



# #___________________________________________________________
# sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

#___________________________________________________
#Conectar a la base de dades usant la variable db_path pip install sqlitecloud



conn = sqlitecloud.connect(cami_db)


cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"


cursor.execute(query)
num_registres = cursor.fetchone()[0]

cursor.execute(query)
result = cursor.fetchone()

#_______________________________________________________
# Afegir text dins d'un marc amb l'estil definit
text_personalitzat = "Receptes"

st.markdown(f'''
<div class="marco">
        <div class="text-personalitzat">{text_personalitzat}</div>
        <div class="resultat">{num_registres}</div>
</div>''', unsafe_allow_html=True)

conn.commit()

#_____________________________

background_home()
estils_marc()
# _________________________________________________________________________

