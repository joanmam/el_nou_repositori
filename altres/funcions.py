#emoji

import re
import emoji
from altres.manteniment import emojis


# Funció per obtenir l'emoji basat en el valor de la cel·la
emoji_per_defecte = "\u2753"

def obtenir_emoji(components):
    if components is None:
        return [emoji_per_defecte]
    emoji_noms = re.findall(r'(\w+)\s*\(([^)]+)\)', components)
    resultat_emoji = []

    for nom, quantitat in emoji_noms:
        emoji_nom = emojis.get(nom.lower(), emoji_per_defecte)
        resultat_emoji.append(f"{emoji_nom} {nom} ({quantitat})")

    return resultat_emoji
