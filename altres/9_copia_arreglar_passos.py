from altres.imports import *

st.set_page_config(layout="wide")

# Carregar Font Awesome
font_awesome()

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
    st.switch_page("pages/3_copia_editar.py")
elif selection1 == "borrar":
    st.switch_page("pages/4_borrar.py")
elif selection1 == "arreglar_passos":
    st.switch_page("pages/9_copia_arreglar_passos.py")
elif selection1 == "copia_editar":
    st.switch_page("pages/10_editar.py")
elif selection1 == "copia_arreglar_passos":
    st.switch_page("pages/11_arreglar_passos.py")
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



query = "SELECT ID_Recepte, Imatge, Titol, Observacions, Etiquetes, Categoria, Preparacio, Temps FROM Receptes WHERE ID_Recepte = ?"

df = pd.read_sql(query, conn, params=[id_to_update])

df['Observacions'] = df['Observacions'].apply(lambda x: process_observacions(x))


# Configurar columnas del DataFrame
with st.container():
    st.dataframe(
        df,
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
            "Categoria": st.column_config.SelectboxColumn(
                label="Categoria",
                options=["Plato único", "Acompañamiento", "Primero", "Segundo"]
            ),
        },
        hide_index=True,
        use_container_width=True)






# # Mostra les dades existents
# st.subheader('Dades actuals dels registres')
# # Aplica l'estil de les files i les columnes
# styled_df = df.style.apply(row_style, axis=1)
# df.columns = ['ID_Recepte', 'Imatge', 'Titol', 'Observacions', 'Etiquetes', 'Categoria','Preparacio', 'Temps']
#
# # Genera l'HTML estilitzat
# html = styled_df.hide(axis='index').to_html()
# html = html.replace('<style type="text/css">',
#                     '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')
#
# # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
# taula = dataframe_actualitzar(html)
#
# # Mostra el DataFrame estilitzat utilitzant Streamlit
# st.components.v1.html(taula, height=200, scrolling=True)
# separador()
#
# st.subheader("Nous valors passos")
#
# query2 = "SELECT ID_Recepte, URL_passos, Pas FROM Passos WHERE ID_Recepte = ?"
# df2 = pd.read_sql(query2, conn, params=[id_to_update])
# df2.columns = ["ID_Recepte", "Imatge_passos", "Pas"]
# df2['Imatge_passos'] = '<img src="' + df2['Imatge_passos'] + '" style="width:150px; height:auto;">'
#
# valors_fila = df2.loc[df2["ID_Recepte"] == id_to_update]
#
# nou_Pas = st.text_input("Nou Pas", value=valors_fila.iloc[0]["Pas"])
# nova_Imatge = st.text_input("Nova Imatge", value=valors_fila.iloc[0]["Imatge_passos"])
#
# # Botó per actualitzar
# if st.button("Actualitzar"):
#     # Comprovar que l'ID no és buit
#     if id_to_update:
#         # Convertir l'ID a tipus enter
#         id_to_update = int(id_to_update)
#
#         # Llegeix les dades existents a la taula "Receptes"
#         df = pd.read_sql_query("SELECT * FROM Passos", conn)
#         df.columns = ["ID_Receptes", "Imatge_passos", "Pas"]
#         # Comprova que l'ID existeix a la taula
#         if id_to_update in df['ID_Recepte'].values:
#             # Actualitza les columnes proporcionades
#
#             if nou_Pas:
#                 df.loc[df['ID_Recepte'] == id_to_update, 'Pas'] = nou_Pas
#             if nova_Imatge:
#                 df.loc[df['ID_Recepte'] == id_to_update, 'Imatge_passos'] = nova_Imatge
#                 df['Imatge_passos'] = '<img src="' + df['Imatge_passos'] + '" style="width:150px; height:auto;">'
#             # Genera un nom únic per a la taula temporal
#             temp_table_name = f"Passos_temp_{uuid.uuid4().hex}"
#
#             # Guarda només les dades actualitzades a la taula temporal
#             df_actualitzat = df[df['ID_Recepte'] == id_to_update]
#             df_actualitzat.to_sql(temp_table_name, conn, if_exists='replace', index=False)
#
#             # Actualitza la taula original
#             conn.execute(f"DELETE FROM Passos WHERE ID_Recepte = ?", (id_to_update,))
#             conn.commit()
#
#             conn.execute(f"INSERT INTO Passos SELECT * FROM {temp_table_name}")
#             conn.commit()
#
#             # Esborra la taula temporal
#             conn.execute(f"DROP TABLE {temp_table_name}")
#             conn.commit()
#
#             # Comprova i mostra els canvis
#             df_mostrat = pd.read_sql_query("SELECT ID_Recepte, URL_passos, Pas FROM Passos WHERE ID_Recepte = ?", conn, params=[id_to_update])
#             st.subheader("Dades actualitzades:")
#
#             df_mostrat.columns = ['ID_Recepte', 'Imatge', 'Pas']
#
#
#             styled_df = df_mostrat.style.apply(row_style, axis=1)
#
#
#             # Genera l'HTML estilitzat
#             html = styled_df.hide(axis='index').to_html()
#
#             # html = html.replace('<style type="text/css">','')
#
#
#             # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
#             taula = dataframe_actualitzar(html)
#
#             # Mostra el DataFrame estilitzat utilitzant Streamlit
#             st.components.v1.html(taula, height=600, scrolling=True)
#
#         else:
#             st.write("No s'ha trobat cap registre amb aquest ID.")
#     else:
#         st.write("Si us plau, introdueix l'ID de la recepta.")
#
# conn.close()
#
#
#
