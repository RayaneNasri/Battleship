import numpy as np
import matplotlib.pyplot as plt
import random
import math

def generate_grid(N: int) -> np.array:
    """
    Génère une grille carrée de dimensions N x N remplie de zéros, avec un point unique positionné à 1 
    basé sur une distribution normale centrée autour du milieu de la grille.

    Parameters
    ----------
    N : int
        Taille de la grille NxN à générer.

    Returns
    -------
    np.array
        Une grille 2D (tableau NumPy) de taille NxN remplie de zéros, à l'exception d'un seul point 
        ayant la valeur 1, positionné en fonction de coordonnées générées aléatoirement selon 
        une distribution normale.
    """

    x = int(random.normalvariate(N / 2, 1))
    y = int(random.normalvariate(N / 2, 1))

    grid = np.zeros((N, N))
    grid[x][y] = 1
    
    return grid

def generate_random_probability_grid(N: int) -> np.array:
    """
    Génère une grille de probabilités aléatoires de dimensions N x N, où 
    les valeurs au centre de la grille sont plus probables que celles des bords. 
    La somme des valeurs dans la grille est normalisée à 1.

    Parameters
    ----------
        N (int): La taille de la grille à générer. La grille aura la dimension 
                  N x N.

    Returns
    -------
    np.array: 
        Un tableau NumPy de dimensions N x N contenant des probabilités. La somme des valeurs dans ce tableau sera égale à 1.
    """

    # Génération d'une grille de taille N x N avec des valeurs aléatoires
    grid: np.array = np.random.rand(N, N)

    # Calcule du centre de la grille
    center = (N - 1) // 2

    # Appliquer un facteur de distance pour diminuer les valeurs en s'éloignant du centre
    factor: np.array = np.zeros((N, N))  # Correction de l'initialisation du tableau
    for i in range(N):
        for j in range(N):
            distance = np.sqrt((i - center) ** 2 + (j - center) ** 2)
            factor[i][j] = np.exp(-distance)  # Diminuer les valeurs avec la distance

    # Multiplier les valeurs aléatoires par le facteur de distance
    grid *= factor
    grid_sum = np.sum(grid)

    # Normaliser la grille pour que la somme soit égale à 1
    if grid_sum > 0:
        grid /= grid_sum

    return grid

def maximise(grid: np.array) -> tuple[int, int]:
    """
    Sélectionne et retourne la position (x, y) de la case ayant la plus grande probabilité dans la grille.
    Utilise la fonction 'np.argmax' pour trouver l'index de la valeur maximale dans le tableau 'grid',
    puis le convertit en coordonnées (x, y) avec `np.unravel_index`.

    Parameters
    ----------
    prob : np.array
        Un tableau numpy 2D contenant des probabilités.

    Returns
    -------
    tuple[int][int] :
        Un tuple (x, y) représentant la position de la case ayant la plus grande probabilité dans la grille.
    """
    return np.unravel_index(np.argmax(grid), (grid.shape))

def check(grid: np.array, position: tuple[int, int], ps) -> bool:
    """
    Vérifie si un capteur détecte correctement un point de la grille (marqué par la valeur 1), avec une probabilité d'exactitude donnée.

    Parameters
    ----------
    grid : np.array
        La grille 2D de dimensions NxN contenant des valeurs 0 et 1, où 1 représente un point d'intérêt.
    
    position : tuple[int, int]
        Coordonnées (x, y) sur la grille où le capteur va vérifier la présence du point d'intérêt.
    
    ps : float, optionnel
        La probabilité (entre 0 et 1) que le capteur détecte correctement la présence du point d'intérêt à la position donnée.
        La valeur par défaut est 0.8, ce qui signifie que le capteur détecte correctement dans 80% des cas.

    Returns
    -------
    bool
        'True' si le capteur détecte correctement le point d'intérêt (basé sur la probabilité ps), sinon 'False'.
        Si le point d'intérêt n'est pas présent à la position donnée dans la grille (c'est-à-dire 'grid[x][y] != 1'), retourne également 'False'.
    """

    x, y = position

    if(grid[x][y] == 1):
        rand = random.random()

        if(rand < ps):
            return True
    
    return False

def scorpion(grid: np.array, ps: float = 0.8) -> int:
    """
    Implémente l'algorithme du scorpion pour optimiser une grille probabiliste.
    
    L'objectif est de maximiser une grille probabiliste `random_probability_grid` jusqu'à ce qu'une certaine condition 
    soit remplie, évaluée par la fonction `check`. Cette fonction met à jour les probabilités dans la grille en 
    fonction de la règle d'actualisation.

    Parameters
    ----------
    grid : np.array
        Une matrice N x N représentant l'état actuel du problème.
        
    ps : float, optionnel (par défaut = 1.0)
        La probabilité de sélection pour le scorpion. Il influence la mise à jour des probabilités dans la grille.

    Returns
    -------
    int
        Le nombre d'itérations nécessaires pour remplir la condition `check`.
    """
    
    # Génération de la grille de probabilités aléatoires
    random_probability_grid: np.array = generate_random_probability_grid(grid.shape[0])

    # Nombre d'itérations
    iterations = 1

    # Maximisation initiale de la grille
    x, y = maximise(random_probability_grid)

    # Boucle jusqu'à ce que la condition soit remplie
    while not check(grid, (x, y), ps):
        pi_k = random_probability_grid[x][y]

        # Mise à jour de la probabilité pour la case sélectionnée
        random_probability_grid[x][y] = ((1 - ps) * pi_k) / (1 - ps * pi_k)

        # Mise à jour des autres cases
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if (i, j) != (x, y):
                    random_probability_grid[i][j] = random_probability_grid[i][j] / (1 - ps * pi_k)

        # Maximisation après mise à jour
        x, y = maximise(random_probability_grid)
        iterations += 1

    return iterations

def estimation_de_la_distribution_sco(N: int, p: float):
    """
    Réalise N simulations de parties aléatoires et calcule la distribution empirique du nombre d'itérations nécessaires 
    pour trouver l'objet égaré. La distribution est représentée sous la forme d'un dictionnaire, où chaque clé 
    correspond à un nombre d'itérations, et la valeur associée représente la fréquence d'apparition de ce nombre.

    La fonction effectue les étapes suivantes :
    1. Génère une grille de jeu pour chaque simulation.
    2. Calcule le nombre d'itérations pour chaque simulation à l'aide de la fonction `scorpion`.
    3. Met à jour la fréquence d'apparition de chaque nombre d'itérations dans un dictionnaire.
    4. Calcule la moyenne et l'écart-type des nombres d'itérations à partir des fréquences.

    Parameters
    ----------
    N : int  
        Le nombre de simulations à réaliser.
    p : float
        La précision du senseur.
        
    Returns
    -------
    None
        Les résultats (moyenne et écart-type) sont affichés à l'écran.
    """
    res = {}
    for i in range(N):
        grid = generate_grid(10)
        tmp = scorpion(grid, p)  # Calcul du nombre de coups joués pour cette partie.
        res[tmp] = res.get(tmp, 0) + 1  # Mise à jour de la fréquence pour ce nombre de coups.

    # Affichage de l'histogramme
    plt.bar(res.keys(), res.values(), color='blue')
    plt.xlabel('Nombre d\'itérations')
    plt.ylabel('Fréquence')
    plt.title(f'Distribution du nombre d\'itérations sur {N} simulations')
    plt.show()

    # Calcul de la somme des fréquences
    total_freq = sum(res.values())

    # Calcul de la moyenne pondérée
    mean = sum(val * freq for val, freq in res.items()) / total_freq

    # Calcul de l'écart-type pondéré
    variance = sum(freq * (val - mean) ** 2 for val, freq in res.items()) / total_freq
    std_dev = math.sqrt(variance)

    # Affichage des résultats
    print("Moyenne :", mean)
    print("Écart-type :", std_dev)

