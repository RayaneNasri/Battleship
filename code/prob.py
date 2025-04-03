import numpy as np
import matplotlib.pyplot as plt
import random

from mod import generer_grille_aleatoire, bateaux

# Implémentation des classes

class Bataille:
    # Attributs
    grille: np.array

    # Constructeur
    def __init__(self)-> None:
        self.grille = generer_grille_aleatoire()
    

    # Méthodes
    def joue(self, position: tuple[int, int]) -> int:
        """
        Cible la position passée en paramètre et vérifie s'il y a un bateau à cette position.
        Si un bateau est touché (grille[x][y] != 0), il est retiré de la grille (grille[x][y] = 0) 
        et la fonction retourne le numéro du bateau touché. Sinon, elle retourne 0 (aucun bateau).

        Parameters
        ----------
        position : tuple[int, int]
            Les coordonnées (x, y) de la position à cibler sur la grille.

        Returns
        -------
        int :
            Le numéro du bateau touché (si un bateau est à la position donnée) ou 0 si aucun bateau n'est touché.
        """
        
        x, y = position  # Décompose le tuple en coordonnées x et y
        
        # Si la position cible contient un bateau (grille[x][y] != 0)
        if self.grille[x][y] != 0:
            bateau_touche = self.grille[x][y]  # Sauvegarde le numéro du bateau touché
            self.grille[x][y] = 0  # Retire le bateau de la grille (marque la case comme vide)
            return bateau_touche  # Retourne le numéro du bateau touché
        
        return 0  # Retourne 0 si aucune partie de bateau n'a été touchée
    
    def victoire(self) -> bool:
        """
        Vérifie si le joueur a gagné en vérifiant que tous les bateaux ont été coulés.

        Returns
        -------
        bool :
            True si tous les bateaux ont été coulés (c'est-à-dire si la grille ne contient que des zéros), 
            sinon False.
        """
        
        # Vérifie si la grille est entièrement remplie de zéros (c'est-à-dire qu'il n'y a plus de bateaux).
        return np.array_equal(self.grille, np.zeros((10, 10)))

    
    def reset(self) -> None:
        """
        Réinitialise le jeu en générant une nouvelle grille de jeu avec des bateaux placés aléatoirement.
        La grille actuelle est remplacée par une nouvelle grille générée.
        """
        self.grille = generer_grille_aleatoire()


class Joueur:
    
    # Version aléatoire.
    def jouer_alea(self, b: Bataille) -> int:
        """
        Joue aléatoirement des coups sur la grille de la partie 'Bataille' jusqu'à ce que le joueur gagne.
        Les positions déjà jouées sont stockées pour éviter de tirer plusieurs fois la même position.

        Parameters
        ----------
        b : Bataille
            Instance de la classe 'Bataille' représentant le jeu en cours.

        Returns
        -------
        int :
            Le nombre de coups joués avant que la victoire soit obtenue.
        """
        
        res: int = 0  # Compteur du nombre de coups joués
        ensemble_positions: set[tuple[int, int]] = set()  # Ensemble qui stocke les positions déjà jouées
        
        # Tant que la victoire n'est pas atteinte (il reste des bateaux sur la grille)
        while not b.victoire():
            # Tirer aléatoirement une position (ligne et colonne)
            x = int(random.random() * b.grille.shape[0])  # Ligne aléatoire
            y = int(random.random() * b.grille.shape[1])  # Colonne aléatoire
            
            # Si la position a déjà été jouée, tirer une nouvelle position
            while (x, y) in ensemble_positions:
                x = int(random.random() * b.grille.shape[0])  # Nouvelle ligne aléatoire
                y = int(random.random() * b.grille.shape[1])  # Nouvelle colonne aléatoire

            # Incrémenter le nombre de coups joués
            res += 1
            b.joue((x, y))  # Jouer à la position (x, y)
            ensemble_positions.add((x, y))  # Ajouter la position au set des positions jouées

        return res  # Retourner le nombre total de coups joués

    
    def shout(self, b, ensemble_positions: set[tuple[int, int]], position: tuple[int, int]) -> int:
        """
        Tente de détruire complètement un bateau à partir d'une position donnée en explorant dans toutes les directions
        (haut, bas, gauche, droite) jusqu'à épuiser les possibilités.

        Parameters
        ----------
        b : Bataille
            Instance de la classe 'Bataille' représentant le plateau de jeu contenant la grille.
        ensemble_positions : set[tuple[int, int]]
            Ensemble des positions déjà attaquées, pour éviter de tirer plusieurs fois sur les mêmes cases.
        position : tuple[int, int]
            Position initiale (x, y) où un bateau a été détecté.

        Returns
        -------
        int :
            Le nombre total de coups effectués (incluant les coups qui n'ont pas touché).
        """
        
        res = 0  # Nombre de coups effectués
        x, y = position  # Décompose la position initiale en x et y

        # Initialise les directions possibles : [droite, bas, gauche, haut]
        directions = [1, 1, 1, 1]
        
        # Désactiver certaines directions si elles ne sont pas possibles
        if x == 0 or (x - 1, y) in ensemble_positions:  # Pas de déplacement vers le haut
            directions[3] = 0
        if x == b.grille.shape[0] - 1 or (x + 1, y) in ensemble_positions:  # Pas de déplacement vers le bas
            directions[1] = 0
        if y == 0 or (x, y - 1) in ensemble_positions:  # Pas de déplacement vers la gauche
            directions[2] = 0
        if y == b.grille.shape[1] - 1 or (x, y + 1) in ensemble_positions:  # Pas de déplacement vers la droite
            directions[0] = 0

        # Tant qu'il reste des directions à explorer
        while sum(directions) > 0:
            # Choisir aléatoirement une direction parmi celles disponibles
            rand = random.randint(0, 3)
            while not directions[rand]:  # Si la direction choisie n'est plus valide, en choisir une autre
                rand = random.randint(0, 3)

            if rand == 0:  # Vers la droite (y augmente)
                y += 1
                while y < b.grille.shape[1]:
                    res += 1
                    if b.grille[x][y] != 0:  # Si un bateau est touché
                        b.grille[x][y] = 0  # Détruire la case
                        ensemble_positions.add((x, y))
                    else:  # Si la case est vide, on arrête d'explorer cette direction
                        ensemble_positions.add((x, y))
                        break
                    y += 1
                x, y = position  # Retour à la position initiale
                directions[rand] = 0  # Désactiver cette direction

            elif rand == 1:  # Vers le bas (x augmente)
                x += 1
                while x < b.grille.shape[0]:
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    x += 1
                x, y = position
                directions[rand] = 0

            elif rand == 2:  # Vers la gauche (y diminue)
                y -= 1
                while y >= 0:
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    y -= 1
                x, y = position
                directions[rand] = 0

            else:  # Vers le haut (x diminue)
                x -= 1
                while x >= 0:
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    x -= 1
                x, y = position
                directions[rand] = 0

        return res  # Retourne le nombre total de coups effectués


    def jouer_heuristique(self, b: Bataille):
        """
        Cette fonction permet de jouer une partie de bataille navale en suivant une heuristique simple.
        Le joueur tire aléatoirement des coups sur la grille jusqu'à ce que tous les bateaux soient coulés.

        L'algorithme fonctionne en tirant aléatoirement une position (x, y) sur la grille. Si un bateau est touché,
        il tente de le couler complètement. Le jeu continue jusqu'à ce que la fonction 'victoire' de l'objet 'Bataille'
        renvoie `True`, signifiant que tous les bateaux sont détruits.

        Parameters
        ----------
        b : Bataille
            Un objet de la classe 'Bataille', qui contient la grille de jeu ainsi que les méthodes pour gérer l'état du jeu (comme jouer un coup ou vérifier la victoire).

        Returns
        -------
        int :
            Le nombre total de coups nécessaires pour couler tous les bateaux.
        """

        # Initialisation du nombre de coups effectués
        res: int = 0

        # Un ensemble pour garder une trace des positions déjà jouées (éviter de rejouer au même endroit)
        ensemble_positions: set[tuple[int, int]] = set()

        # Boucle principale du jeu : continue tant que tous les bateaux ne sont pas coulés
        while not b.victoire():
            # Tirage aléatoire d'une position sur la grille
            x = random.randint(0, b.grille.shape[0] - 1)  # Choisit une ligne au hasard
            y = random.randint(0, b.grille.shape[1] - 1)  # Choisit une colonne au hasard

            # Si la position a déjà été jouée, tirer de nouveau jusqu'à trouver une position non jouée
            while (x, y) in ensemble_positions:
                x = random.randint(0, b.grille.shape[0] - 1)
                y = random.randint(0, b.grille.shape[1] - 1)

            # Ajouter cette position à l'ensemble des positions jouées
            ensemble_positions.add((x, y))

            # Jouer à la position (x, y) et obtenir l'Id du bateau touché (i > 0 si un bateau est touché)
            i = b.joue((x, y))

            # Si un bateau est touché, tenter de le couler complètement
            if i > 0:
                # La méthode `shout` est appelée pour couler le bateau autour de la position touchée (x, y)
                res += self.shout(b, ensemble_positions, (x, y))

            # Incrémenter le nombre total de coups joués (coup initial + tentatives de couler le bateau)
            res += 1

        # Retourner le nombre total de coups nécessaires pour remporter la partie
        return res
    
    # Version probabiliste simple.
    def update_prob(self, prob: np.array, bateau: int, position: tuple[int, int], direction: bool, interdites: set[tuple[int, int]]) -> bool:
        """
        Met à jour la matrice des probabilités en fonction du placement potentiel d'un bateau sur la grille.
        
        Cette fonction augmente les probabilités des cellules où le bateau pourrait être placé et vérifie si le placement 
        est valide (par exemple, s'il y a des restrictions dues à d'autres bateaux ou s'il dépasse la grille).

        Parameters
        ----------

        prob : np.array
            Un tableau numpy 2D représentant la grille où chaque cellule contient une probabilité.
        bateau : int 
            Un entier représentant l'index du bateau à placer. Sa longueur est déterminée par le tableau global `bateaux`.
        position : tuple[int, int]
            Un tuple (x, y) indiquant la position de départ du bateau sur la grille.
        direction : bool
            Un booléen indiquant la direction du bateau :
                    - 'True' pour un placement vertical (de haut en bas).
                    - 'False' pour un placement horizontal (de gauche à droite).
        interdites : set[tuple[int, int]]
            Un ensemble de tuples (x, y) représentant les cellules où les bateaux ne peuvent pas être placés.

        Returns
        -------

        bool : 
            'True' si la mise à jour a été effectuée avec succès, sinon 'False' si le placement du bateau est impossible.
        """
        
        # Extraire les coordonnées initiales (x, y) du tuple `position`
        x, y = position
        
        # Déterminer la longueur du bateau à partir du tableau global `bateaux`
        length = bateaux[bateau]
        
        # Cas où le bateau est placé verticalement
        if direction:
            # Calculer la limite finale sur l'axe vertical (axe des x)
            limit = x + length - 1
            # Vérifier si le bateau dépasserait les limites de la grille
            if limit >= prob.shape[0]:
                return False  # Le bateau dépasse la grille, retour False

            # Parcourir les cellules sur lesquelles le bateau serait placé
            for i in range(length):
                # Vérifier si la cellule (x + i, y) est interdite
                if (x + i, y) in interdites:
                    # Si une cellule interdite est rencontrée, annuler toute mise à jour et retourner False
                    prob[x:x+i, y] -= 1  # Correction des modifications déjà faites
                    return False
                else:
                    # Si la cellule est valide, augmenter la probabilité à cet endroit
                    prob[x + i][y] += 1

        # Cas où le bateau est placé horizontalement
        else:
            # Calculer la limite finale sur l'axe horizontal (axe des y)
            limit = y + length - 1
            # Vérifier si le bateau dépasserait les limites de la grille
            if limit >= prob.shape[1]:
                return False  # Le bateau dépasse la grille, retour False

            # Parcourir les cellules sur lesquelles le bateau serait placé
            for i in range(length):
                # Vérifier si la cellule (x, y + i) est interdite
                if (x, y + i) in interdites:
                    # Si une cellule interdite est rencontrée, annuler toute mise à jour et retourner False
                    prob[x, y:y+i] -= 1  # Correction des modifications déjà faites
                    return False
                else:
                    # Si la cellule est valide, augmenter la probabilité à cet endroit
                    prob[x][y + i] += 1

        # Si toutes les cellules sont valides, retour True
        return True
    
    def create_prob(self, shape: tuple[int, int], ensemble_positions: set[tuple[int, int]], ensemble_positions_bateaux: set[tuple[int, int]]) -> np.array:
        """
            Génère une grille de probabilités pour le placement des bateaux, en tenant compte des positions interdites.

            Cette fonction crée une matrice de probabilités indiquant la faisabilité de placer un bateau dans chaque cellule. 
            Les cellules interdites, c'est-à-dire celles où un bateau ne peut pas être placé, ont une probabilité de 0.

            Parameters
            ----------

            shape : tuple[int, int])
                Un tuple représentant les dimensions de la grille (nombre de lignes, nombre de colonnes).
            ensemble_positions : set[tuple[int, int]]
                Un ensemble de tuples (x, y) indiquant les positions déjà jouées, où aucun bateau ne peut 
            être placé.
            ensemble_positions_bateaux : set[tuple[int, int]])
                Un ensemble de tuples (x, y) représentant les positions des bateaux déjà touchés 
            ou en cours de placement.

            Returns
            -------
            np.array :
                Un tableau numpy 2D où chaque cellule contient la somme des probabilités qu'un bateau puisse être placé à cet 
            endroit, en tenant compte des positions interdites et des bateaux déjà placés.
        """
        
        # Initialiser un tableau numpy de probabilités, de dimensions `shape`, avec toutes les cellules à 0
        prob = np.zeros(shape)

        # Parcourir chaque bateau à placer (les longueurs des bateaux sont stockées dans le tableau global `bateaux`)
        for x in bateaux:
            # Initialiser un tableau temporaire pour les probabilités de placement du bateau actuel
            tmp = np.zeros(shape)

            # Parcourir chaque cellule de la grille
            for i in range(shape[0]):
                for j in range(shape[1]):
                    # Si la cellule (i, j) est dans les positions interdites ou déjà occupées par un bateau, on l'ignore
                    if (i, j) not in (ensemble_positions - ensemble_positions_bateaux):
                        # Mise à jour des probabilités pour un placement vertical du bateau
                        self.update_prob(tmp, x, (i, j), True, ensemble_positions - ensemble_positions_bateaux)
                        # Mise à jour des probabilités pour un placement horizontal du bateau
                        self.update_prob(tmp, x, (i, j), False, ensemble_positions - ensemble_positions_bateaux)

            # Ajouter les probabilités calculées pour ce bateau à la grille globale de probabilités
            prob += tmp

        # Assurer que toutes les cellules interdites ou déjà occupées aient une probabilité de 0
        for x, y in ensemble_positions:
            prob[x, y] = 0

        return prob


    
    def select_max_prob(self, prob: np.array) -> tuple[int, int]:
        """
        Sélectionne et retourne la position (i, j) de la case ayant la plus grande probabilité dans la grille.

        Cette méthode utilise la fonction 'np.argmax' pour trouver l'index de la valeur maximale dans le tableau 'prob',
        puis convertit cet index en coordonnées (i, j) avec `np.unravel_index`.

        Parameters
        ----------
        prob : np.array 
            Un tableau numpy 2D contenant des probabilités.

        Returns
        -------
        tuple[int, int]:
            Un tuple (i, j) représentant la position de la case ayant la plus grande probabilité dans la grille.
        """
        # Trouve l'index de la valeur maximale dans le tableau de probabilités
        max_index = np.argmax(prob)
        
        # Convertit l'index 1D en coordonnées 2D (i, j) correspondant à la grille
        max_position = np.unravel_index(max_index, prob.shape)
        
        return max_position  # Retourne les coordonnées (i, j)

    def shoot_probabiliste(self, b: Bataille, prob: np.array, ensemble_positions: set[tuple[int, int]], ensemble_positions_bateaux: set[tuple[int, int]], position: tuple[int, int]):
        """
        Effectue des tirs probabilistes sur une grille de jeu pour tenter de couler un bateau.

        Parameters
        ----------

        b : Bataille 
            Une instance de la classe Bataille contenant une matrice 'grille'.
        prob : np.array 
            Un tableau numpy 2D contenant les probabilités associées à chaque position.
        ensemble_positions : [tuple[int, int] 
            Un ensemble pour stocker les positions déjà tirées.
        ensemble_positions_bateaux : [tuple[int, int]] 
            Un ensemble pour stocker les positions des bateaux touchés.
        position : tuple[int, int] 
            Un tuple (x, y) représentant la position actuelle de tir.

        Returns
        -------
        int :
            Le nombre total de coups effectués durant le tir.
        """
        res = 0  # Initialisation du nombre de coups effectués
        x, y = position  # Décomposition de la position initiale

        # Calcule des directions possibles (droite, bas, gauche, haut) avec les probabilités
        directions = {}  # Dictionnaire pour stocker les directions et leurs probabilités
        directions[0] = 0 if y == b.grille.shape[1] - 1 else prob[x, y + 1]  # Vers la droite
        directions[1] = 0 if x == b.grille.shape[0] - 1 else prob[x + 1, y]  # Vers le bas
        directions[2] = 0 if y == 0 else prob[x, y - 1]  # Vers la gauche
        directions[3] = 0 if x == 0 else prob[x - 1, y]  # Vers le haut

        # Continue tant qu'il reste des directions à explorer
        while sum(directions.values()) > 0:  
            # Sélectionne la meilleure direction selon la probabilité
            best: int = max(directions, key=directions.get)

            # Traite chaque direction possible
            if best == 0:  # Vers la droite (y augmente)
                y += 1
                while y < b.grille.shape[1]:  # Parcourt les cases vers la droite
                    res += 1  # Incrémente le compteur de coups
                    if b.grille[x][y] != 0:  # Si un bateau est touché
                        b.grille[x][y] = 0  # Marque la case comme détruite
                        ensemble_positions.add((x, y))  # Ajoute à l'ensemble des positions
                        ensemble_positions_bateaux.add((x, y))  # Ajoute à l'ensemble des bateaux
                    else:  # Si aucune touche
                        ensemble_positions.add((x, y))  # Ajoute à l'ensemble des positions
                        break  # Quitte la boucle
                    y += 1  # Avance vers la droite
                x, y = position  # Retourne à la position initiale
                directions[best] = 0  # Désactive cette direction

            elif best == 1:  # Vers le bas (x augmente)
                x += 1
                while x < b.grille.shape[0]:  # Parcourt les cases vers le bas
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                        ensemble_positions_bateaux.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    x += 1
                x, y = position
                directions[best] = 0

            elif best == 2:  # Vers la gauche (y diminue)
                y -= 1
                while y >= 0:  # Parcourt les cases vers la gauche
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                        ensemble_positions_bateaux.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    y -= 1
                x, y = position
                directions[best] = 0

            else:  # Vers le haut (x diminue)
                x -= 1
                while x >= 0:  # Parcourt les cases vers le haut
                    res += 1
                    if b.grille[x][y] != 0:
                        b.grille[x][y] = 0
                        ensemble_positions.add((x, y))
                        ensemble_positions_bateaux.add((x, y))
                    else:
                        ensemble_positions.add((x, y))
                        break
                    x -= 1
                x, y = position
                directions[best] = 0

        return res  # Retourne le nombre total de coups effectués


    def jouer_probabiliste_simple(self, b: Bataille) -> int:
        """
        Joue au jeu de la bataille navale en utilisant une approche probabiliste simple.

        Cette fonction génère un tableau de probabilités, et sélectionne la position ayant la plus grande probabilité. 
        Une fois un bateau touché, l'algorithme tente de le détruire en appelant shout_probabiliste.
        Le processus continue jusqu'à ce que tous les bateaux soient coulés.

        Parameters
        ----------
        b : Bataille 
            Un objet de la classe 'Bataille' qui contient la grille de jeu.

        Returns
        -------
        int :
            Le nombre total de coups nécessaires pour couler tous les bateaux.
        """
        res: int = 0  # Nombre total de coups effectués
        ensemble_positions: set[tuple[int, int]] = set()  # Ensemble des positions déjà jouées
        ensemble_positions_bateaux: set[tuple[int, int]] = set()  # Ensemble des positions où des bateaux ont été touchés

        # Tant qu'il reste des bateaux à détruire
        while not b.victoire():
            # Crée un tableau de probabilités pour les positions à jouer
            prob = self.create_prob(b.grille.shape, ensemble_positions, ensemble_positions_bateaux)
            
            # Sélectionne la position ayant la plus grande probabilité
            x, y = self.select_max_prob(prob)
            
            # Joue à la position (x, y)
            i = b.joue((x, y))

            # Si un bateau est touché
            if i > 0:
                # Tente de détruire le bateau et met à jour le nombre de coups
                res += self.shoot_probabiliste(b, prob, ensemble_positions, ensemble_positions_bateaux, (x, y))
                ensemble_positions_bateaux.add((x, y))  # Ajoute la position du bateau touché à l'ensemble

            ensemble_positions.add((x, y))  # Ajoute la position jouée à l'ensemble

            # Incrémente le nombre de coups après chaque tentative
            res += 1

        return res  # Retourne le nombre total de coups effectués

def estimation_de_la_distribution(N: int, function):
    """
    Réalise N simulations de parties aléatoires et calcule la distribution empirique du nombre de coups nécessaires 
    pour couler tous les bateaux. La distribution est retournée sous forme d'un dictionnaire où chaque clé représente 
    un nombre de coups, et la valeur associée représente sa fréquence d'apparition.
    
    Parameters
    ----------
    N : int  
        Le nombre de simulations à réaliser.
    function : Bataille-> int 
        Retourne le nombre de coups joués jusqu'à ce que tout les bateaux soient coulés.
    
    Returns
    -------
    dict[int, int] :
        Un dictionnaire associant à chaque nombre de coups joués sa fréquence d'apparition sur les N simulations.
    """
    b: Bataille = Bataille()  # Initialisation d'une instance du jeu Bataille.
    res: dict[int, int] = dict()  # Dictionnaire pour stocker la distribution du nombre de coups joués.

    for i in range(N):
        tmp = function(b)  # Calcul du nombre de coups joués pour cette partie.
        res[tmp] = res.get(tmp, 0) + 1  # Mise à jour de la fréquence pour ce nombre de coups.
        b.reset()  # Réinitialisation de la grille pour une nouvelle partie.
    
    # Affichage de l'histogramme
    plt.bar(res.keys(), res.values(), color='blue')
    plt.xlabel('Nombre de coups joués')
    plt.ylabel('Fréquence')
    plt.title(f'Distribution du nombre de coups joués sur {N} simulations')
    plt.show()

    return sum(c * val for c, val in res.items()) / N
