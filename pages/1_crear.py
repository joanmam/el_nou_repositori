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
elif selection1 == "arreglar_passos":
    st.switch_page("pages/9_arreglar_passos.py")
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

# Carregar Font Awesome
font_awesome()

#Comença la capçalera
# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

# Mostrar resultats en diverses columnes
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    # Mostrar la imatge com a enllaç clicable
    # Mostrar el div estilitzat amb text
    st.markdown(
        f"""
        <a href="/crear" style="text-decoration: none;">
            <div style="border: 1px solid red; background-color: red; background: linear-gradient(90deg, red, yellow);
 border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white; text-align: left;">
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


with col3:
    st.markdown(
        f"""
    <a href="/crear" style="text-decoration: none;">
        <div style="border: 1px solid red; background-color: orange; border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white;">
        + Recepte
        </div>
    </a>   
    """,
    unsafe_allow_html=True)

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

separador()
st.text("")
#Acaba la capçalera

#______________________________________________
ultimo_id = None
if 'ultimo_id' not in st.session_state:
    st.session_state.ultimo_id = None

st.subheader("Recepte")


with st.form(key="Form"):
    col1, col2 = st.columns(2)

    with col1:
        data = st.date_input("Seleccionar data")

    with col2:
        Titol = st.text_input("Titol")

    st.markdown("---")  # Separador
    # Subida d'imatges amb Streamlit
    uploaded_url = st.text_input("Puja una URL imatge",)



    col3, col4 = st.columns(2)
    with col3:
        categoria = st.selectbox("Selecciona categoria", ["Plato único", "Acompañamiento", "Primero", "Segundo"])
    with col4:
        tags = st.text_input("Etiquetes (separades per comes)")
    st.markdown("---")  # Separador

    observacions = st.text_area("Observacions")
    st.markdown("---")  # Separador

    col5, col6 = st.columns(2)
    with col5:
        st.write("Temps de preparació")
        hores_prep = st.number_input("Hores", step=1, key="hores_preparacio")
        minuts_prep = st.number_input("Minuts", step=1, key="minuts_preparacio")
    with col6:
        st.write("Temps total")
        hores = st.number_input("Hores", step=1, key="hores_totals")
        minuts = st.number_input("Minuts", step=1, key="minuts_totals")

    enviar = st.form_submit_button("Enviar")
    if enviar:

        # Processar dades del formulari
        data_formatejada = data.strftime("%d-%m-%Y")
        etiquetes = ', '.join([tag.strip() for tag in tags.split(',')])
        temps_total = int(hores * 60 + minuts)
        temps_preparacio = int(hores_prep * 60 + minuts_prep)

        sql = ("INSERT INTO Receptes (Data_formatejada, Titol, Observacions, Etiquetes, Imatge, Temps, Preparacio, Categoria)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
        datos = data_formatejada, Titol, observacions, etiquetes, uploaded_url, temps_total, temps_preparacio, categoria
        cursor.execute(sql, datos)
        conn.commit()

        cursor.execute('''SELECT last_insert_rowid()''')
        st.session_state.ultimo_id = cursor.fetchone()[0]
        st.write(f'El último ID asignado en la tabla Receptes es: {st.session_state.ultimo_id}')


# Crear un formulario para los ingredientes
st.subheader("Ingredients")

# Lista para almacenar temporalmente los ingredientes
if 'ingredientes' not in st.session_state:
    st.session_state.ingredientes = []

# Estil CSS per personalitzar el botó "Finalizar"
st.markdown("""
    <style>
    st.button_Finalizar {
        background-color: red;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# Formulari per afegir ingredients
with st.form(key="Form2"):
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom de l'ingredient")
        submit_button1 = st.form_submit_button("Afegir ingredient")
    with col2:
        quantitat = st.text_input('Quantitat')


    if submit_button1:
        if nom and quantitat:
            st.session_state.ingredientes.append((nom, quantitat))
        else:
            st.error("Sisplau, ompli tots dos camps.")

# Mostrar ingredients afegits en una llista acumulativa
if st.session_state.ingredientes:
    st.write("Ingredients afegits temporalment:")
    for idx, (nom, quantitat) in enumerate(st.session_state.ingredientes, start=1):
        st.write(f"{idx}. Ingredient: {nom}, Quantitat: {quantitat}")

submit_button2 = st.button("Acabar")
if submit_button2:
    if 'ultimo_id' in st.session_state:
        # Inserir ingredients a la base de dades només quan es pressiona "Finalizar"
        for nom, quantitat in st.session_state.ingredientes:
            cursor.execute('INSERT INTO ingredients (nom, quantitat, ID_Recepte) VALUES (?, ?, ?)',
                           (nom, quantitat, st.session_state.ultimo_id))
            conn.commit()

        # Fer un SELECT per mostrar els ingredients de l'última recepta
        cursor.execute('SELECT nom, quantitat FROM ingredients WHERE ID_Recepte = ?', (st.session_state.ultimo_id,))
        ingredients = cursor.fetchall()

        st.write("Ingredients de l'última recepte guardada:")
        if ingredients:
            for idx, (nom, quantitat) in enumerate(ingredients, start=1):
                st.write(f"{idx}. Ingredient: {nom}, Quantitat: {quantitat}")

        st.success("Tots els ingredients s'han guardat amb exit!")
        st.session_state.ingredientes = []

    else:
        st.error("Primer ha de guardar una recepte.")


# Tancar la connexió
conn.close()