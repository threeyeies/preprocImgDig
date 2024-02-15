import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
from PIL import Image
from PIL.ExifTags import TAGS
import os

ren = 400
col = 400
channels = 3 # RGB
prom = 123 # Promedio de la matriz m
mb = np.zeros((ren, col),dtype=np.uint8) # Matriz binarizada
imagepath = "matrizMc.jpg" #ruta de la imagen para obtener los datos EXIF

# Colores en formato BGR utilizado por OpenCV
colors_bgr = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'cyan': (255, 255, 0),
    'magenta': (255, 0, 255),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'light_gray': (192, 192, 192),
    'maroon': (0, 0, 128),
    'olive': (0, 128, 128),
    'navy': (128, 0, 0),
    'purple': (128, 0, 128),
    'teal': (128, 128, 0),
    'silver': (192, 192, 192),
    'gold': (0, 215, 255),
    'pink': (203, 192, 255),
    'orange': (0, 165, 255),
    'brown': (42, 42, 165)
}



def etiquetado_4adyacente(mb, mc):

    for i in range(len(mb)):  
        for j in range(len(mb)):
            p = mb[i,j] #pixel actual

            # Si es el primer pixel (0,0)
            if i==0 and j==0:
                if p==0:
                    mc[i,j] = (0,0,0) #se queda en fondo, pasa al siguiente pixel
                elif p==255:
                    mc[i,j] = random.choice(list(colors_bgr.values())) #se asigna un color aleatorio

            # Si es el primer renglón (i=0) no se verifica el pixel de arriba
            if i==0 and j!=0:
                t = mc[i,j-1] 
                if p == 0:
                    mc[i,j] = (0,0,0)
                elif p == 255:
                    if np.any(t == (0, 0, 0)):
                        mc[i,j] = random.choice(list(colors_bgr.values()))
                    if np.any(t != (0, 0, 0)):
                        mc[i,j] = t

            # Si es la primera columna (j=0) no se verifica el pixel de la izquierda
            if j==0 and i!=0:
                r = mc[i-1,j] 
                if p == 0:
                    mc[i,j] = (0,0,0)
                elif p == 255:
                    if np.any(r == (0,0,0)):
                        mc[i,j] = random.choice(list(colors_bgr.values()))
                    if np.any(r != (0,0,0)):
                        mc[i,j] = r

            # Si no es ni el primer renglón ni la primera columna
            if i!=0 and j!=0:
                r = mc[i-1,j] 
                t = mc[i,j-1] 
                if p == 0:
                    mc[i,j] = (0,0,0)
                elif p == 255:
                    if np.any(t == (0,0,0)) and np.any(r == (0,0,0)):
                        mc[i,j] = random.choice(list(colors_bgr.values()))
                    if np.any(t == (0,0,0)) and np.any(r != (0,0,0)):
                        mc[i,j] = r
                    if np.any(t != (0,0,0)) and np.any(r == (0,0,0)):
                        mc[i,j] = t
                    if np.any(t != (0,0,0)) and np.any(r != (0,0,0)):
                        mc[i,j] = r
    return mc

def get_ExifData(imagePath):
    exif_data = {}
    image = Image.open(imagePath)
    info = image.info
    if info:
        for tag, value in info.items():
            tagName = TAGS.get(tag, tag)
            exif_data[tagName] = value
    nombre = os.path.basename(imagePath)
    exif_data["Nombre"] = nombre
    fecha_creacion = os.path.getctime(imagePath)
    exif_data["Fecha de creación"] = fecha_creacion
    tamaño = os.path.getsize(imagePath)
    exif_data["Tamaño"] = tamaño
    ancho, alto = image.size
    exif_data["Dimensiones"] = ancho, "x", alto
    return exif_data
    
def ecualitation(hist, bins ):
    L = 255 # Número de niveles de intensidad en la imagen
    MN = ren*col # Número total de pixeles en la imagen
    n_k = {}
    s_k = {}
    pr_Aux = 0

    
    for freqInd, i in zip(hist, bins):
        n_k[i] = freqInd/MN
        print(f"r_k:{i}  n_k: {freqInd} Pr(n_k):{n_k[i]}")
    
    for i, prs in enumerate(n_k.values()):
        pr_Aux += prs
        s_k [i] = round(pr_Aux * (L-1))
        print(f"Para el nivel de gris --{i}-- ahora es: --{s_k[i]}--")

    
        
    return s_k




def main():
    # Matriz ecualizada
    mEq = np.zeros((ren, col), dtype=np.uint8)  

    # Matriz con etiquetas | cromtaizacion de regiones
    mc = np.zeros((ren, col, channels), dtype=np.uint8)

    # Matriz de 400x400 con valores aleatorios entre 0 y 255
    m = np.random.randint(0, 255, (ren, col))

    # salvando como imagen la matriz m (escala de grises)
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizM1.jpg", m)

    # Histograma de la matriz m
    # hist es la frecuencia de aparición de cada valor
    # bins es el rango de valores de 0 a 255
    hist, bins = np.histogram(m, bins=range(257))  # Crear histograma con 256 bins (de 0 a 255)


    '''NumPy internamente aplana la matriz en una sola dimensión, es decir, convierte la matriz en una lista 
    unidimensional. Luego, cuenta cuántas veces aparece cada valor en esta lista unidimensional dentro de 
    los bins especificados. El resultado es un vector con la frecuencia de aparición de cada valor.'''

    # Visualización del histograma
    plt.figure(1)  # Ajustar el tamaño de la ventana
    plt.bar(bins[:-1], hist, width=3)  # Crear el gráfico de barras
    plt.title('Histograma de Frecuencias de cada Valor 0-255')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    

    # Ecualización del histograma
    new_Levels_Gray = ecualitation(hist, bins)
    

    # Aplicar la ecualización a la matriz m
    valores_confirmados = set()  # Conjunto para almacenar los valores ya confirmados


    for i in range(len(m)):
        for j in range(len(m[i])):
            valor_m = m[i, j]  # Obtener el valor de m[i, j]
            if valor_m in new_Levels_Gray:  # Verificar si el valor está en las claves de s_k
                mEq[i, j] = new_Levels_Gray[valor_m]  # Asignar el nuevo valor de s_k a m[i, j]
                if valor_m not in valores_confirmados:
                    valores_confirmados.add(valor_m)
                    print(f"CONFIRMANDO...El valor {valor_m} ahora es {mEq[i, j]}")

    
    # Histograma de la matriz mEq
    
    hist2, bins2 = np.histogram(mEq, bins=range(257))  # Crear histograma con 256 bins (de 0 a 255)


    # Visualización del histograma
    plt.figure(2)  # Ajustar el tamaño de la ventana
    plt.bar(bins2[:-1], hist2, width=3)  # Crear el gráfico de barras
    plt.title('Histograma de Frecuencias de cada Valor 0-255')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    

   

    # proceso de binarización
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] > 123:
                mb[i][j] = 1*255
            else:
                mb[i][j] = 0*255
    
    
    # salvando como imagen la matriz binarizada (B/N)
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMb.jpg", mb)

  
    # Aplicar etiquetado de 4-adyacencia y asignar colores
    mc = etiquetado_4adyacente(mb, mc)

    # Guardar la matriz con etiquetas como una imagen JPEG y BMP y abrir ambas
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMc.jpg", mc)
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMc.bmp", mc)

    # Abrir la imagen con etiquetas
    os.system("start E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMc.jpg")
    os.system("start E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMc.bmp")


    # obtener los datos EXIF de las imagenes
    metadata = get_ExifData(imagepath)
    metadata2 = get_ExifData("matrizMc.bmp")

    # Imprimir los datos EXIF
    print("Datos EXIF de la imagen matrizMc.jpg")
    for tag, value in metadata.items():
        print(f"{tag}: {value}")
    print("\nDatos EXIF de la imagen matrizMc.bmp")
    for tag, value in metadata2.items():
        print(f"{tag}: {value}")

    plt.show()


if __name__ == "__main__":
    main()