import matplotlib.pyplot as plt
import numpy as np

def visualize_route(route, grid_size=(24, 24)):
    # Crear una matriz de ceros
    grid = np.zeros(grid_size)
    route = [(y, x) for (x, y) in route]  # Invertir el eje y

    # Marcar la ruta en la matriz
    for (x, y) in route:
        grid[grid_size[1] - 1 - y, x] = 1  # Marcar la celda como parte de la ruta

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Mostrar la matriz como una imagen
    ax.imshow(grid, cmap='Greys', interpolation='none')

    # Añadir etiquetas a los ejes
    ax.set_xticks(np.arange(grid_size[0]))
    ax.set_yticks(np.arange(grid_size[1]))
    ax.set_xticklabels(np.arange(1, grid_size[0] + 1))
    ax.set_yticklabels(np.arange(1, grid_size[1] + 1))

    # Añadir una cuadrícula
    ax.grid(which='both', color='black', linestyle='-', linewidth=1)

    # Mostrar la figura
    plt.show()

# Ejemplo de uso
route = [(19, 5), (18, 5), (18, 6), (17, 6)]
visualize_route(route)