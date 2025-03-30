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

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

separador()
st.text("")
#Acaba la capçalera



receptes_seleccionades = st.text_input("Selecciona els ID de les receptes:")

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[receptes_seleccionades])





# pels passos
    query2 = "SELECT Numero, URL_passos, Pas FROM Passos WHERE ID_Recepte = ?"
    df = pd.read_sql(query2, conn, params=[receptes_seleccionades])
    # Converteix cada blob a una imatge i crea una nova columna amb les imatges

    # Transformar la columna 'URL_passos' per mostrar imatges
    df['URL_passos'] = '<img src="' + df['URL_passos'] + '" style="width:150px; height:auto;">'
    df.columns = ['Núm.', 'Imatge', 'Descripció del Pas']

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1)



    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_passos(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.components.v1.html(taula, height=600, scrolling=True)


