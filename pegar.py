# Disseny dins de Streamlit
for i, row in df.iterrows():
    col = columns[i % num_columns]  # Seleccionar columna
    with col:
        if row["blob"]:  # Verificar que no sigui None
            img_base64 = convert_blob_to_base64(row["blob"])

            st.markdown(
                f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background-color: #f9f9f9;">
                    <!-- Imatge que ocupa una columna -->
                    <div style="grid-column: 1 / span 1;">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="Foto" style="width:100%; height:auto; border-radius:10px; object-fit:cover;" />
                    </div>
                    <!-- Títol i Categoria que ocupen dues columnes -->
                    <div style="grid-column: 1 / span 2; text-align: center;">
                        <h3>{row['Titol']}</h3>
                        <p><strong>Categoría:</strong> {row['Categoria']}</p>
                    </div>
                    <!-- Observacions que ocupen una columna -->
                    <div style="grid-column: 1 / span 1;">
                        <p><strong>Observacions:</strong> {row['Observacions']}</p>
                    </div>
                    <!-- Ingredients que ocupen una columna -->
                    <div style="grid-column: 2 / span 1;">
                        <p><strong>Ingredients:</strong> {row['components']}</p>
                    </div>
                    <!-- Temps de preparació que ocupa dues columnes -->
                    <div style="grid-column: 1 / span 2; text-align: center;">
                        <p><strong>Temps de preparació:</strong> {row['Preparacio']} min</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )




