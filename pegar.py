query2 = "SELECT Numero, URL_passos, Pas FROM Passos WHERE ID_Recepte = ?"
df = pd.read_sql(query2, conn, params=[receptes_seleccionades])

# Actualitza els encapçalaments
df.columns = ['Núm.', 'Imatge', 'Descripció del Pas']

# Transformar la columna 'URL_passos' en imatges
df['Imatge'] = df['Imatge'].apply(
    lambda x: f'<img src="{x}" style="width:150px; height:auto;">' if x else '<p>No disponible</p>'
)

# Estil per alternar colors a les files
def row_style(row):
    if row.name % 2 == 0:
        return ['background-color: #f0f0f0'] * len(row)
    else:
        return ['background-color: #ffffff'] * len(row)

# Generar HTML estilitzat
styled_df = df.style.apply(row_style, axis=1)
html = styled_df.hide(axis='index').to_html(escape=False, index=False)
html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

# Mostrar taula estilitzada a Streamlit
taula = dataframe_passos(html)
st.markdown("### Taula dels passos")
st.components.v1.html(taula, height=600, scrolling=True)