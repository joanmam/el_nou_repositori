

# 1. Descarregar la imatge des de Google Fotos
google_photos_url = "URL_DE_GOOGLE_FOTOS"  # Substitueix aquest URL pel de Google Fotos
response = requests.get(google_photos_url)

if response.status_code == 200:  # Comprova que la imatge s'ha descarregat correctament
    image_data = response.content
else:
    st.write("No s'ha pogut descarregar la imatge de Google Fotos")
    exit()

# 2. Carregar la imatge a Postimages
postimages_api_url = "https://api.postimages.org/1/upload"
payload = {
    "key": "71ee969c2c37eaf3b2a57211fa8f789a",  # Has de registrar-te a Postimages per obtenir una API key
    "expiration": "0",  # 0 significa que l'enllaç no caducarà
}
files = {
    "file": ("imatge.jpg", image_data, "image/jpeg")
}

post_response = requests.post(postimages_api_url, data=payload, files=files)

if post_response.status_code == 200:
    post_result = post_response.json()
    post_url = post_result.get("data", {}).get("url")
else:
    st.write("No s'ha pogut carregar la imatge a Postimages")





