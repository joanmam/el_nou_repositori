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

query = f'SELECT ID_Recepte, Titol FROM Receptes;'

cursor.execute(query)
registres = cursor.fetchall()

# Obtenir els tres últims registres utilitzant slicing
ultims_registres = registres[-3:]

separador()

st.subheader("Aquestes son les ultimes 3")

for i, registre in enumerate(ultims_registres, start=1):
    data = {
        'ID_Recepte': registre[0],
        'Titol': registre[1],
    }
    card_html = crear_tarjeta_html_resumida(data)
    st.markdown(card_html, unsafe_allow_html=True)
