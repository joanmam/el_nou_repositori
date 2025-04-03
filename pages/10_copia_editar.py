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

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

# Obtenir els IDs dels registres a actualitzar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registre per actualitzar:</p>', unsafe_allow_html=True)
id_to_update = st.number_input("", min_value=43, step=1)


# Mostrar informació dels registres seleccionats
registre = (id_to_update,)
st.write(f"El registre seleccionat per actualitzar és: {id_to_update}")

# def render_image(Imatge):
#     return f'<img src="{Imatge}" width="150">'
#
# query = "SELECT ID_Recepte, Imatge, Titol, Observacions, Etiquetes, Categoria, Preparacio, Temps FROM Receptes"
#
# df = pd.read_sql(query, conn)
#
# df['Observacions'] = df['Observacions'].apply(lambda x: process_observacions(x))
# df['Imatge'] = df['Imatge'].apply(render_image)
#
#
#
#
# st.dataframe(
#     df,
#     column_config=column_configuration,
#     use_container_width=True,
#     hide_index=True
#



# Realizar consulta SQL para obtener registros
query = "SELECT ID_Recepte, Imatge, Titol FROM Receptes"
df = pd.read_sql(query, conn)

# Configurar columnas del DataFrame
with st.container():
    edited_df = st.data_editor(
        df,
        column_config={
            "ID_Recepte": st.column_config.NumberColumn(
                label="Numero",
                width= "small" # Tamaño más compacto
            ),
            "Titol": st.column_config.TextColumn(
                label="Retitol",
                width="large"  # Tamaño más compacto

            ),
            "Imatge": st.column_config.ImageColumn(
                label="Vista previa",
                width="small",  # Tamaño más compacto
                help="Imagenes"
            )
        },
        hide_index=True,
        use_container_width=False)

# Botón para actualizar cambios en SQLiteCloud
if st.button("Actualizar en SQLiteCloud"):
    for index, row in edited_df.iterrows():
        query_update = f"""
        UPDATE Receptes 
        SET Titol = '{row["Titol"]}', Imatge = '{row["Imatge"]}'
        WHERE ID_Recepte = {row["ID_Recepte"]}
        """
        conn.execute(query_update)  # Ejecutar el UPDATE en SQLiteCloud

    conn.commit()  # Guardar cambios
    st.success("¡Datos actualizados correctamente en SQLiteCloud! 🎉")

query = "SELECT ID_Recepte, Imatge, Titol FROM Receptes"
df = pd.read_sql(query, conn)

# Configurar columnas del DataFrame
with st.container():
    update_df = st.dataframe(
        df,
        column_config={
            "ID_Recepte": st.column_config.NumberColumn(
                label="Numero",
                width= "small" # Tamaño más compacto
            ),
            "Titol": st.column_config.TextColumn(
                label="Retitol",
                width="large"  # Tamaño más compacto

            ),
            "Imatge": st.column_config.ImageColumn(
                label="Vista previa",
                width="small",  # Tamaño más compacto
                help="Imagenes"
            )
        },
        hide_index=True,
        use_container_width=False)

# Cerrar conexión

