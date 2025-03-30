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


# Carregar Font Awesome
font_awesome()

#Comença la capçalera
# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)


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

#Les ultimes receptes
query = 'SELECT ID_Recepte, Titol, Data_formatejada, Observacions, Preparacio, Temps FROM Receptes ORDER BY ID_Recepte DESC LIMIT 10'
df = pd.read_sql(query, conn)
df['Observacions'] = df['Observacions'].apply(process_observacions)

st.subheader("Aquestes son les 10 ultimes")

# Aplica l'estil de les files i les columnes
styled_df = df.style.apply(row_style, axis=1)

# Genera l'HTML estilitzat
html = styled_df.hide(axis='index').to_html()
html = html.replace('<style type="text/css">',
                    '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

# Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
taula = dataframe_estadistiques(html)

# Mostra el DataFrame estilitzat utilitzant Streamlit
st.components.v1.html(taula, height=400, scrolling=True)

separador()

#final de les ultimes receptes

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)


#Acaba la capçalera



max_passos = 10

# Inicialitzar variables de sessió
if 'num_passos' not in st.session_state:
    st.session_state.num_passos = max_passos

if 'imatges' not in st.session_state:
    st.session_state.imatges = [None] * max_passos

if 'passos' not in st.session_state:
    st.session_state.passos = [None] * max_passos

# Connexió a la base de dades (ajusta la teva base de dades aquí)
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

# Obtenir els IDs de la recepte per introduir els passos
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Recepte seleccionada:</p>', unsafe_allow_html=True)
recepte_seleccionada = st.number_input("", min_value=3, step=1)

st.write(f"La recepte seleccionada per afegir passos es la numero **{recepte_seleccionada}**")


for i in range(st.session_state.num_passos):
    separador()
    st.write("")
    st.write("")
    lletra_variable()
    st.markdown(f'<div class="custom-element"><p class="custom-title">Pas: {i+1}</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 7])

    with col1:
        lletra_variable()
        st.markdown('<div class="custom-element2"><p class="custom-title2">Imatge:</p>', unsafe_allow_html=True)
        image = st.text_input("Puja una URL imatge", )

        if image is not None:
            st.session_state.imatges[i] = image

    with col2:
        lletra_variable()
        st.markdown('<div class="custom-element2"><p class="custom-title2">Pas:</p>', unsafe_allow_html=True)
        pas = st.text_area(f"", key=f"pas_{i}")

        if pas:
            st.session_state.passos[i] = pas

    # Botó per aturar el bucle
    if st.button(f"Aturar després del pas {i + 1}"):
        st.session_state.num_passos = i + 1
        break

separador()

if st.button("Guardar", key="save_data"):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    cursor.execute('''
        INSERT INTO Passos (ID_Recepte, Numero, Data_passos, Pas, URL_passos) VALUES (?, ?, ?, ?, ?)
    ''', (recepte_seleccionada, i+1, current_date, pas, image))

    conn.commit()
    st.success("Guardado")

    # Reinicialitzar les llistes i establir el nombre de passos segons el punt d'aturada
    st.session_state.imatges = [None] * max_passos
    st.session_state.passos = [None] * max_passos
    st.session_state.num_passos = max_passos

    # Reinicialitzar break_loop per evitar crear elements posteriors
    break_loop = False

#________________________________

query = ('SELECT Receptes.ID_Recepte, '
         'Receptes.Titol, '
         'Passos.Numero, '
         'Passos.Pas '
         'FROM Receptes '
         'JOIN Passos '
         'ON Receptes.ID_Recepte = Passos.ID_Recepte '
         'WHERE Receptes.ID_Recepte = ?;')

cursor.execute(query, (recepte_seleccionada,))
records = cursor.fetchall()
for record in records:
    data = {'ID_Recepte': record[0],
            'Titol': record[1],
            'Numero': record[2],
            'Pas': record[3]
    }
    card_html = crear_tarjeta_html_pas(data)
    st.markdown(card_html, unsafe_allow_html=True)