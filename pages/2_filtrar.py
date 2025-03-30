from altres.imports import *


st.set_page_config(layout="wide")




#barra lateral
pages_dir = Path("pages/")
archivos_filtrados1 = [
    archivo.stem.split("_", 1)[-1]
    for archivo in pages_dir.iterdir()
    if archivo.name != "__pycache__"
       and "ext" not in archivo.name
       and not archivo.name.startswith(("5", "6"))
]
archivos_filtrados2 = [
    archivo.stem.split("_", 1)[-1]
    for archivo in pages_dir.iterdir()
    if archivo.name != "__pycache__"
       and "ext" in archivo.name
]
archivos_filtrados3 = [
    archivo.stem.split("_", 1)[-1]
    for archivo in pages_dir.iterdir()
    if archivo.name != "__pycache__"
       and  archivo.name.startswith(("5", "6"))
]

# Agregar una opción neutral al inicio del menú
opciones1 = ["Selecciona una opción"] + archivos_filtrados1
opciones2 = ["Selecciona una opción"] + archivos_filtrados2
opciones3 = ["Selecciona una opción"] + archivos_filtrados3
# Crear el radio con la opción neutral
selection1 = st.sidebar.radio("General", opciones1, index=0)
selection2 = st.sidebar.radio("Externs", opciones2, index=0)
selection3 = st.sidebar.radio("Passos", opciones3, index=0)
# Manejar el caso en el que no se ha seleccionado ninguna opción significativa
if selection1 == "crear":
    st.switch_page("pages/1_crear.py")
elif selection1 == "filtrar":
    st.switch_page("pages/2_filtrar.py")
elif selection1 == "editar":
    st.switch_page("pages/3_editar.py")
elif selection1 == "borrar":
    st.switch_page("pages/4_borrar.py")
else:
    st.write("")
# Manejar el caso en el que no se ha seleccionado ninguna opción significativa
if selection2 == "recetas_externas":
    st.switch_page("pages/7_recetas_externas.py")
elif selection2 == "biblioteca_externa":
    st.switch_page("pages/8_biblioteca_externa.py")
else:
    st.write("")

if selection3 == "passos":
    st.switch_page("pages/5_passos.py")
elif selection3 == "protocol":
    st.switch_page("pages/6_protocol.py")
else:
    st.write("")

#_fi barra lateral____________________________


agregar_iconos_google()

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
            <div style="border: 1px solid red; background-color: red; background: linear-gradient(90deg, red, yellow);
border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: center;">
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
    "Entre 10 y 50": "🟠",
    "Superior a 60": "🔴"}
dificultat = {
    "Menor de 10": "Curt",
    "Entre 10 y 60": "Mitjà",
    "Superior a 60": "Llarg"

}


# Definir una llista d'icones per a cada etiqueta
emojis = {
    "Menor de 10": "🟢",
    "Entre 10 y 60": "🟠",
    "Superior a 60": "🔴"}
dificultats = {
    "Menor de 10":  (0, 10),
    "Entre 10 y 60": (10, 60),
    "Superior a 60": (60, 240)

}

# Definir les tres variables inicialment
temps_1 = (0, 10)
temps_2 = (10, 60)
temps_3 = (60, 240)

query_params = st.query_params
temps_seleccionat = query_params.get("temps", [None])[0]

# Assignar la variable temps segons el paràmetre seleccionat
if temps_seleccionat == "1":
    temps = temps_1
elif temps_seleccionat == "2":
    temps = temps_2
elif temps_seleccionat == "3":
    temps = temps_3
else:
    temps = (0, 240)  # Valor predeterminat si no hi ha selecció


with col3:
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in resultat_df.iterrows():
        col = columns[idx % num_columns]
        emoji = emojis.get(row['Etiqueta'], "✅")
        dificultat_text = row['Etiqueta']

        with col:
            st.markdown(f"""
            <a href="?temps={idx + 1}" style="text-decoration: none;">
                <div style="border: 1px solid red; border-radius: 20px; padding: 5px;
                            background-color: #f9f9f9; color: black; font-weight: bold;
                            text-align: center; cursor: pointer;">
                    {emoji} {row['Nombre de registres']} {dificultat_text}
                </div>
            </a>
            """, unsafe_allow_html=True)

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

#Crear elements amb contorns individuals
#Primer element
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
with col3:
    st.write("Selecciona el Temps Total:")  # Text que estarà dins del contorn
    temps_act = st.slider('', 0, 240, value=temps, step=1)
    st.markdown('</div>', unsafe_allow_html=True)
#Acaben els filtres
# ________________________________________________
 # Captura del paràmetre URL
query_params = st.query_params
temps_seleccionat = query_params.get("temps", [None])[0]


#Definir la consulta SQL amb els paràmetres necessaris
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Categoria, Receptes.Preparacio, Receptes.URL_Imatge, Receptes.Temps,
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

# Afegir condició SQL segons el temps seleccionat
if temps != (0, 240):  # Només si el rang no és per defecte
    conditions.append("Receptes.Temps BETWEEN ? AND ?")
    params.extend([temps[0], temps[1]])

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
num_columns = 2
columns = st.columns(num_columns)



for i, row in df.iterrows():
    col = columns[i % num_columns]  # Seleccionar columna

    with col:
        # Generem la targeta HTML
        targeta_html = generar_html_fontawesome2(
            ID_Recepte=row['ID_Recepte'],
            titol=row['Titol'],
            data_formatejada=row['Data_formatejada'],  # Data formatejada
            imatge_url=row['URL_Imatge'],  # URL de la imatge
            ingredients=row['components'],  # Ingredients
            temps_preparacio=row['Preparacio'],  # Temps de preparació
            temps_act=row["Temps"]  # Temps total
        )

        # Mostrar la targeta a Streamlit
        st.markdown(targeta_html, unsafe_allow_html=True)




# Tancar la connexió a la base de dades
conn.close()



#

col1, col2, col3, col4, col5 = st.columns(5)
with col3:


    # HTML i CSS per centrar el botó
    st.markdown(
        """
        <div style="justify-content: center; align-items: center; height: 100vh;">
            <a href="/editar" style="text-decoration: none;">
                <div style="border: 1px solid red; background-color: green; border-radius: 18px; padding: 10px 20px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: center;">
                    Editar
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # HTML i CSS per centrar el botó
    st.markdown(
        """
        <div style="justify-content: center; align-items: center; height: 100vh;">
            <a href="/editar" style="text-decoration: none;">
                <div style="border: 1px solid red; background-color: green; border-radius: 18px; padding: 10px 20px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: center;">
                    Editar
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
