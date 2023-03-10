import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from src.testData import trajet_en_df


def representation_itineraire_back(data, reseau_neurones=[]):
    """Affichage des N villes par des points ainsi que le parcours réalisé
       Le parcours est donné par l'ordre des villes dans le dataframe

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir
    reseau_neurones : list
        list stockant un réseau de neurone de kohonen
    """
    # Affichage des points
    plt.scatter(data.iloc[0, :], data.iloc[1, :], zorder=1)
    # Repérage du point initial par un cercle rouge
    plt.scatter(data.iloc[0, 0], data.iloc[1, 0], zorder=1,
                color="red", marker='o', label='Point de Départ')
    plt.legend(loc="upper right")

    if (reseau_neurones == []):
        # Affichage des traits
        plt.plot(data.iloc[0, :], data.iloc[1, :], zorder=1)
        plt.title('Chemin parcouru par le marchand', loc='center')
        # Pour une visualisation plus proche de la réalité
        # plt.axis("equal")
    else:
        x = [neurone[0] for neurone in reseau_neurones]
        y = [neurone[1] for neurone in reseau_neurones]
        # Affichage des neurones
        plt.scatter(x, y, zorder=1,
                    color="green", marker='x', label='Réseau de Kohonen')
        # Affichage des traits
        plt.plot(x, y, zorder=1)
        plt.title('Chemin parcouru par le réseau', loc='center')
    plt.show()


def representation_itineraire_web(data):
    """Affichage des N villes par des points ainsi que le parcours réalisé
       Le parcours est donné par l'ordre des villes dans le dataframe

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des informations sur un algorithme

    Returns
    -------
    fig
        Graphique de visualisation plolty
    """
    fig = px.line(data, x='x', y='y', markers=True,
                  title="Graphique représentant le chemin emprunté par le marchand")
    return fig


def representation_temps_calcul(data):
    """Affichage du temps de calcul d'un algorithme en fonction
    du nombre de ville qu'il a traité

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des informations sur un algorithme

    Returns
    -------
    fig
        Graphique de visualisation plolty
    """
    fig = px.line(data, x='Nombre de villes',
                  y='Temps de calcul (en s)', markers=True, title="Graphique des temps de calcul en fonction du nombre de villes évaluées")
    return fig


def affichage(df_resolution, data):
    """Affichage d'un trajet et des performances d'un algorithme

    Parameters
    ----------
    df_resolution : Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme sur un dataset
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir

    Returns
    -------
    fig
        Graphique de visualisation plolty
    """
    df_meilleur_trajet = trajet_en_df(
        df_resolution.loc[0, 'Solution'], data)
    # representation_itineraire_back(df_meilleur_trajet)
    fig = representation_itineraire_web(df_meilleur_trajet)

    # print("=============================================")
    # print("Nombre de ville : ", df_resolution.loc[0, "Nombre de villes"])
    # print("Pourcentage d'erreur : ", df_resolution.loc[0, "Erreur (en %)"])
    # print("Temps de calcul (en s): ",
    #      df_resolution.loc[0, "Temps de calcul (en s)"])
    # print("=============================================")

    return fig
