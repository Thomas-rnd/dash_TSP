import time

import numpy as np
import pandas as pd

from src.distance import distance_trajet


def plus_proche_voisin(data, matrice_distance):
    """Retourne le trajet trouvé en se déplacement de proche en proche.
    La ville de départ étant arbitraire on choisit la ville d'index 0

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir
    matrice_distance : list
        matrice stockant l'integralité des distances inter villes

    Returns
    -------
    chemin_explores : list
        L'ensemble des sous chemins empruntés pour arriver au résulat
    temps_calcul : int
        temps necessaire à la résolution du problème
    """
    start_time = time.time()

    # Stockage de la progression de l'exploration
    chemin_explore = []
    itineraire = [0]
    while len(data.loc['x']) != len(itineraire):
        # A chaque itération on cherche la ville la plus proche de la ville actuelle
        # la ville actuelle étant la dernière de l'itinéraire

        # Liste trié dans l'ordre croissant des distances entre la ville actuelle et le reste
        distances = sorted(matrice_distance[itineraire[-1]])

        # On enlève la distance qui correspond à rester sur la même ville
        distances.remove(0)

        i = 0
        # On recherche la ville la plus proche encore inexplorée
        while matrice_distance[itineraire[-1]].index(distances[i]) in itineraire:
            i += 1
        itineraire.append(
            matrice_distance[itineraire[-1]].index(distances[i]))
        chemin_explore.append(itineraire)
    # On fait attention à fermer le cycle
    itineraire.append(itineraire[0])

    temps_calcul = time.time() - start_time
    return chemin_explore, temps_calcul


def main(data, matrice_distance, chemin_optimal=[]):
    """Lancement de l'algorithme de recherche 

    Parameters
    ----------
    matrice_distance : list
        matrice stockant l'integralité des distances inter villes
    chemin_initial : list
        suite de villes donnant le chemin parcouru. Ce chemin initial influ énormément 
        sur la solution finale trouvée.
    chemin_optimal : list
        résulat optimal donné par la TSPLIB

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """

    if chemin_optimal != []:
        distance_chemin_optimal = distance_trajet(
            chemin_optimal, matrice_distance)

    # On récupère les chemins testés et le temps de résolution de l'algorithme
    chemin_explores, temps_calcul = plus_proche_voisin(data, matrice_distance)

    # Calcul de la distance du trajet final trouvé par l'algorithme. En dernière position
    # de la variable précédente
    distance_chemin_sub_optimal = distance_trajet(
        chemin_explores[-1], matrice_distance)
    # Calcul de l'erreur si un chemin optimal est renseigné
    if chemin_optimal != []:
        erreur = 100*(distance_chemin_sub_optimal -
                      distance_chemin_optimal)/distance_chemin_optimal
    else:
        erreur = None

    # Chemin final trouvé
    solution = chemin_explores[-1]

    # Création du dataframe à retourner
    df_resultat_test = pd.DataFrame({
        'Nombre de villes': len(solution),
        # Dans un tableau pour être sur une seule ligne du dataframe
        'Solution': [solution],
        # Erreur par rapport à la solution optimal de la TSPLIB
        'Erreur (en %)': erreur,
        'Temps de calcul (en s)': temps_calcul
    })

    return df_resultat_test
