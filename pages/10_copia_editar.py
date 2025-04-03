from PIL.FontFile import WIDTH

from altres.imports import *

st.set_page_config(layout="wide")

# Carregar Font Awesome
font_awesome()

def render_image(Imatge):
    return f'<img src="{Imatge}" width="150">'

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
elif selection1 == "editar_copy":
    st.switch_page("pages/10_copia_editar.py")
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
#_____________________________________________________________________________
#connexio a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()


# Realizar consulta SQL para obtener registros
query = "SELECT * FROM Receptes"
df = pd.read_sql(query, conn)

df["Imatge_text"] = df["Imatge"]
df_visible = df.drop(columns=["blob", "Preparacio", "Temps", "Data_formatejada"])  # Quita las columnas antes de mostra


column_order = ["ID_Recepte", "Titol", "Imatge_text", "Imatge", "Observacions", "Etiquetes", "Categoria"]
df_visible = df_visible[column_order]


# Configurar columnas del DataFrame
with st.container():
    edited_df = st.data_editor(
        df_visible,
        column_config={
            "ID_Recepte": st.column_config.NumberColumn(
                label="ID",
            ),
            "Titol": st.column_config.TextColumn(
                label="Titol",
            ),
            "Imatge_text": st.column_config.TextColumn(
                label="URL",
            ),
            "Imatge": st.column_config.ImageColumn(
                label="Vista previa",
                help="Imagenes"
            ),
            "Observacions": st.column_config.TextColumn(
                label="Observacions",
            ),
            "Etiquetes": st.column_config.TextColumn(
                label="Etiquetes",
            ),
            "Categoria": st.column_config.TextColumn(
                label="Categoria",
            ),
        },
        hide_index=True,
        use_container_width=True)

# Botón para actualizar cambios en SQLiteCloud
if st.button("Actualitzar"):
    for index, row in edited_df.iterrows():
        query_update = f"""
        UPDATE Receptes 
        SET Titol = '{row["Titol"]}',
            Imatge = '{row["Imatge_text"]}',
            Observacions = '{row["Observacions"]}',
            Etiquetes = '{row["Etiquetes"]}',
            Categoria = '{row["Categoria"]}'
        WHERE ID_Recepte = {row["ID_Recepte"]}
        """
        conn.execute(query_update)  # Ejecutar el UPDATE en SQLiteCloud

    conn.commit()  # Guardar cambios
    st.success("¡Datos actualizados correctamente en SQLiteCloud! 🎉")

    query = "SELECT ID_Recepte, Imatge, Titol, Observacions, Etiquetes, Categoria FROM Receptes"
    update_df = pd.read_sql(query, conn)

    # Configurar columnas del DataFrame
    with st.container():
        update_df = st.dataframe(
            update_df,
            column_config={
                "ID_Recepte": st.column_config.NumberColumn(
                    label="ID",
                ),
                "Titol": st.column_config.TextColumn(
                    label="Titol",
                ),
                "Imatge": st.column_config.ImageColumn(
                    label="Vista previa",
                    help="Imagenes"
                ),
                "Observacions": st.column_config.TextColumn(
                    label="Observacions",
                ),
                "Etiquetes": st.column_config.TextColumn(
                    label="Etiquetes",
                ),
                "Categoria": st.column_config.TextColumn(
                    label="Categoria",
                ),
            },
        hide_index=True,
        use_container_width=True)
