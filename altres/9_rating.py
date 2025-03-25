from altres.imports import *

st.set_page_config(layout="wide")

# Carregar Font Awesome
font_awesome()


st.logo(
    "imagenes/designer.png",
    link="https://elnourepositori.streamlit.app/",
    size="large"
)
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



separador()
st.text("")
#Acaba la capçalera



#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

#__________________________________________________________
lletra_variable()

st.markdown('<div class="custom-element"><p class="custom-title">Registre per valorar:</p>', unsafe_allow_html=True)
id_to_update = st.number_input("", min_value=18, step=1)

# Mostrar informació dels registres seleccionats
registre = (id_to_update,)
st.write(f"El registre seleccionat per actualitzar és: {id_to_update}")

# Mostrar informació dels registres seleccionats
query = ('SELECT ID_Recepte, '
         'Titol, '
         'Observacions, '
         'Etiquetes, '
         'Categoria, '
         'Preparacio, '
         'Temps '
         'FROM Receptes WHERE ID_Recepte = ?')

cursor.execute(query, registre)
record = cursor.fetchone()

data = {'ID_Recepte': record[0],
        'Titol': record[1],
        }
card_html = crear_tarjeta_html_resumida(data)
st.markdown(card_html, unsafe_allow_html=True)
separador()

accio = "fet"
today = date.today()


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="custom-element"><p class="custom-title">Accio:</p>', unsafe_allow_html=True)
    st.write(accio)

with col2:
       # Mostrem el títol amb estil personalitzat
    st.markdown('<div class="custom-element"><p class="custom-title">Rating:</p></div>', unsafe_allow_html=True)

    # Slider per seleccionar un valor (seguim mostrant un slider)
    slider_value = st.slider("", min_value=0, max_value=5, step=1)

    # Convertim el valor del slider en text (simulació del text de Rating)
    if slider_value == 0:
        Rating = "Molt dolent"
    elif slider_value == 1:
        Rating = "Dolent"
    elif slider_value == 2:
        Rating = "Regular"
    elif slider_value == 3:
        Rating = "Acceptable"
    elif slider_value == 4:
        Rating = "Bé"
    else:
        Rating = "Molt bé"



with col3:
    st.markdown('<div class="custom-element"><p class="custom-title">Data:</p>',
                unsafe_allow_html=True)
    data_accio = st.date_input('', today)


st.markdown('<div class="custom-element"><p class="custom-title">Resenya:</p>', unsafe_allow_html=True)
Resenya = st.text_area("")

if st.button('Guardar'):

    cursor.execute('INSERT INTO Accions (ID_Recepte, Accio, Resenya, Rating, Data_accio) VALUES (?, ?, ?, ?, ?)',
               (record[0],accio, Resenya, Rating, data_accio))
    conn.commit()
    st.subheader("Valoracio actualitzada")

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Accio, Resenya, Rating, Data_accio FROM Accions WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[id_to_update])
    df["ID_Recepte"] = df["ID_Recepte"].astype(str)
    # Justificar la columna 'Ciudad' a la izquierda
    df_styled = df.style.set_properties(subset=["ID_Recepte", "Data_accio"], **{'text-align': 'left'})
    st.dataframe(df_styled, hide_index=True, width=1500)