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


separador()


pasted_text = st.text_input("URL")

# Botón para confirmar la entrada
if st.button("Enviar"):


# Si hay contenido pegado
    if pasted_text:
        try:
            # Configurar opciones para Selenium en modo headless (sin abrir el navegador)
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # Configurar el navegador con WebDriver Manager para instalar Chromedriver automáticamente
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),             options=chrome_options
            )
            # Cargar la página desde la URL pegada
            driver.get(pasted_text)

            # Obtener el contenido después de ejecutar JavaScript
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

          # Extraer el título
            title = soup.title.string if soup.title else "No se encontró un título"
            title2 = title.replace("Recipe", "")
            title2 = title2.strip()



            # Mostrar el título en la app de Streamlit
            st.success(f"{title2}")
            # Buscar la imagen

            image_tag = soup.find("img", alt=title2)
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]
                st.image(image_url, caption="Imagen extraída")
                st.write(image_url)
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                size = (100, 100)
                image.thumbnail(size)
                st.image(image)

            else:
                st.warning("No se encontró ninguna imagen con el atributo 'alt' proporcionado o no tiene 'src'.")

            # Cerrar navegador
            driver.quit()

        except Exception as e:
            # Manejo de errores
            st.error(f"Error: {e}")




