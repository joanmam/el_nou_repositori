from PIL import Image
import io
import base64


def convert_blob_to_base64_2(blob, width=300, height=None):
    """
    Convierte un blob de imagen de la base de datos a una imagen redimensionada en base64.

    Args:
    - blob: Datos binarios de la imagen.
    - width: Ancho deseado para la imagen redimensionada.
    - height: Altura deseada. Si no se proporciona, se calcula manteniendo la proporción.

    Returns:
    - str: Imagen en base64 lista para usar en HTML.
    """
    try:
        # Convertir el blob en un objeto de imagen usando Pillow
        image = Image.open(io.BytesIO(blob))

        # Redimensionar la imagen
        if height is None:
            aspect_ratio = image.height / image.width
            height = int(width * aspect_ratio)
        resized_image = image.resize((width, height), Image.ANTIALIAS)

        # Convertir la imagen redimensionada a base64
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error al procesar el blob de imagen: {e}")
        return None






