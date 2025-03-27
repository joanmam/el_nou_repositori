from altres.imports import *

st.set_page_config(layout="wide")

# Connexió a la base de dades
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()


# Cargar credenciales desde el archivo JSON
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

# Crear el cliente de Google Drive
service = build('drive', 'v3', credentials=creds)

# ID de la carpeta en Google Drive
folder_id = 'receptes-447415'  # Reemplaza con el ID de tu carpeta

# Subir imatges amb Streamlit
uploaded_file = st.file_uploader("Puja una imatge", type=["jpg", "png", "jpeg"])
if uploaded_file:
    # Subir la imatge a Google Drive
    file_metadata = {
        "name": uploaded_file.name,
        "parents": [folder_id]
    }
    media = io.BytesIO(uploaded_file.read())
    media.seek(0)
    media_body = googleapiclient.http.MediaIoBaseUpload(media, mimetype="image/jpeg")
    uploaded_image = service.files().create(
        body=file_metadata, media_body=media_body, fields="id"
    ).execute()
    file_id = uploaded_image.get("id")
    file_url = f"https://drive.google.com/uc?id={file_id}"

    # Mostra el URL generat
    st.success(f"Imatge pujada exitosament a Google Drive! URL: {file_url}")


# Guardar URL en la base de dades
cursor.execute("INSERT INTO Receptes (ID_Extern, url) VALUES (?, ?)", (uploaded_file.name, file_url))
conn.commit()
st.success("URL guardat a SQLiteCloud!")



