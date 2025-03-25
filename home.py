from altres.imports import *





# #___________________________________________________________
# sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

#___________________________________________________
#Conectar a la base de dades usant la variable db_path pip install sqlitecloud

st.set_page_config(layout="wide")



conn = sqlitecloud.connect(cami_db)


cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"


cursor.execute(query)
num_registres = cursor.fetchone()[0]

cursor.execute(query)
result = cursor.fetchone()

#_______________________________________________________


conn.commit()
#navigation

# # Directorio a listar
# # st.markdown(
#     """
#     <style>
#     /* Ocultar los círculos de los botones de opción */
#     div[role="radiogroup"] > label > div:first-child {
#         display: none; /* Oculta el círculo */
#     }
#
#     /* Personalizar las opciones como botones redondeados */
#     div[role="radiogroup"] > label {
#         font-size: 10px !important; /* Cambiar tamaño del texto */
#         font-family: Arial, sans-serif; /* Fuente consistente */
#         padding: 15px; /* Espaciado interno corregido */
#         margin: 5px 0; /* Espaciado entre botones */
#         width: 200px; /* Ancho fijo */
#         height: 50px; /* Altura fija */
#         background-color: #fff8dc; /* Fondo amarillo claro */
#         color: black; /* Texto negro */
#         border: 2px solid #ffd700; /* Borde amarillo dorado */
#         border-radius: 25px; /* Bordes redondeados */
#         cursor: pointer; /* Cursor estilo puntero */
#         display: flex; /* Flexbox para alinear contenido */
#         align-items: center; /* Alinear el texto verticalmente */
#         justify-content: center; /* Justificar texto dentro del botón */
#         text-align: center; /* Alinear texto horizontalmente */
#     }
#
#     /* Cambiar el fondo y borde al pasar el cursor */
#     div[role="radiogroup"] > label:hover {
#         background-color: #fffacd; /* Fondo más claro al pasar el cursor */
#         border-color: #ffa500; /* Borde más oscuro */
#     }
#
#     /* Cambiar el tamaño del texto del label de st.radio */
#     .sidebar .stMarkdown h4 {
#         font-size: 24px; /* Tamaño del texto */
#         color: darkblue; /* Color del texto */
#         font-weight: bold; /* Texto en negrita */
#     }
#
#     /* Estilo para la opción seleccionada */
#     div[role="radiogroup"] > label:has(input:checked) {
#         background-color: #ffd700 !important; /* Fondo amarillo intenso */
#         color: black !important; /* Texto negro */
#         border-color: #ffa500 !important; /* Borde naranja intenso */
#         font-size: 22px !important; /* Texto más grande para la opción seleccionada */
#         font-weight: bold; /* Texto en negrita */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )






pages_dir = Path("pages/")
archivos_filtrados1 = [
    archivo.stem.split("_", 1)[-1]
    for archivo in pages_dir.iterdir()
    if archivo.name != "__pycache__"
       and "ext" not in archivo.name
]
archivos_filtrados2 = [
    archivo.stem.split("_", 1)[-1]
    for archivo in pages_dir.iterdir()
    if archivo.name != "__pycache__"
       and "ext" in archivo.name
]
# Agregar una opción neutral al inicio del menú
opciones1 = ["Selecciona una opción"] + archivos_filtrados1
opciones2 = ["Selecciona una opción"] + archivos_filtrados2
# Crear el radio con la opción neutral
selection1 = st.sidebar.radio("Menu1", opciones1, index=0)
selection2 = st.sidebar.radio("Menu2", opciones2, index=0)
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

#_____________________________

background_home()
estils_marc()
# _________________________________________________________________________
st.markdown(
    """
    <style>
    .absolute-button {
        position: absolute;
        top: -100px; /* Posició vertical fixa */
        left: 125%; /* Centrat horitzontalment */
        transform: translate(-50%, 0%); /* Centrat completament horitzontalment */
        background-color: red;
        color: white !important; /* Text blanc, prioritat amb !important */
        font-size: 18px; /* Mida del text */
        font-weight: bold;
        border: none;
        border-radius: 8px; /* Cantonades arrodonides */
        padding: 10px 20px; /* Espai dins del botó */
        width: 200px; /* Definició d'una amplada fixa si cal */
        cursor: pointer;
        text-align: center; /* Centrar el text dins del botó */
        text-decoration: none !important; /* Eliminar subratllat */
    }
    .absolute-button:hover {
        background-color: #ff7700; /* Color més intens en passar el cursor */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HTML per al botó
st.markdown(
    """
    <a href="/pages/1_crear.py" class="absolute-button">
        Afegir recepta
    </a>
    """,
    unsafe_allow_html=True
)


# Refresc automàtic després del botó
st.markdown(
    """
    <script>
        window.location.reload();
    </script>
    """,
    unsafe_allow_html=True
)
