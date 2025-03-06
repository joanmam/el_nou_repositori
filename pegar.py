import streamlit as st
import sqlite3
import pandas as pd

# Connexió a la base de dades
conn = sqlite3.connect('base_de_dades.db')

# Obtenir el paràmetre de consulta (si existeix) des de l'URL
query_params = st.experimental_get_query_params()
dificultat_text = query_params.get('dificultat', ['Sense dades'])[0]  # Valor per defecte si no hi ha paràmetre

# Definir intervals basats en `dificultat_text`
interval_mapping = {
    "Curt": (0, 60),
    "Mitjà": (60, 120),
    "Llarg": (120, 240)
}
slider_range = interval_mapping.get(dificultat_text, (0, 240))  # Assignar el rang segons el paràmetre

# Títol de la pàgina
st.title("Filtratge de Receptes")

# **Crear els elements clicables**
st.subheader("Selecciona la dificultat")
col3 = st.container()

with col3:
    num_columns = 3
    columns = st.columns(num_columns)

    emojis = {
        "Curt": "🟢",
        "Mitjà": "🟠",
        "Llarg": "🔴"
    }

    dificultats = ["Curt", "Mitjà", "Llarg"]
    for idx, dificultat in enumerate(dificultats):
        col = columns[idx % num_columns]
        emoji = emojis.get(dificultat, "✅")
        with col:
            st.markdown(f"""
            <a href="?dificultat={dificultat}" target="_self" style="text-decoration: none;">
                <div style="
                    border: 1px solid red;
                    padding: 5px;
                    border-radius: 10px;
                    text-align: center;
                    background-color: #f9f9f9;
                    font-weight: bold;">
                    {emoji} {dificultat}
                </div>
            </a>
            """, unsafe_allow_html=True)

# **Definir el `slider` per al temps de preparació**
st.subheader("Filtra pel temps de preparació")
temps_prep = st.slider(
    "Selecciona el temps de preparació (en minuts):",
    min_value=0,
    max_value=240,
    value=slider_range,
    step=1
)

# **Consulta SQL dinàmica**
st.subheader("Filtres addicionals")
# Categoria
categoria = st.multiselect("Selecciona la categoria:", ['Tots', 'Entrant', 'Plat Principal', 'Postres'], default=['Tots'])

# Ingredients
ingredients_seleccionats = st.multiselect("Selecciona els ingredients:", ['Tomàquet', 'Patata', 'Pollastre', 'Formatge'])

# **Construir la consulta SQL**
query = '''
    SELECT Receptes.ID_Recepte, Receptes.Data_formatejada, Receptes.Titol, Receptes.Categoria, Receptes.Preparacio, Receptes.blob, Receptes.Temps,
    GROUP_CONCAT(Ingredients.nom || ' (' || Ingredients.quantitat || ')', ', ') AS components
    FROM Receptes
    LEFT JOIN ingredients
    ON Receptes.ID_Recepte = ingredients.ID_Recepte
'''

params = []
conditions = []

# Filtrar per categoria
if 'Tots' not in categoria:
    conditions.append("Receptes.Categoria IN ({})".format(', '.join('?' * len(categoria))))
    params.extend(categoria)

# Filtrar pel temps de preparació
if temps_prep != (0, 240):
    conditions.append("Receptes.Preparacio BETWEEN ? AND ?")
    params.extend(temps_prep)

# Filtrar per ingredients seleccionats
if ingredients_seleccionats:
    ingredient_conditions = []
    for ing in ingredients_seleccionats:
        ingredient_conditions.append("ingredients.nom LIKE ?")
        params.append(f'%{ing}%')
    conditions.append("(" + " OR ".join(ingredient_conditions) + ")")

# Afegir condicions a la consulta
if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += " GROUP BY Receptes.ID_Recepte"

# **Executar la consulta**
try:
    df = pd.read_sql(query, conn, params=params)
except Exception as e:
    st.error(f"Error en executar la consulta: {e}")
    conn.close()
    st.stop()

# **Mostrar els resultats**
if df.empty:
    st.warning("No s'han trobat receptes amb els filtres seleccionats.")
else:
    st.write(f"S'han trobat {len(df)} receptes.")
    for index, row in df.iterrows():
        st.write(f"- **{row['Titol']}** ({row['Categoria']}): {row['Preparacio']} minuts")
        st.write(f"  - Ingredients: {row['components']}")

# Tancar la connexió
conn.close()

