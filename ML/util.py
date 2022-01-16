import numpy as np
import psycopg2
import pandas as pd

# Fonction fabriquant un histogramme à partir d'un dataframe
# Prend en argument le dataframe et le nombre de classes


def histo(df, nbBins, type):
    tuples = []
    for j, bin in enumerate(nbBins):
        cluster = df[df['clusterID'] == j][type]
        # Nombre de classes
        k = bin
        minimum = cluster.min()
        maximum = cluster.max()
        largeur = (maximum-minimum)/k
        classes = [minimum + i*largeur for i in range(0, k+1)]
        hauteurs = [0]*(k+1)
        for elem in cluster:
            i = 1
            while elem > (minimum + largeur*i):
                i += 1
            hauteurs[i-1] += 1
        tuples.append((classes, hauteurs))
    return tuples


# Fonction récupérant les hauteurs et les classes d'un histogramme
def getHistoValues(histo):
    return {'classes': histo[0], 'hauteurs': histo[1]}


# Fonction renvoyant les scores pour un histogramme à partir des laps actuels
def scoreHisto(df, valeursHisto, colonne, fonction):

    df[fonction] = np.nan
    for c in range(5):

        vH = pd.DataFrame(valeursHisto[c])
        pd.merge


# def scoreHisto(df, valeursHisto, colonne, fonction):

    # df[fonction] = np.nan

    # for c in range(5):

    #     cluster = df[df['clusterID'] == c]

    #     taille = cluster.shape[0]
    #     nb_classes = len(valeursHisto[c]['classes'])
    #     taille_ech = sum(valeursHisto[c]['hauteurs'])

    #     for i in range(taille):
    #         classe = 0
    #         while df[colonne][i] > valeursHisto['classes'][classe] and classe < nb_classes-1:
    #             classe += 1
    #         df[fonction][i] = valeursHisto[c]['hauteurs'][classe-1]/taille_ech

    # return df

# Fonction se connectant à la base locale


def connexion():
    conn = psycopg2.connect(host="localhost",
                            database="NOPLP",
                            user="postgres",
                            password="Objectifcentrale2019!")
    return (conn, conn.cursor())
