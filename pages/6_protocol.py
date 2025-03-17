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

llista_ingredients_sense_ordenar = list(set(obtenir_ingredients()))
llista_ingredients = sorted(llista_ingredients_sense_ordenar)

separador()
st.text("")
#Acaba la capçalera



receptes_seleccionades = st.text_input("Selecciona els ID de les receptes:")

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[receptes_seleccionades])





# pels passos
    query2 = "SELECT Numero, Imatge_passos, Pas FROM Passos WHERE ID_Recepte = ?"
    df = pd.read_sql(query2, conn, params=[receptes_seleccionades])
    # Converteix cada blob a una imatge i crea una nova columna amb les imatges
    df['Miniatura'] = df['Imatge_passos'].apply(create_thumbnail2)

    # Oculta la columna del blob
    df = df[['Numero', 'Miniatura', 'Pas']]

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1)



    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_passos(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.components.v1.html(taula, height=600, scrolling=True)
