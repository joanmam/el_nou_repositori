from PIL.FontFile import WIDTH

from altres.imports import *

st.set_page_config(layout="wide")

# Carregar Font Awesome
font_awesome()

def render_image(Imatge):
    return f'<img src="{Imatge}" width="150">'
barra_lateral2()

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




#Acaba la capçalera
#_____________________________________________________________________________
#connexio a la base de dades


conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

st.subheader(":material/edit: Editar")

# Realizar consulta SQL para obtener registros
query = "SELECT * FROM Receptes"
df = pd.read_sql(query, conn)

df["Imatge_text"] = df["Imatge"]
df_visible = df.drop(columns=["blob", "Preparacio", "Temps", "Data_formatejada"])  # Quita las columnas antes de mostra


column_order = ["ID_Recepte", "Titol", "Imatge_text", "Imatge", "Observacions", "Etiquetes", "Categoria"]
df_visible = df_visible[column_order]


# Configurar columnas del DataFrame
with st.container():
    edited_df = st.data_editor(
        df_visible,
        column_config={
            "ID_Recepte": st.column_config.NumberColumn(
                label="ID",
            ),
            "Titol": st.column_config.TextColumn(
                label="Titol",
            ),
            "Imatge_text": st.column_config.TextColumn(
                label="URL",
            ),
            "Imatge": st.column_config.ImageColumn(
                label="Vista previa",
                help="Imagenes"
            ),
            "Observacions": st.column_config.TextColumn(
                label="Observacions",
            ),
            "Etiquetes": st.column_config.TextColumn(
                label="Etiquetes",
            ),
            "Categoria": st.column_config.SelectboxColumn(
                label="Categoria",
                options=["Plato único", "Acompañamiento", "Primero", "Segundo"]
            ),
        },
        hide_index=True,
        use_container_width=True)

# Botón para actualizar cambios en SQLiteCloud
if st.button("Actualitzar"):
    for index, row in edited_df.iterrows():
        query_update = f"""
        UPDATE Receptes 
        SET Titol = '{row["Titol"]}',
            Imatge = '{row["Imatge_text"]}',
            Observacions = '{row["Observacions"]}',
            Etiquetes = '{row["Etiquetes"]}',
            Categoria = '{row["Categoria"]}'
        WHERE ID_Recepte = {row["ID_Recepte"]}
        """
        conn.execute(query_update)  # Ejecutar el UPDATE en SQLiteCloud

    conn.commit()  # Guardar cambios
    st.success("¡Datos actualizados correctamente en SQLiteCloud! 🎉")

    query = "SELECT ID_Recepte, Imatge, Titol, Observacions, Etiquetes, Categoria FROM Receptes"
    update_df = pd.read_sql(query, conn)

    # Configurar columnas del DataFrame
    with st.container():
        update_df = st.dataframe(
            update_df,
            column_config={
                "ID_Recepte": st.column_config.NumberColumn(
                    label="ID",
                ),
                "Titol": st.column_config.TextColumn(
                    label="Titol",
                ),
                "Imatge": st.column_config.ImageColumn(
                    label="Vista previa",
                    help="Imagenes"
                ),
                "Observacions": st.column_config.TextColumn(
                    label="Observacions",
                ),
                "Etiquetes": st.column_config.TextColumn(
                    label="Etiquetes",
                ),
                "Categoria": st.column_config.TextColumn(
                    label="Categoria",
                ),
            },
        hide_index=True,
        use_container_width=True)
