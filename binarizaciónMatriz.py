import numpy as np
import cv2
import matplotlib.pyplot as plt

ren = 400
col = 400
prom = 123
mb = np.zeros((ren, col))

def main():
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

if __name__ == "__main__":
    main()