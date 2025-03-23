from altres.imports import *



st.set_page_config(layout="wide")

st.logo(
    "imagenes/designer.png",
    link="https://elnourepositori.streamlit.app/",
    size="large"
)


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
        Data = st.date_input("Seleccionar data")

    with col2:
        Titol = st.text_input("Titol")

    st.markdown("---")  # Separador

    foto = st.file_uploader("Elige",type=["jpg","png"])
    st.markdown("---")  # Separador

    col3, col4 = st.columns(2)
    with col3:
        Categoria = st.selectbox("Selecciona", ["Plato unico","Acompañamiento", "Primero", "Segundo"])
        st.markdown("---")  # Separador

    with col4:
        tags = st.text_input("Etiquetes")
        st.markdown("---")  # Separador

    Observacions = st.text_area("Observacions")
    st.markdown("---")  # Separador

    col5, col6 = st.columns(2)
    with col5:
        st.write("Temps de preparacio")
        Hores_prep = st.number_input("Hores", step=1, key="hores_preparacio")
        Minuts_prep = st.number_input("Minuts", step=1, key="minuts_preparacio")

    with col6:
        st.write("Temps total")
        Hores = st.number_input("Hores", step=1, key="hores_totals")
        Minuts = st.number_input("Minuts", step=1, key="minuts_totals")

    enviar = st.form_submit_button()
    if enviar:
        if foto is not None:
            foto_bytes = foto.read()
            img = Image.open(BytesIO(foto_bytes))
            st.image(img)
            buffer = BytesIO()
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(buffer, format="JPEG")
            blob = buffer.getvalue()
            Etiquetes = ', '.join([tag.strip() for tag in tags.split(',')])
            Data_formatejada = Data.strftime("%d-%m-%Y")

            Temps = Hores * 60 + Minuts
            Preparacio = Hores_prep * 60 + Minuts_prep


            sql = ("INSERT INTO Receptes (Data_formatejada, Titol, Observacions, Etiquetes, blob, Temps, Preparacio, Categoria)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            datos = Data_formatejada, Titol, Observacions, Etiquetes, blob, Temps, Preparacio, Categoria
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