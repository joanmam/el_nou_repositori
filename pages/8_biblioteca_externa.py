from altres.imports import *



st.set_page_config(layout="wide")
barra_lateral2()
# #barra lateral
# pages_dir = Path("pages/")
# archivos_filtrados1 = [
#     archivo.stem.split("_", 1)[-1]
#     for archivo in pages_dir.iterdir()
#     if archivo.name != "__pycache__"
#        and "ext" not in archivo.name
#        and not archivo.name.startswith(("5", "6"))
# ]
# archivos_filtrados2 = [
#     archivo.stem.split("_", 1)[-1]
#     for archivo in pages_dir.iterdir()
#     if archivo.name != "__pycache__"
#        and "ext" in archivo.name
# ]
# archivos_filtrados3 = [
#     archivo.stem.split("_", 1)[-1]
#     for archivo in pages_dir.iterdir()
#     if archivo.name != "__pycache__"
#        and  archivo.name.startswith(("5", "6"))
# ]
#
# # Agregar una opción neutral al inicio del menú
# opciones1 = ["Selecciona una opción"] + archivos_filtrados1
# opciones2 = ["Selecciona una opción"] + archivos_filtrados2
# opciones3 = ["Selecciona una opción"] + archivos_filtrados3
# # Crear el radio con la opción neutral
# selection1 = st.sidebar.radio("General", opciones1, index=0)
# selection2 = st.sidebar.radio("Externs", opciones2, index=0)
# selection3 = st.sidebar.radio("Passos", opciones3, index=0)
# # Manejar el caso en el que no se ha seleccionado ninguna opción significativa
# if selection1 == "crear":
#     st.switch_page("pages/1_crear.py")
# elif selection1 == "filtrar":
#     st.switch_page("pages/2_filtrar.py")
# elif selection1 == "borrar":
#     st.switch_page("pages/4_borrar.py")
# elif selection1 == "arreglar_passos":
#     st.switch_page("pages/11_arreglar_passos.py")
# elif selection1 == "editar":
#     st.switch_page("pages/10_editar.py")
#
# else:
#     st.write("")
# # Manejar el caso en el que no se ha seleccionado ninguna opción significativa
# if selection2 == "recetas_externas":
#     st.switch_page("pages/7_recetas_externas.py")
# elif selection2 == "biblioteca_externa":
#     st.switch_page("pages/8_biblioteca_externa.py")
# else:
#     st.write("")
#
# if selection3 == "passos":
#     st.switch_page("pages/5_passos.py")
# elif selection3 == "protocol":
#     st.switch_page("pages/6_protocol.py")
# else:
#     st.write("")
#
# #_fi barra lateral____________________________





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

#final capçalera


# Inicialitzar l'escurçador
shortener = pyshorteners.Shortener()

conn = sqlitecloud.connect(cami_db)



st.subheader(":material/library_books: Biblioteca receptes externes")

#consulta taula externs
query2 = "SELECT * FROM Externs"
df = pd.read_sql(query2, conn)

col1, col2 = st.columns(2)
# Obtenir els valors únics de la columna Meal
with col1:
    apats_unics = df["Meal"].unique().tolist()
    selection1 = st.pills("Apat", apats_unics, selection_mode="multi")

with col2:
    font_unics = df["Logo"].unique().tolist()
    selection2 = st.pills("Font", font_unics, selection_mode="multi")


df['Miniatura'] = df['Foto'].apply(create_thumbnail2)

df["Vincle"] = df["Link"].apply(lambda link: shortener.tinyurl.short(link))
df["Vincle"] = df['Vincle'].apply(process_observacions)
df = df[["ID_Externs", "Miniatura", "Titol", "Vincle", "Logo", "Meal"]]

# Control inicial: Mostra totes les receptes si no hi ha selecció
if not selection1 and not selection2:
    df_filtrat = df  # Si no hi ha selecció, mostrar tot el DataFrame
else:
    df_filtrat = df[(df["Meal"].isin(selection1)) | (df["Logo"].isin(selection2))]

rows = df.shape[0]
columns = 3
col_index = 0


# Aplicar el filtre al DataFrame


for i, row in df_filtrat.iterrows():
    if col_index % columns == 0:  # Iniciar una nova fila cada 4 columnes
        cols = st.columns(columns)

    with cols[col_index % columns]:
        # Fons blaucel amb HTML + CSS
        with cols[col_index % columns]:
            # Fons blaucel amb HTML + CSS i menys espai entre títol i vincle
            st.markdown(f"""
               <div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                   <p style='margin-bottom: 5px;'><b>Miniatura:</b> {row['Miniatura']}</p>
                   <p style='margin-bottom: 5px;'><b>Títol:</b> {row['Titol']}</p>
                   <p style='margin-bottom: 5px;'><b>Vincle:</b> {row['Vincle']}</p>
                   <p style='margin-bottom: 5px;'><b>Logo:</b> {row['Logo']}</p>
                   <p style='margin-bottom: 10px;'><b>Meal:</b> {row['Meal']}</p>
               </div>
               """, unsafe_allow_html=True)  # Activar HTML
    col_index += 1