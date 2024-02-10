import numpy as np
import matplotlib.pyplot as plt


m = [1,2,3],[1,5,6],[7,8,9]

def main():

    print(m)
     # Histograma de la matriz m
    hist, bins = np.histogram(m, bins=range(11))  # Crear histograma con 256 bins (de 0 a 255)

    '''NumPy internamente aplana la matriz en una sola dimensión, es decir, convierte la matriz en una lista 
    unidimensional. Luego, cuenta cuántas veces aparece cada valor en esta lista unidimensional dentro de 
    los bins especificados. El resultado es un vector con la frecuencia de aparición de cada valor.'''

    # Visualización del histograma
    plt.bar(bins[:-1], hist, width=1)  # Crear el gráfico de barras
    plt.xticks(np.arange(0, 10, 1)) # Marcar graduación del eje x desde 0 hasta 10 cada unidad
    print(hist)
    plt.title('Histograma de Frecuencias')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.show()

   
if __name__ == "__main__":
    main()