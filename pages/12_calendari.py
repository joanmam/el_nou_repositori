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


#Acaba la capçalera

barra_lateral2()
locale.setlocale(locale.LC_TIME, "ca_ES.UTF-8")

st.subheader("Hola")

# 🟢 Formulari d'entrada de dades
st.subheader(":material/app_registration: Ingressar dades ")
opcions_apats = ["Esmorzar", "Dinar", "Sopar"]

data = st.date_input("Data")
receptes_input = st.text_area("Receptes (separades per comes)")
apats_input = st.selectbox("Selecciona un àpat", opcions_apats)  # Selectbox en
urls_input = st.text_area("URLs (separades per comes)")

separador()

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

df["URL_Externs"] = df["URL_Externs"].apply(lambda x: x[:3] + [None] * (2 - len(x)))


df_urls = pd.DataFrame(df["URL_Externs"].to_list(), columns=["URL 1", "URL 2"])




# 📌 Fusionar amb `df_final`
df_final = pd.concat([df.drop(columns=["URL_Externs"]), df_urls[[f"URL {i}" for i in range(1, 3)]]], axis=1)
df_final["Data"] = pd.to_datetime(df_final["Data"]).dt.strftime("%d/%m/%y")







# 🔹 Fusionar amb el dataframe final



df_urls.columns = [f"URL {i+1}" for i in range(df_urls.shape[1])]

df_final = pd.concat([df.drop(columns=["URL_Externs"]), df_urls], axis=1)
df_final["Data"] = pd.to_datetime(df_final["Data"]).dt.strftime("%d/%m/%y")



# 🔵 Selecció de setmana
data_seleccionada = st.date_input("Selecciona una data")
dia_setmana = data_seleccionada.weekday()  # Troba el dia de la setmana (0=Dilluns)
primer_dia = data_seleccionada - timedelta(days=dia_setmana)  # Trobar el dilluns corresponent
ultim_dia = primer_dia + timedelta(days=6)  # Calcula diumenge

primer_dia = pd.to_datetime(primer_dia)
ultim_dia = pd.to_datetime(ultim_dia)

# ✅ Convertir la columna "Data" a datetime abans de filtrar
df_final["Data"] = pd.to_datetime(df_final["Data"], format="%d/%m/%y")

# 🔎 Filtrar per la setmana correcta
df_setmana = df_final[(df_final["Data"] >= primer_dia) & (df_final["Data"] <= ultim_dia)]
df_setmana = df_setmana.drop(columns=["id"], errors="ignore")  # Treu 'id'

# 🔹 Separar el DataFrame per dies
df_per_dia = {dia: df_setmana[df_setmana["Data"] == dia] for dia in df_setmana["Data"].unique()}

# 🔗 Mostrar cada dia per separat
st.subheader(f"📅 Setmana del {primer_dia.strftime('%d/%m/%y')} al {ultim_dia.strftime('%d/%m/%y')}")



if st.button("Visualitzar"):
    df_setmana["Apat"] = df_setmana["Apat"].apply(
        lambda x: ", ".join(map(str, x)) if isinstance(x, list) else str(x))  # ✅ Convertir llistes a cadenes

    df_setmana = df_setmana.sort_values(["Data", "Apat"])  # ✅ Ordenar primer per Data i Apat
    df_setmana["Recepte"] = df_setmana["Recepte"].apply(
        lambda x: ", ".join(map(str, x)) if isinstance(x, list) else str(x))

    df_agrupat_per_data = df_setmana.groupby("Data")  # ✅ Agrupar primer per Data

    for dia, df_dia in df_agrupat_per_data:
        st.subheader(f"{pd.to_datetime(dia).strftime('%A, %d/%m/%y')}")  # 🔹 Dia en català

        # 🔹 Agrupar per Apat dins de cada dia

        df_agrupat_per_apats = df_dia.groupby("Apat")

        for apat, df_apats in df_agrupat_per_apats:
            st.subheader(f"🍽️ {apat}")  # 🔹 Mostrar nom de l'àpat
            df_apats = df_apats.drop(columns=["Data", "Apat"], errors="ignore")  # ✅ Treure columnes innecessàries
            for col in ["URL 1", "URL 2", "URL 3"]:
                if col in df_apats.columns:
                    df_apats[f"Imatge {col}"] = df_apats[col].apply(assignar_imatge)

            ordre_columnes = [
                "Recepte",
                "Imatge URL 1", "URL 1",
                "Imatge URL 2", "URL 2"
            ]
            columnes_present = [col for col in ordre_columnes if col in df_apats.columns]

            df_apats = df_apats[columnes_present]  # ✅ Aplicar l'ordre correcte


            columnes_df = {
                **{col: st.column_config.LinkColumn(width="small", display_text="Open") for col in df_apats.columns if
                   col in ["URL 1", "URL 2"]},
                **{"Recepte": st.column_config.TextColumn(width="large")},
                **{col: st.column_config.ImageColumn(width="medium") for col in ["Imatge URL 1", "Imatge URL 2"]}

            }
            st.dataframe(df_apats, hide_index=True, column_config=columnes_df, use_container_width=False)


