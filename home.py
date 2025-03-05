from altres.imports import *



# #___________________________________________________________
# sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

#___________________________________________________
#Conectar a la base de dades usant la variable db_path pip install sqlitecloud



conn = sqlitecloud.connect(cami_db)


cursor = conn.cursor()

query = "SELECT COUNT(*) FROM Receptes"


cursor.execute(query)
num_registres = cursor.fetchone()[0]

cursor.execute(query)
result = cursor.fetchone()

#_______________________________________________________
# Afegir text dins d'un marc amb l'estil definit
text_personalitzat = "Receptes"

st.markdown(f'''
<div class="marco">
        <div class="text-personalitzat">{text_personalitzat}</div>
        <div class="resultat">{num_registres}</div>
</div>''', unsafe_allow_html=True)

conn.commit()

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
    <a href="/crear" class="absolute-button">
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
