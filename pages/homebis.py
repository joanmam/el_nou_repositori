from altres.imports import *


st.set_page_config(layout="wide")

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Vibur&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True)


# Carregar Font Awesome
font_awesome()

#_____________________________________________________________________________

st.subheader("Receptes")


# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)

# Carregar tota la taula
# Mostrar resultats en diverses columnes
col1, col2, col3 = st.columns([2, 1, 3])

with col1:


    # Mostrar la imatge com a enllaç clicable
    # Mostrar el div estilitzat amb text
    st.markdown(
        f"""
        <div style="border: 1px solid red; background-color: red; border-radius: 18px; padding: 5px; font-family: 'Roboto', sans-serif; font-weight: 600; font-style: italic; font-size: 18px; color: white;">
            Les Receptes de Mamen
        </div>
        """,
        unsafe_allow_html=True)

with col2:
    query = "SELECT * FROM Receptes"
    df = pd.read_sql(query, conn)
    count_total = df.shape[0]
    st.markdown(
        f'<div style="border: 1px solid red; border-radius: 20px; padding: 5px;"><i class="fas fa-bell"></i> {count_total}</div>',
        unsafe_allow_html=True)


# Mostrar recompte total amb icona

df = pd.read_sql("SELECT Temps FROM Receptes", conn)


# Crear intervals amb pandas
intervals = [0, 10, 60, float("inf")]
etiquetes = ["Menor de 10", "Entre 10 y 60", "Superior a 60"]


df["intervals"] = pd.cut(df["Temps"], bins=intervals, labels=etiquetes, right=True)

# Comptar registres per interval
resultat = df["intervals"].value_counts(sort=False)
resultat_df = resultat.reset_index()
resultat_df.columns = ["Etiqueta", "Nombre de registres"]

# Definir una llista d'icones per a cada etiqueta
emojis = {
    "Menor de 10": "🟢",
    "Entre 10 y 60": "🟠",
    "Superior a 60": "🔴"}

dificultat = {
    "Menor de 10": "Curt",
    "Entre 10 y 60": "Mitjà",
    "Superior a 60": "Llarg"

}
with col3:
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in resultat_df.iterrows():
        col = columns[idx % num_columns]
        emoji = emojis.get(row['Etiqueta'], "✅")  # Definir un emoji de fall back
        dificultat_text = dificultat.get(row['Etiqueta'], "Desconeguda")  # Definir un emoji de fall back
        with col:
            st.markdown(f"""
            <div style="border: 1px solid red; padding: 5px; border-radius: 20px;">
            {emoji} {row['Nombre de registres']} {dificultat_text}
            </div>
            """, unsafe_allow_html=True)


conn.close()




# CSS personalitzat per estilitzar el botó i assegurar que el text sigui blanc
st.markdown(
    """
    <style>
    .absolute-button {
        position: absolute;
        top: 50px; /* Posició vertical fixa */
        left: 50%; /* Centrat horitzontalment */
        transform: translate(-50%, 0); /* Centrat completament horitzontalment */
        background-color: orange; /* Color carbassa */
        color: white !important; /* Text blanc, prioritat amb !important */
        font-size: 18px; /* Mida del text */
        font-weight: bold;
        border: none;
        border-radius: 8px; /* Cantonades arrodonides */
        padding: 10px 20px; /* Espai dins del botó */
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
