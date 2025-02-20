from altres.imports import *


st.set_page_config(layout="wide")

rellotge()
#___________________________________________________________________________________
st.header('Filtre de Receptes')
#______________________________________________________________________________________
base64_image, cropped_image = cropping()
banner(base64_image)
#_____________________________________________________________________________
#connexio a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

# Obtenir la llista d'ingredients
llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

# Widgets de Streamlit per obtenir les condicions
st.text("")
st.text("")

#_______________________________________________________

# CSS per canviar la mida de la lletra del nom de la variable
lletra_variable()

#____________________________________________________________

# Utilitza HTML per aplicar la classe CSS al títol
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
categoria = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona un valor:</p>', unsafe_allow_html=True)
temps_prep = st.slider('', 0, 240, (0, 240), step=1)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
ingredients_seleccionats = st.multiselect('',llista_ingredients)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

#___________________________________________________________

# Definir la consulta SQL amb els paràmetres necessaris
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Observacions, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps, Receptes.Etiquetes,
    GROUP_CONCAT(Ingredients.nom || ' (' || Ingredients.quantitat || ')', ', ') AS components
    FROM Receptes
    LEFT JOIN ingredients
    ON Receptes.ID_Recepte = ingredients.ID_Recepte
'''

params = []
conditions = []

# Afegir condicions a la consulta SQL
if 'Tots' not in categoria:
    conditions.append("Receptes.Categoria IN ({})".format(', '.join('?' * len(categoria))))
    params.extend(categoria)

if temps_prep != (0, 240):
    conditions.append("Receptes.Preparacio BETWEEN ? AND ?")
    params.extend([temps_prep[0], temps_prep[1]])

if ingredients_seleccionats:
    ingredient_conditions = []
    for ing in ingredients_seleccionats:
        ingredient_conditions.append("ingredients.nom LIKE ?")
        params.append(f'%{ing}%')
    conditions.append("(" + " OR ".join(ingredient_conditions) + ")")

if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += " GROUP BY Receptes.ID_Recepte"


cursor.execute(query, params)
resultados = cursor.fetchall()

#____________________________________________________________________
agregar_estilos_css()

# Bucle a través dels resultats per crear targetes
for resultado in resultados:
    data = {
        'ID_Recepte': resultado[0],
        'Data_formatejada': resultado[1],
        'Titol': resultado[2],
        'Observacions': resultado[3],
        'Categoria': resultado[4],
        'Preparacio': resultado[5],
        'Etiquetes': resultado[8],
        'img_base64': convert_blob_to_base64(resultado[6]),
        'Temps': resultado[7],
        'components': ', '.join(obtenir_emoji(resultado[9]))  # Convertir components a cadena amb emojis
    }
    # crear la targeta amb l'opció seleccionada
    card_html = crear_tarjeta_html(data)
    st.markdown(card_html, unsafe_allow_html=True)

# Tancar la connexió a la base de dades
conn.close()
