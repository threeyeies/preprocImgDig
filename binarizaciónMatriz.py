import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

ren = 400
col = 400
channels = 3 # RGB
prom = 123 # Promedio de la matriz m
mb = np.zeros((ren, col),dtype=np.uint8) # Matriz binarizada

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



def main():
    # Matriz con etiquetas | cromtaizacion de regiones
    mc = np.zeros((ren, col, channels), dtype=np.uint8)

    # Matriz de 400x400 con valores aleatorios entre 0 y 255
    m = np.random.randint(0, 255, (ren, col))

    # salvando como imagen la matriz m (escala de grises)
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizM1.jpg", m)

     # Histograma de la matriz m
    hist, bins = np.histogram(m, bins=range(257))  # Crear histograma con 256 bins (de 0 a 255)

    '''NumPy internamente aplana la matriz en una sola dimensión, es decir, convierte la matriz en una lista 
    unidimensional. Luego, cuenta cuántas veces aparece cada valor en esta lista unidimensional dentro de 
    los bins especificados. El resultado es un vector con la frecuencia de aparición de cada valor.'''

    # Visualización del histograma
    plt.bar(bins[:-1], hist, width=3)  # Crear el gráfico de barras
    plt.title('Histograma de Frecuencias de cada Valor 0-255')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.show()

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

    # Guardar la matriz con etiquetas como una imagen JPEG
    cv2.imwrite("E:\\Lenovo\\Documents\\DIAMCRUST\\CODING\\SPACEWORK\\PYTHON\\procesamientoDeImagenes\\matrizMc.jpg", mc)
                
    print(mb[:1, :10])
    print(mc[:1, :10])

if __name__ == "__main__":
    main()