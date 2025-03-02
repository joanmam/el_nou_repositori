import pandas as pd

# Suposem que tens un DataFrame amb una columna 'components'
data = {
    "ID_Recepte": [1, 2],
    "components": [
        "Tomàquet (2), Ceba (1), Sal (1)",
        "Patata (3), All (2)"
    ]
}
df = pd.DataFrame(data)

# Diccionari d'emojis per als ingredients
emojis = {
    "tomàquet": "🍅",
    "ceba": "🧅",
    "sal": "🧂",
    "patata": "🥔",
    "all": "🧄"
}
emoji_per_defecte = "❓"

# Funció que transforma components amb emojis
def obtenir_emoji(components):
    if components is None:
        return [emoji_per_defecte]
    emoji_noms = re.findall(r'(\w+)\s*\(([^)]+)\)', components)
    resultat_emoji = []

    for nom, quantitat in emoji_noms:
        emoji_nom = emojis.get(nom.lower(), emoji_per_defecte)
        resultat_emoji.append(f"{emoji_nom} {nom} ({quantitat})")

    return resultat_emoji

# Aplicar la funció a la columna components
df["components_emoji"] = df["components"].apply(lambda x: ', '.join(obtenir_emoji(x)))

# Mostrar el DataFrame resultat
st.write("DataFrame actualitzat amb emojis:", df)




