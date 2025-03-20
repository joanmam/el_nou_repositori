from streamlit import dataframe

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

# Inicialitzar l'escurçador
shortener = pyshorteners.Shortener()

conn = sqlitecloud.connect(cami_db)



#consulta taula externs
query2 = "SELECT * FROM Externs"
df = pd.read_sql(query2, conn)

df['Miniatura'] = df['Foto'].apply(create_thumbnail2)

df["Vincle"] = df["Link"].apply(lambda link: shortener.tinyurl.short(link))
df["Vincle"] = df['Vincle'].apply(process_observacions)
df = df[["ID_Externs", "Miniatura", "Titol", "Vincle", "Logo", "Meal"]]

rows = df.shape[0]
columns = 3
col_index = 0




for i, row in df.iterrows():
    if col_index % columns == 0:  # Iniciar una nova fila cada 4 columnes
        cols = st.columns(columns)

    with cols[col_index % columns]:
        # Fons blaucel amb HTML + CSS
        with cols[col_index % columns]:
            # Fons blaucel amb HTML + CSS i menys espai entre títol i vincle
            st.markdown(f"""
               <div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                   <p style='margin-bottom: 5px;'><b>Miniatura:</b> {row['Miniatura']}</p>
                   <p style='margin-bottom: 5px;'><b>Títol:</b> {row['Titol']}</p>
                   <p style='margin-bottom: 5px;'><b>Vincle:</b> {row['Vincle']}</p>
                   <p style='margin-bottom: 5px;'><b>Logo:</b> {row['Logo']}</p>
                   <p style='margin-bottom: 10px;'><b>Meal:</b> {row['Meal']}</p>
               </div>
               """, unsafe_allow_html=True)  # Activar HTML
    col_index += 1
