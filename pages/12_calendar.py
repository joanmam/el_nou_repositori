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


# Seleccionar data d'inici
data_inici = st.date_input("Selecciona el primer dia de la setmana", pd.Timestamp.today())
primer_dilluns_actual = data_inici - pd.offsets.Week(weekday=0)

# Trobar el primer dilluns de la setmana següent
primer_dilluns_seguent = primer_dilluns_actual + pd.DateOffset(weeks=1)

# Definir dies de la setmana
dies_setmana = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
apats = ["Esmorzar", "Dinar", "Sopar"]

# Generar les dates corresponents
dates_setmana = pd.date_range(start=primer_dilluns_seguent, periods=7, freq="D").strftime("%d/%m/%Y")

# Crear un diccionari de `DataFrames`, un per cada dia amb la seva data
calendari = {
    dia: pd.DataFrame(index=apats, columns=["Data", "Activitat", "Extern"])
    for dia in dies_setmana
}
# Afegir la data correcta a cada dia
for i, dia in enumerate(dies_setmana):
    calendari[dia]["Data"] = dates_setmana[i]



# Mostrar cada `DataFrame` a Streamlit
for dia, df in calendari.items():
    st.subheader(f"📅 {dia} ({df['Data'][0]})")  # Mostra el dia amb la seva data
    # Comprovar si "Extern" existeix abans d'aplicar process_observacions
    if "Extern" in df.columns:
        df["Extern"] = df["Extern"].fillna("").apply(process_observacions)
    df_visible = df.drop(columns=["Data"])  # Quita las columnas antes de mostra

    edited_df = st.data_editor(df_visible, hide_index=False, key=f"editor_{dia}")  # Evita conflictes de Streamlit
    calendari[dia] = edited_df


if st.button("Guardar"):
    for dia, edited_df in calendari.items():
        st.subheader(f"📅 {dia} ({dates_setmana[dies_setmana.index(dia)]})")  # Mostra el dia amb la seva data

        st.table(edited_df)

