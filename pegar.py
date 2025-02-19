def cropping():
    global cropped_image
    # Carregar la imatge
    image_path = 'ruta/a/la/teva/imatge.jpg'  # Ajusta això segons la ruta de la teva imatge
    image = Image.open(image_path)
    # Definir les coordenades del crop (left, top, right, bottom)
    left = 100
    top = 100
    right = 400
    bottom = 400
    # Fer el crop de la imatge
    cropped_image = image.crop((left, top, right, bottom))


cropping()

# Mostrar la imatge retallada (opcional)
cropped_image.show()

# Guardar la imatge retallada
cropped_image.save('ruta/a/la/teva/imatge_retallada.jpg')
