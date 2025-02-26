from altres.funcions import dataframe_estadistiques
from altres.imports import *

st.set_page_config(layout="wide")


# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________
rellotge()

#___________________________________________________________________________________
base64_image, cropped_image = cropping()
banner(base64_image)
#_________________________________________________________________________________________
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"

cursor.execute(query)
num_registres = cursor.fetchone()[0]


#_______________________________________________________
# Afegir text dins d'un marc amb l'estil definit
text_personalitzat = f"Portem {num_registres} receptes acumulades"

st.write("")
st.subheader(f"{text_personalitzat}")
conn.commit()

#______________________________________________________________

# query = f'SELECT ID_Recepte, Titol FROM Receptes;'
#
# cursor.execute(query)
# registres = cursor.fetchall()
#
# # Obtenir els tres últims registres utilitzant slicing
# ultims_registres = registres[-3:]
#
# separador()
#
# st.subheader("Aquestes son les ultimes 3")
#
# for i, registre in enumerate(ultims_registres, start=1):
#     data = {
#         'ID_Recepte': registre[0],
#         'Titol': registre[1],
#     }
#     card_html = crear_tarjeta_html_resumida(data)
#     st.markdown(card_html, unsafe_allow_html=True)
separador()
query = 'SELECT ID_Recepte, Titol, Data_formatejada, Observacions, Preparacio, Temps FROM Receptes ORDER BY ID_Recepte DESC LIMIT 3'
df = pd.read_sql(query, conn)
df['Observacions'] = df['Observacions'].apply(process_observacions)

st.subheader("Aquestes son les 3 ultimes")

# Aplica l'estil de les files i les columnes
styled_df = df.style.apply(row_style, axis=1)

# Genera l'HTML estilitzat
html = styled_df.hide(axis='index').to_html()
html = html.replace('<style type="text/css">',
                    '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

# Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
taula = dataframe_estadistiques(html)

# Mostra el DataFrame estilitzat utilitzant Streamlit
st.components.v1.html(taula, height=200, scrolling=True)

separador()

