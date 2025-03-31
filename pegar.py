df.loc[df['ID_Recepte'] == id_to_update, ['Titol', 'Observacions', 'Etiquetes', 'Categoria', 'Preparacio', 'Temps', 'URL_Imatge']] = [
    nou_Titol, nova_Observacions, nova_Etiquetes, nova_Categoria, nova_Preparacio, nou_Temps, nova_Imatge
]