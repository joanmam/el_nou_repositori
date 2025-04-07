from altres.imports import *
st.set_page_config(layout="wide")
#Comença la capçalera
# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

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

barra_lateral2()


# 🟢 Formulari d'entrada de dades
st.title("Ingressar dades en SQLiteCloud")
data = st.date_input("Data")
receptes_input = st.text_area("Receptes (separades per comes)")
apats_input = st.text_area("Apats (separades per comes)")
urls_input = st.text_area("URLs (separades per comes)")

# Guardar dades
if st.button("Guardar Dades"):
    if receptes_input:
        # Convertir a JSON
        receptes = json.dumps([x.strip() for x in receptes_input.split(",")])
        urls = json.dumps([x.strip() for x in urls_input.split(",")])
        apats = json.dumps([x.strip() for x in apats_input.split(",")])
        # Inserir a SQLiteCloud
        cursor.execute("INSERT INTO Calendari (Data, Apat, Recepte, URL_Externs) VALUES (?, ?, ?, ?)",
                       (str(data), apats, receptes, urls))
        conn.commit()
        st.success("✅ Dades guardades correctament!")

# 🟠 Mostrar les dades guardades
df = pd.read_sql_query("SELECT * FROM Calendari", conn)

# Expandir JSON en columnes per veure millor
df["Apat"] = df["Apat"].apply(json.loads)
df["Recepte"] = df["Recepte"].apply(json.loads)
df["URL_Externs"] = df["URL_Externs"].apply(json.loads)

df["URL_Externs"] = df["URL_Externs"].apply(lambda x: x[:3] + [None] * (3 - len(x)))


df_urls = pd.DataFrame(df["URL_Externs"].to_list(), columns=["URL 1", "URL 2", "URL 3"])

df_urls.columns = [f"URL {i+1}" for i in range(df_urls.shape[1])]

df_final = pd.concat([df.drop(columns=["URL_Externs"]), df_urls], axis=1)


st.subheader("Dades en la Base de Dades")
st.dataframe(df_final, column_config={
    col: st.column_config.LinkColumn() for col in df_urls.columns
})



