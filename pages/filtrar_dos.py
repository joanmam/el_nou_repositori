from altres.imports import *


st.set_page_config(layout="wide")
agregar_iconos_google()



# Carregar Font Awesome
font_awesome()
# Usar un icono de Google
st.markdown(
    '<i class="material-icons">outdoor_grill</i> ¡Icono de Google!',
    unsafe_allow_html=True
)
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

col1, col2 = st.columns([1, 5])

# Col·loquem tots els elements dins del contenidor de col1
with col1:
    # Injectar CSS personalitzat per als elements individuals
    st.markdown("""
        <style>
            .custom-element {
                border: 1px solid red; /* Contorn vermell */
                border-radius: 10px; /* Cantonades arrodonides */
                padding: 10px; /* Espai intern */
                margin-bottom: 20px; /* Espai entre elements */
                background-color: #f9f9f9; /* Fons gris clar */
            }
            .custom-title {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Crear elements amb contorns individuals
    # Primer element
    st.markdown('<div class="custom-element">', unsafe_allow_html=True)
    st.markdown('<p class="custom-title">Selecciona la primera categoria:</p>', unsafe_allow_html=True)
    categoria = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Segon element
    st.markdown('<div class="custom-element">', unsafe_allow_html=True)
    st.markdown('<p class="custom-title">Selecciona la segona categoria:</p>', unsafe_allow_html=True)
    ingredients_seleccionats = st.multiselect('', llista_ingredients)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tercer element
    st.markdown('<div class="custom-element">', unsafe_allow_html=True)
    st.markdown('<p class="custom-title">Selecciona un valor:</p>', unsafe_allow_html=True)
    temps_prep = st.slider('', 0, 240, (0, 240), step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    # CSS per canviar la mida de la lletra del nom de la variable
    # lletra_variable()

    #____________________________________________________________

    # Utilitza HTML per aplicar la classe CSS al títol
    # st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
    # categoria = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
    # st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    # st.markdown('<div class="custom-element"><p class="custom-title">Selecciona un valor:</p>', unsafe_allow_html=True)
    # temps_prep = st.slider('', 0, 240, (0, 240), step=1)
    # st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    # st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)
    # ingredients_seleccionats = st.multiselect('',llista_ingredients)
    # st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

#___________________________________________________________

# Definir la consulta SQL amb els paràmetres necessaris
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps,
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

df = pd.read_sql(query, conn, params=params)


df["components"] = df["components"].apply(lambda x: ', '.join(obtenir_emoji(x)))
with col2:
    # Mostrar els registres com a targetes
    num_columns = 3

    columns = st.columns(num_columns)

    for i, row in df.iterrows():
        col = columns[i % num_columns]  # Seleccionar columna
        with col:
            # Generar la targeta amb la funció actualitzada
            targeta_html = generar_html_fontawesome(
                ID_Recepte=row['ID_Recepte'],
                titol=row['Titol'],
                data_formatejada=row['Data_formatejada'],  # Data formatejada
                imatge_base64=convert_blob_to_base64(row['blob']),  # Imatge
                ingredients=row['components'],  # Ingredients
                temps_preparacio=row['Preparacio'],  # Temps de preparació
                temps_total=row['Temps'],  # Temps total
            )

            # Mostrar la targeta a Streamlit
            st.markdown(targeta_html, unsafe_allow_html=True)




# Tancar la connexió a la base de dades
conn.close()
