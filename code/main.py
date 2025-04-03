# Les imports
from mod import *
from prob import *
from sco import *

import sys

def option_1():
    # Récupérer un entier de l'utilisateur
    while True:
        n = input("Veuillez entrer un entier entre 1 et 5 : ")
        try:
            n = int(n)
            if(n < 1 or 5 < n):
                print("Entrée invalide.")
            else:
                print(f"Vous avez entré l'entier {n}.")
                break
        except ValueError:
            print("Entrée invalide, veuillez entrer un entier.")

    print("Valeur de retour : ", compter_placements(n))

def option_2():
    # Récupérer un entier et une liste d'entiers
    while True:
        try:        
            taille = int(input("Veuillez entrer la taille de la liste : "))
            liste = []
            for i in range(taille):
                while True:
                    try:
                        x = int(input(f"Entrez l'entier {i + 1} (entre 1 et 5) : "))
                        if x < 1 or x > 5:
                            raise ValueError("L'entier doit être entre 1 et 5.")
                        liste.append(x)
                        break
                    except ValueError as e:
                        print(e)
            print(f"Liste : {liste}")
            break
        except ValueError:
            print("Erreur : Veuillez entrer un entier valide.")
    print("Valeur de retour : ", compter_placements_bateaux(liste))

def option_3():
    # Récupérer un entier
    n = input("Veuillez entrer le nombre de grilles : ")
    while(True):
        try:
            n = int(n)
            print(f"Vous avez entré l'entier {n}.")
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un entier.")
    print("Valeur de retour : ", findLambda(n))

def option_4_5_6(option_number):
    # Récupérer un entier pour les options 4, 5, 6
    n = input(f"Merci de saisir le nombre de simulations : ")
    while(True):
        try:
            n = int(n)
            print(f"Vous avez entré l'entier {n}.")
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un entier.")

    j = Joueur()
    if(option_number == 4): 
        print("Valeur de retour : ", estimation_de_la_distribution(n, j.jouer_alea))
    elif(option_number == 5):
        print("Valeur de retour : ", estimation_de_la_distribution(n, j.jouer_heuristique))
    else:
        print("Valeur de retour : ", estimation_de_la_distribution(n, j.jouer_probabiliste_simple))


def option_7():
    # Récupérer un entier et un flottant entre 0 et 1
    while(True):
        try:
            n = int(input("Merci de saisir le nombre de simulations : "))
            p = float(input("Merci de saisir la precision du senseur entre 0 et 1 : "))
            if p < 0 or p > 1:
                raise ValueError("La précision doit être comprise entre 0 et 1.")
            print(f"Nombre de simulations : {n}, La précision du senseur : {p}")
            break
        except ValueError as e:
            print(f"Erreur : {e}")
    estimation_de_la_distribution_sco(n, p)

def main():
    print("===========================================")
    print("          Projet: Bataille Navale         ")
    print("===========================================")
    print("Auteur       : Rayane Nasri")
    print("Date         : 10/10/2024")
    print("===========================================")
    print("\nDémarrage du projet...\n")
    
    print("Les options :")
    print("Combinatoire du jeu")
    print(" -1- Nombre de configurations possible pour un bateau.")
    print(" -2- Nombre de configurations possible pour une liste de bateaux.")
    print(" -3- Ratio de validité lambda.")
    print("\nModélisation probabiliste du jeu")
    print(" -4- Nombre moyen de coups pour couler la flotte (version aléatoire).")
    print(" -5- Nombre moyen de coups pour couler la flotte (version heuristique).")
    print(" -6- Nombre moyen de coups pour couler la flotte (version probabiliste simple).")
    print("\nSenseur imparfait")
    print(" -7- Nombre moyen de recherche pour détecter l'objet égaré.")
    print(" \n-8- Quitter le programme.")

    while True:
        i = input("Merci de saisir le numéro de l'option que vous souhaitez exécuter : ")
        
        while True:
            try:
                i = int(i)
                break
            except ValueError:
                print("Votre entrée est invalide.")
                i = input("Merci de saisir le numéro de l'option que vous souhaitez exécuter : ")

        if i == 1:
            option_1()
        elif i == 2:
            option_2()
        elif i == 3:
            option_3()
        elif i in [4, 5, 6]:
            option_4_5_6(i)
        elif i == 7:
            option_7()
        elif i == 8:
            sys.exit()
        else:
            print("Option invalide. Le programme va se fermer.")
            sys.exit()

if __name__ == "__main__":
    main()
