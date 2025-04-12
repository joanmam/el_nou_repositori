from altres.imports import *





# #___________________________________________________________
# sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

#___________________________________________________
#Conectar a la base de dades usant la variable db_path pip install sqlitecloud

st.set_page_config(layout="wide")



barra_lateral2()

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
