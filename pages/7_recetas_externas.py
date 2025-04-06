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


separador()


conn = sqlitecloud.connect(cami_db)


# Botón para confirmar la entrada




# Configuració de la base de dades



# Configuració de la base de dades
conn = sqlitecloud.connect(cami_db)

# Inputs de Streamlit
pasted_text = st.text_input("URL")
font = st.text_input("Font")
meal = st.text_input("Meal")

if st.button("Enviar"):
    if pasted_text:
        # Fer una sol·licitud GET a la URL
        response = requests.get(pasted_text)

        # Comprovar si la sol·licitud ha tingut èxit
        if response.status_code == 200:
            html = response.text

            # Analitzar el contingut HTML amb BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # Extreure el títol
            title = soup.title.string if soup.title else "No se encontró un título"
            title2 = title.replace("Recipe", "").strip()
            st.success(f"Títol: {title2}")

            # Buscar la imatge
            blob = None
            image_tag = soup.find("img")  # Buscar la primera etiqueta img
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]
                if not image_url.startswith("http"):
                    # Assegura que l'URL sigui complet
                    image_url = requests.compat.urljoin(pasted_text, image_url)

                st.write(f"URL de la imatge: {image_url}")

                # Obtenir i mostrar la imatge
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    image = Image.open(BytesIO(img_response.content))
                    image.thumbnail((100, 100))  # Reduir la mida de la imatge
                    st.image(image)

                    # Convertir la imatge a blob binari
                    buffer = BytesIO()
                    image.save(buffer, format="JPEG")
                    blob = buffer.getvalue()

            # Crear el DataFrame
            df_insert = pd.DataFrame({
                "Titol": [title2],
                "Link": [pasted_text],
                "Foto": [blob],
                "Logo": [font],
                "Meal": [meal]
            })

            # Inserir registres a la base de dades
            records = df_insert.to_records(index=False).tolist()
            query_insert = "INSERT INTO Externs (Titol, Link, Foto, Logo, Meal) VALUES (?, ?, ?, ?, ?)"
            conn.executemany(query_insert, records)
            conn.commit()
            st.success("Guardat!")
        else:
            st.error(f"No s'ha pogut carregar la URL. Codi d'error: {response.status_code}")




