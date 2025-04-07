import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import date, timedelta

# 🔗 Connexió a SQLite
conn = sqlite3.connect("Calendari.sqlite")
cursor = conn.cursor()

# 🟢 Formulari d'entrada de dades
st.title("Ingressar dades en SQLiteCloud")
opcions_apats = ["Esmorzar", "Dinar", "Sopar"]

data = st.date_input("Data")
receptes_input = st.text_area("Receptes (separades per comes)")
apats_input = st.selectbox("Selecciona un àpat", opcions_apats)
urls_input = st.text_area("URLs (separades per comes)")

st.divider()  # Millora la presentació visual

# 🔄 Guardar dades
if st.button("Guardar Dades"):
    if receptes_input:
        # Convertir a JSON
        receptes = json.dumps([x.strip() for x in receptes_input.split(",")])
        urls = json.dumps([x.strip() for x in urls_input.split(",")])

        # Inserir a la base de dades
        cursor.execute("INSERT INTO Calendari (Data, Apat, Recepte, URL_Externs) VALUES (?, ?, ?, ?)",
                       (str(data), apats_input, receptes, urls))
        conn.commit()
        st.success("✅ Dades guardades correctament!")

# 🔎 Mostrar les dades guardades
df = pd.read_sql_query("SELECT * FROM Calendari", conn)

# 🔹 Expandir JSON en columnes
df["Apat"] = df["Apat"].apply(json.loads)
df["Recepte"] = df["Recepte"].apply(json.loads)
df["URL_Externs"] = df["URL_Externs"].apply(json.loads)

# 🔗 Limitar URLs a 3 màxim
df["URL_Externs"] = df["URL_Externs"].apply(lambda x: x[:3] + [None] * (3 - len(x)))

df_urls = pd.DataFrame(df["URL_Externs"].to_list(), columns=["URL 1", "URL 2", "URL 3"])
df_final = pd.concat([df.drop(columns=["URL_Externs"]), df_urls], axis=1)

# 🔎 Transformar les dates a format DD/MM/YY
df_final["Data"] = pd.to_datetime(df_final["Data"]).dt.strftime("%d/%m/%y")

# 🔵 Selecció de setmana
data_seleccionada = st.date_input("Selecciona una data")
dia_setmana = data_seleccionada.weekday()  # Troba el dia de la setmana (0=Dilluns)
primer_dia = data_seleccionada - timedelta(days=dia_setmana)  # Trobar el dilluns corresponent
ultim_dia = primer_dia + timedelta(days=6)  # Calcula diumenge

# 🔹 Convertir dates a strings per comparar
primer_dia_str = primer_dia.strftime("%d/%m/%y")
ultim_dia_str = ultim_dia.strftime("%d/%m/%y")

# 🔎 Filtrar per la setmana correcta
df_setmana = df_final[(df_final["Data"] >= primer_dia_str) & (df_final["Data"] <= ultim_dia_str)]
df_setmana = df_setmana.drop(columns=["id"], errors="ignore")  # Treu 'id'

# 🔹 Separar el DataFrame per dies
df_per_dia = {dia: df_setmana[df_setmana["Data"] == dia] for dia in df_setmana["Data"].unique()}

# 🔗 Mostrar cada dia per separat
st.subheader(f"📅 Setmana del {primer_dia.strftime('%d/%m/%y')} al {ultim_dia.strftime('%d/%m/%y')}")

for dia, df_dia in df_per_dia.items():
    st.subheader(f"Dades del {dia}")
    st.dataframe(df_dia, hide_index=True, column_config={
        col: st.column_config.LinkColumn() for col in df_urls.columns
    }, use_container_width=True)