# ARCHIVO DE PRUEBA PARA EL MANEJO DE IMÁGENES RGB (BGR EN OPENCV) EN PYTHON
import numpy as np
import cv2

# Crear una matriz (por ejemplo, una imagen en blanco)
width = 400
height = 300
channels = 3  # RGB

# Crear una matriz con valores aleatorios para este ejemplo
matrix = np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)

# Guardar la matriz como una imagen JPEG
cv2.imwrite('matriz_imagen.jpg', matrix)

print("Imagen guardada correctamente.")

coord_x = 12
coord_y = 23

pixel_value = matrix[coord_y, coord_x]

print("Valor del píxel en la posición (12, 23):", pixel_value)
