# Les imports
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

# Variables globales
bateaux: dict[int, int] = {1:2, 2:3, 3:3, 4:4, 5:5}
bateaux_inv = {val: key for key, val in bateaux.items()}

# 1 Modélisation et fonctions simples

def peut_placer_bateau(grille: np.array, indice_bateau: int, position: tuple[int, int], est_vertical: bool) -> bool:
    """
    Vérifie si un bateau peut être placé sur la grille à la position donnée et dans la direction spécifiée.

    Parameters
    ----------
    grille : np.array
        Un tableau 2D représentant la grille de jeu. Les cases vides sont marquées par des 0, 
        et les cases occupées par un bateau sont marquées par une autre valeur.
    indice_bateau : int
        L'indice du bateau à placer dans la liste 'bateaux', représentant sa taille.
    position : tuple[int, int]
        La position initiale (x, y) où commencer le placement du bateau.
    est_vertical : bool
        Si `True`, le bateau est placé verticalement (de haut en bas).
        Si `False`, le bateau est placé horizontalement (de gauche à droite).

    Returns
    -------
    bool
        Retourne `True` si le bateau peut être placé sans sortir de la grille ni entrer en collision 
        avec un autre bateau, sinon retourne `False`.
    """
    
    x, y = position  # Coordonnées initiales de placement du bateau
    taille_bateau = bateaux[indice_bateau]  # Récupération de la taille du bateau

    # Boucle pour vérifier chaque case où le bateau sera placé
    while taille_bateau > 0:
        # Vérifie si la position actuelle est hors de la grille ou si la case est déjà occupée
        if not (0 <= x <= 9 and 0 <= y <= 9) or grille[x][y] != 0:
            return False

        # Déplacement des coordonnées selon la direction (verticale ou horizontale)
        if est_vertical:
            x += 1  # Déplacement vers le bas
        else:
            y += 1  # Déplacement vers la droite
        
        taille_bateau -= 1  # Réduction de la taille restante du bateau à placer

    return True

def placer_bateau(grille: np.array, indice_bateau: int, position: tuple[int, int], est_vertical: bool) -> np.array:
    """
    Place un bateau sur la grille à la position et dans la direction spécifiées.
    
    Attention : Cette fonction ne vérifie pas si le placement est valide. Il est recommandé 
    d'utiliser une fonction de validation avant d'appeler cette fonction.
    
    Parameters
    ----------
    grille : np.array
        Un tableau 2D représentant la grille de jeu. Les cases vides sont marquées par des 0, 
        et les cases occupées par un bateau sont marquées avec l'indice du bateau.
    indice_bateau : int
        L'indice du bateau à placer dans la liste 'bateaux', représentant sa taille.
    position : tuple[int, int]
        La position initiale (x, y) où commencer le placement du bateau.
    est_vertical : bool
        Si `True`, le bateau est placé verticalement (de haut en bas).
        Si `False`, le bateau est placé horizontalement (de gauche à droite).

    Returns
    -------
    np.array
        Retourne la grille mise à jour avec le bateau placé.
    """
    
    x, y = position  # Coordonnées initiales du placement
    taille_bateau = bateaux[indice_bateau]  # Récupère la taille du bateau

    # Boucle pour placer le bateau sur la grille
    while taille_bateau > 0:
        grille[x][y] = indice_bateau  # Place l'indice du bateau dans la grille

        # Déplacement des coordonnées selon la direction (verticale ou horizontale)
        if est_vertical:
            x += 1  # Déplacement vers le bas
        else:
            y += 1  # Déplacement vers la droite
        
        taille_bateau -= 1  # Réduction de la taille restante à placer

    return grille

def placer_bateau_aleatoire(grille: np.array, indice_bateau: int) -> np.array:
    """
    Place aléatoirement un bateau sur la grille. Une position et une direction sont 
    tirées aléatoirement jusqu'à trouver un placement admissible.

    Parameters
    ----------
    grille : np.array
        Tableau 2D représentant la grille de jeu.
    indice_bateau : int
        L'indice du bateau à placer dans la liste 'bateaux', représentant sa taille.

    Returns
    -------
    np.array
        La grille mise à jour avec le bateau placé de manière aléatoire.
    """

    # Tirage aléatoire d'une position (x, y) dans la grille
    x = random.randint(0, grille.shape[0] - 1)
    y = random.randint(0, grille.shape[1] - 1)

    # Tirage aléatoire d'une direction (True pour vertical, False pour horizontal)
    est_vertical = random.choice([True, False])

    # Vérifier jusqu'à obtenir un placement valide
    while not peut_placer_bateau(grille, indice_bateau, (x, y), est_vertical):
        # Tirage de nouvelles positions aléatoires si le placement n'est pas possible
        x = random.randint(0, grille.shape[0] - 1)
        y = random.randint(0, grille.shape[1] - 1)
        est_vertical = random.choice([True, False])

    # Placer le bateau une fois la position et la direction valides trouvées
    return placer_bateau(grille, indice_bateau, (x, y), est_vertical)

def afficher_grille(grille: np.array):
    """
    Affiche la grille de jeu avec des couleurs pour différencier les cases vides et les bateaux.

    Parameters
    ----------
    grille : np.array
        Un tableau 2D représentant la grille de jeu, où les valeurs non nulles représentent les bateaux 
        et les 0 représentent les cases vides.
    """
    plt.figure(figsize=(6, 6))  # Définir la taille de la figure
    plt.imshow(grille, cmap='ocean', interpolation='nearest')  # Choisir un colormap pour représenter la mer et les bateaux
    plt.colorbar(label="Indice du bateau")  # Ajouter une barre de couleurs pour identifier les bateaux
    plt.title("Grille de jeu")  # Ajouter un titre
    plt.grid(False)  # Désactiver la grille
    plt.show()  # Afficher la grille

def grilles_egales(grilleA: np.array, grilleB: np.array) -> bool:
    """
    Compare deux grilles et retourne `True` si elles sont identiques, `False` sinon.

    Parameters
    ----------
    grilleA : np.array
        La première grille de jeu à comparer.
    grilleB : np.array
        La deuxième grille de jeu à comparer.

    Returns
    -------
    bool
        `True` si les deux grilles sont identiques, sinon `False`.
    """
    return np.array_equal(grilleA, grilleB)

def generer_grille_aleatoire() -> np.array:
    """
    Génère une grille de jeu avec tous les bateaux disposés de manière aléatoire.
    
    La grille est initialisée avec des cases vides (0), puis cinq bateaux sont placés de manière aléatoire 
    avec des indices correspondant à leur taille (1 à 5).

    Returns
    -------
    np.array
        Une grille 10x10 avec les bateaux placés aléatoirement. Les cases vides sont marquées par des 0 
        et les cases avec un bateau sont marquées avec l'indice du bateau.
    """
    
    # Initialiser une grille 10x10 avec des zéros (cases vides)
    grille = np.zeros((10, 10))

    # Boucle pour placer 5 bateaux sur la grille (indices 1 à 5)
    for indice_bateau in range(1, 6):
        grille = placer_bateau_aleatoire(grille, indice_bateau)

    return grille

# 2 Combinatoire du jeu

# Une borne supérieure simple du nombre de configurations possibles pour la liste complète de bateaux sur une grille de taille 10 serai = ∑ 220 - 40t

def compter_placements(bateau: int, grille: np.array = np.zeros((10, 10))) -> int:
    """
    Calcule le nombre de façons de placer un bateau dans une grille donnée.

    La fonction itère sur chaque case de la grille et vérifie si le bateau peut y être placé
    dans les deux orientations possibles (verticale et horizontale). 

    Parameters
    ----------
    bateau : int
        L'indice du bateau à placer, représentant sa taille.
    grille : np.array, optional
        La grille sur laquelle le bateau doit être placé. Par défaut, une grille vide 10x10 est utilisée.

    Returns
    -------
    int
        Le nombre total de façons de placer le bateau sur la grille.
    """
    
    res = 0  # Compteur pour le nombre de placements possibles
    
    # Itérer sur chaque case de la grille
    for i in range(10):
        for j in range(10):
            # Vérifier le placement horizontal (direction = 0)
            if peut_placer_bateau(grille, bateau, (i, j), 0):
                res += 1
            # Vérifier le placement vertical (direction = 1)
            if peut_placer_bateau(grille, bateau, (i, j), 1):
                res += 1
                
    return res

def compter_placements_bateaux(bateaux: list[int], grille: np.array = np.zeros((10, 10))) -> int:
    """
    Calcule le nombre de façons de placer une liste de bateaux sur une grille vide.

    La fonction utilise la récursion pour essayer de placer chaque bateau dans toutes les 
    positions et orientations possibles, puis continue avec le reste des bateaux.

    Parameters
    ----------
    bateaux : list[int]
        Une liste contenant les indices (tailles) des bateaux à placer.
    grille : np.array, optional
        La grille sur laquelle les bateaux doivent être placés. Par défaut, une grille vide 10x10 est utilisée.

    Returns
    -------
    int
        Le nombre total de façons de placer tous les bateaux sur la grille.
    """
    
    # Si la liste ne contient qu'un seul bateau, on utilise la fonction pour compter les placements d'un seul bateau
    if len(bateaux) == 1:
        return compter_placements(bateaux[0], grille)
    
    res = 0  # Compteur pour le nombre de placements possibles
    
    # Itérer sur chaque case de la grille
    for i in range(10):
        for j in range(10):
            # Vérifier le placement horizontal (direction = 0)
            if peut_placer_bateau(grille, bateaux[0], (i, j), 0):
                grille_tmp = grille.copy()  # Faire une copie de la grille pour ne pas affecter la grille originale
                grille_tmp = placer_bateau(grille_tmp, bateaux[0], (i, j), 0)  # Placer le bateau
                # Appel récursif pour le reste des bateaux
                res += compter_placements_bateaux(bateaux[1:], grille_tmp)
            
            # Vérifier le placement vertical (direction = 1)
            if peut_placer_bateau(grille, bateaux[0], (i, j), 1):
                grille_tmp = grille.copy()  # Faire une copie de la grille
                grille_tmp = placer_bateau(grille_tmp, bateaux[0], (i, j), 1)  # Placer le bateau
                # Appel récursif pour le reste des bateaux
                res += compter_placements_bateaux(bateaux[1:], grille_tmp)
    
    return res

# Le nombre de grilles pour la liste complète de bateau est égale au nombre de façon de placer la liste de bateaux sur une grille vide.
# Dans le cas où les grille sont equiprobables, le lien entre le nombre de grille "n" et la probabilité de tombé sur une grille donné est P = 1/n.

def nombre_generations_grille(grille: np.array) -> int:
    """
    Retourne le nombre de grilles générées aléatoirement avant d'obtenir une grille identique 
    à celle fournie en paramètre. Utilise une méthode de force brute.

    La fonction génère des grilles aléatoires jusqu'à ce qu'une grille identique à celle donnée 
    soit générée, en comptant le nombre d'essais.

    Parameters
    ----------
    grille : np.array
        La grille de référence à laquelle on veut comparer les grilles générées.

    Returns
    -------
    int
        Le nombre de grilles générées avant d'obtenir une grille identique à celle fournie.
    """
    
    res = 1  # Initialiser le compteur de générations
    grille_tmp = generer_grille_aleatoire()  # Générer la première grille aléatoire
    
    # Boucle jusqu'à ce que la grille générée soit identique à la grille de référence
    while not grilles_egales(grille, grille_tmp):
        res += 1
        grille_tmp = generer_grille_aleatoire()  # Générer une nouvelle grille
    
    return res

def findLambda(N: int) -> float:
    """
    Calcule la proportion de grilles valides où aucun des bateaux ne se chevauche après 
    avoir placé 5 bateaux dans une grille 10x10.

    La fonction génère N grilles aléatoires et place des bateaux sur chacune en s'assurant
    que les bateaux sont placés soit horizontalement soit verticalement. Elle calcule ensuite
    la proportion de grilles dans lesquelles les bateaux ne se chevauchent pas.

    Parameters
    ----------
    - N (int): Le nombre de grilles à générer.

    Returns
    -------
    - float: La proportion de grilles valides (sans chevauchement de bateaux).
    """

    # Compteur des grilles valides (sans chevauchement)
    n: int = 0
    
    for _ in range(N):
        # L'ensemble des cases occupée.
        S: set[tuple[int, int]] = set()
        valid: bool = True

        for z in range(1, 6):
            # Génération aléatoire des positions et direction du bateau
            direction: int = random.randint(0, 1)

            if direction == 0:  # Placement horizontal
                x: int = random.randint(0, 9)
                y: int = random.randint(0, 9)
                while y + bateaux[z] - 1 > 9:  # Vérifier les limites de la grille
                    y = random.randint(0, 9)
                tmp = {(x, y + k) for k in range(bateaux[z])}
            else:  # Placement vertical
                x: int = random.randint(0, 9)
                y: int = random.randint(0, 9)
                while x + bateaux[z] - 1 > 9:  # Vérifier les limites de la grille
                    x = random.randint(0, 9)
                tmp = {(x + k, y) for k in range(bateaux[z])}
 
            # Vérification des chevauchements avec l'intersection
            if len(S & tmp) != 0:
                valid = False
            S = S | tmp
        # Incrémenter si aucune intersection (grille valide)
        n += 1 if valid else 0

    # Retourner la proportion de grilles valides
    return n / N