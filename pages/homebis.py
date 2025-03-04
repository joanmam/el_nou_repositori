from altres.imports import *


st.set_page_config(layout="wide")




# Carregar Font Awesome
font_awesome()

#_____________________________________________________________________________

st.subheader("Receptes")


# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)

# Carregar tota la taula
# Mostrar resultats en diverses columnes
col1, col2 = st.columns([1, 4])

with col1:
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
with col2:
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


