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
id_to_update = st.number_input("", min_value=4, step=1)


# Mostrar informació dels registres seleccionats
registre = (id_to_update,)
st.write(f"El registre seleccionat per actualitzar és: {id_to_update}")



query = "SELECT ID_Recepte, Titol, Observacions, Etiquetes, Categoria, Preparacio, Temps FROM Receptes WHERE ID_Recepte = ?"

df = pd.read_sql(query, conn, params=[id_to_update])

df['Observacions'] = df['Observacions'].apply(lambda x: process_observacions(x))

# Mostra les dades existents
st.subheader('Dades actuals dels registres')
# Aplica l'estil de les files i les columnes
styled_df = df.style.apply(row_style, axis=1)

# Genera l'HTML estilitzat
html = styled_df.hide(axis='index').to_html()
html = html.replace('<style type="text/css">',
                    '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

# Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
taula = dataframe_actualitzar(html)

# Mostra el DataFrame estilitzat utilitzant Streamlit
st.components.v1.html(taula, height=100, scrolling=True)
separador()

st.subheader("Nous valors")

valors_fila = df.loc[df["ID_Recepte"] == id_to_update]
nou_Titol = st.text_input("Nou Titol:", value=valors_fila.iloc[0]["Titol"])
nova_Observacions = st.text_input("Nova Observacions:")
nova_Observacions = process_observacions(nova_Observacions)
nova_Etiquetes = st.text_input("Nova Etiquetes:", value=valors_fila.iloc[0]["Etiquetes"])
nova_Categoria = st.text_input("Noves Categoria", value=valors_fila.iloc[0]["Categoria"])
nova_Preparacio = st.text_input("Nova Preparacio", value=valors_fila.iloc[0]["Preparacio"])
nou_Temps = st.text_input("Nou Temps", value=valors_fila.iloc[0]["Temps"])

# Botó per actualitzar
if st.button("Actualitzar"):
    # Comprovar que l'ID no és buit
    if id_to_update:
        # Convertir l'ID a tipus enter
        id_to_update = int(id_to_update)

        # Llegeix les dades existents a la taula "Receptes"
        df = pd.read_sql_query("SELECT * FROM Receptes", conn)

        # Comprova que l'ID existeix a la taula
        if id_to_update in df['ID_Recepte'].values:
            # Actualitza les columnes proporcionades
            if nou_Titol:
                df.loc[df['ID_Recepte'] == id_to_update, 'Titol'] = nou_Titol
            if nova_Observacions:
                df.loc[df['ID_Recepte'] == id_to_update, 'Observacions'] = nova_Observacions
            if nova_Etiquetes:
                df.loc[df['ID_Recepte'] == id_to_update, 'Etiquetes'] = nova_Etiquetes
            if nova_Categoria:
                df.loc[df['ID_Recepte'] == id_to_update, 'Categoria'] = nova_Categoria
            if nova_Preparacio:
                df.loc[df['ID_Recepte'] == id_to_update, 'Preparacio'] = nova_Preparacio
            if nou_Temps:
                df.loc[df['ID_Recepte'] == id_to_update, 'Temps'] = nou_Temps

            # Genera un nom únic per a la taula temporal
            temp_table_name = f"Receptes_temp_{uuid.uuid4().hex}"

            # Guarda només les dades actualitzades a la taula temporal
            df_actualitzat = df[df['ID_Recepte'] == id_to_update]
            df_actualitzat.to_sql(temp_table_name, conn, if_exists='replace', index=False)

            # Actualitza la taula original
            conn.execute(f"DELETE FROM Receptes WHERE ID_Recepte = ?", (id_to_update,))
            conn.commit()

            conn.execute(f"INSERT INTO Receptes SELECT * FROM {temp_table_name}")
            conn.commit()

            # Esborra la taula temporal
            conn.execute(f"DROP TABLE {temp_table_name}")
            conn.commit()

            # Comprova i mostra els canvis
            df_mostrat = pd.read_sql_query("SELECT ID_Recepte, Titol, Observacions, Etiquetes, Categoria, Preparacio, Temps FROM Receptes WHERE ID_Recepte = ?", conn, params=[id_to_update])
            st.write("Dades actualitzades:")
            styled_df = df_mostrat.style.apply(row_style, axis=1)

            # Genera l'HTML estilitzat
            html = styled_df.hide(axis='index').to_html()
            html = html.replace('<style type="text/css">',
                                '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

            # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
            taula = dataframe_actualitzar(html)

            # Mostra el DataFrame estilitzat utilitzant Streamlit
            st.components.v1.html(taula, height=600, scrolling=True)

        else:
            st.write("No s'ha trobat cap registre amb aquest ID.")
    else:
        st.write("Si us plau, introdueix l'ID de la recepta.")

conn.close()

