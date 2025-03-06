from altres.imports import *


st.set_page_config(layout="wide")




# Carregar Font Awesome
font_awesome()

#Comença la capçalera
# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)


# Mostrar resultats en diverses columnes
col1, col2, col3, col4 = st.columns([2, 1, 3, 1])
with col1:
    # Mostrar la imatge com a enllaç clicable
    # Mostrar el div estilitzat amb text
    st.markdown(
        f"""
        <a href="/crear" style="text-decoration: none;">
            <div style="border: 1px solid red; background-color: red; border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: center;">
                Les Receptes de Mamen
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with col2:
    query = "SELECT * FROM Receptes"
    df = pd.read_sql(query, conn)
    count_total = df.shape[0]
    st.markdown(
        f'<div style="border: 1px solid red; border-radius: 20px; padding: 5px;"><i class="fas fa-bell"></i> {count_total}</div>',
        unsafe_allow_html=True)
# Mostrar recompte total amb icona
df = pd.read_sql("SELECT Temps FROM Receptes", conn)
# Crear intervals amb pandas
intervals = [0, 10, 60, float("inf")]
etiquetes = ["Menor de 10", "Entre 10 y 60", "Superior a 60"]
df["intervals"] = pd.cut(df["Temps"], bins=intervals, labels=etiquetes, right=True)
# Comptar registres per interval
resultat = df["intervals"].value_counts(sort=False)
resultat_df = resultat.reset_index()
resultat_df.columns = ["Etiqueta", "Nombre de registres"]
# Definir una llista d'icones per a cada etiqueta
emojis = {
    "Menor de 10": "🟢",
    "Entre 10 y 60": "🟠",
    "Superior a 60": "🔴"}
dificultat = {
    "Menor de 10": "Curt",
    "Entre 10 y 60": "Mitjà",
    "Superior a 60": "Llarg"

}

query_params = st.query_params
dificultat_text = query_params.get('dificultat', ['Sense dades'])[0]
interval_mapping = {
    "Curt": (0, 60),
    "Mitjà": (60, 120),
    "Llarg": (120, 240)
}
slider_range = interval_mapping.get(dificultat_text, (0, 240))  # Assignar el rang segons el paràmetre

with col3:
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in resultat_df.iterrows():
        col = columns[idx % num_columns]
        emoji = emojis.get(row['Etiqueta'], "✅")  # Definir un emoji de fall back
        dificultat_text = dificultat.get(row['Etiqueta'], "Desconeguda")  # Definir un emoji de fall back
        with col:
            st.markdown(f"""
            <a href="?dificultat={dificultat_text}" target="_self" style="text-decoration: none;">
                <div style="
                    border: 1px solid red;
                    padding: 5px;
                    border-radius: 10px;
                    text-align: center;
                    background-color: #f9f9f9;
                    font-weight: bold;">
                    {emoji} {row['Nombre de registres']} {dificultat_text}
                </div>
            </a>
            """, unsafe_allow_html=True)

temps_prep = st.slider(
    "Selecciona el temps de preparació (en minuts):",
    min_value=0,
    max_value=240,
    value=slider_range,
    step=1)

with col4:
    st.markdown(
        f"""
    <a href="/crear" style="text-decoration: none;">
        <div style="border: 1px solid red; background-color: orange; border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white;">
        + Recepte
        </div>
    </a>   
    """,
    unsafe_allow_html=True)




separador()
st.text("")
#Acaba la capçalera
#_____________________________________________________________________________
#Començcen els filtres

#connexio a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

# Obtenir la llista d'ingredients
llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)



col1, col2, col3 = st.columns(3)


# Injectar CSS personalitzat per als elements individuals
st.markdown("""
    <style>
        .custom-element {
            border: 1px solid red; /* Contorn vermell */
            border-radius: 10px; /* Cantonades arrodonides */
            padding: 10px; /* Espai intern */
            margin-bottom: 20px; /* Espai entre elements */
            background-color: #f9f9f9; /* Fons gris clar */
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Crear elements amb contorns individuals
# Primer element
with col1:
    st.markdown("Selecciona:", unsafe_allow_html=True)
    categoria = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Segon element
with col2:
    st.write("Selecciona l'ingredient (poden ser varios):")  # Text que estarà dins del contorn
    ingredients_seleccionats = st.multiselect('', llista_ingredients)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tercer element
# with col3:
#     st.write("Selecciona el Temps Total:")  # Text que estarà dins del contorn
#     temps_prep = st.slider('', 0, 240, value=slider_range, step=1)
#     st.markdown('</div>', unsafe_allow_html=True)
#Acaben els filtres
# ________________________________________________

#Definir la consulta SQL amb els paràmetres necessaris
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
    params.extend(slider_range)

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

# Mostrar els registres com a targetes
num_columns = 4

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
