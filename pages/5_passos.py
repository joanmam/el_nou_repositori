from altres.imports import *


st.set_page_config(layout="wide")


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

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

separador()
st.text("")
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
        image = st.file_uploader(f"", type=["jpg", "png"], key=f"image_{i}")

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

    for i in range(st.session_state.num_passos):
        image = st.session_state.imatges[i]
        pas = st.session_state.passos[i]

        if image and pas:
            img = Image.open(image)
            buf = io.BytesIO()
            img.save(buf, format="png")
            imatge = buf.getvalue()

            cursor.execute('''
                INSERT INTO Passos (ID_Recepte, Numero, Data_passos, Imatge_passos, Pas) VALUES (?, ?, ?, ?, ?)
            ''', (recepte_seleccionada, i+1, current_date, imatge, pas))

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