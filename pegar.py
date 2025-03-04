import pandas as pd
import sqlitecloud
import streamlit as st

# Connexió a la base de dades
conn = sqlitecloud.connect("cami_a_la_base_de_dades")

# Carregar tota la taula
col1, col2 = st.columns(2)

# Carregar el CSS de Font Awesome
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True
)

with col1:
    query = "SELECT * FROM Receptes"
    df = pd.read_sql(query, conn)
    count_total = df.shape[0]

    # Mostrar recompte total amb icona
    st.markdown(
        f'<i class="fas fa-bell"></i> {count_total}', unsafe_allow_html=True
    )

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
icones = {
    "Menor de 10": '<i class="fa-solid fa-star" style="color: #24c270;"></i>',
    "Entre 10 y 60": '<i class="fa-solid fa-star" style="color: #f07c0f;"></i>',
    "Superior a 60": '<i class="fa-solid fa-star" style="color: #ff0000;"></i>'
}

with col2:
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in resultat_df.iterrows():
        col

