from altres.imports import *


st.set_page_config(layout="wide")



# Conectarse a la base de datos
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

#__________________________________________________________
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Accio:</p>', unsafe_allow_html=True)
accio = st.text_input("")
today = date.today()
st.markdown('<div class="custom-element"><p class="custom-title">Data:</p>', unsafe_allow_html=True)
data_accio = st.date_input('', today)




# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres:</p>', unsafe_allow_html=True)
ids_to_action = st.text_input("", "1")
n_limit = 5



if st.button('**Resum**'):
    df_insert = pd.DataFrame({
        'ID_Recepte': [ids_to_action],
        'Accio': [accio],
        'Data_accio': [data_accio]
    })

    # Convertir el DataFrame a una llista de tuples
    records = df_insert.to_records(index=False).tolist()

    # Inserir els registres directament a la taula Accions utilitzant SQL
    query_insert = "INSERT INTO Accions (ID_Recepte, Accio, Data_accio) VALUES (?, ?, ?)"
    conn.executemany(query_insert, records)
    conn.commit()

    query2 = """
        SELECT Accions.ID_Accions, Receptes.Titol, Accions.Accio, Accions.Data_accio
        FROM Receptes
        JOIN Accions ON Receptes.ID_Recepte = Accions.ID_Recepte
        WHERE Receptes.ID_Recepte = ?
        ORDER BY Accions.ID_Accions DESC
        LIMIT ?
    """
    df = pd.read_sql(query2, conn, params=[ids_to_action, n_limit])

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1)



    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_accions(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.components.v1.html(taula, height=600, scrolling=True)

    conn.close()