import numpy as np
import psycopg2
import pandas as pd

# Fonction fabriquant un histogramme à partir d'un dataframe
# Prend en argument le dataframe et le nombre de classes


def histo(df, nbBins, type):
    tuples = []
    for j, bin in enumerate(nbBins):
        cluster = df[df['clusterID'] == j][type]
        n = cluster.count()
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
        tuples.append((classes, hauteurs/n))
    return tuples


# Fonction récupérant les hauteurs et les classes d'un histogramme
def getHistoValues(histo):
    return {'classes': histo[0], 'hauteurs': histo[1]}


# Fonction renvoyant les scores pour un histogramme à partir des laps actuels
def scoreHisto(df, valeursHisto, colonne, fonction):

    # Initialisation du score et nettoyage des dates
    df[fonction] = np.nan
    df[colonne] = df[colonne].fillna(1000)

    # On itère sur chaque cluster
    for c in range(5):
        # Récupération des valeurs de l'histogramme
        vH = pd.DataFrame(valeursHisto[c])
        # On ne garde que les chansons appartenant au cluster courant et on les ordonne par date
        toJoin = df[df['clusterID'] == c].sort_values(by=colonne)
        # On fait la jointure approximative
        toJoin = pd.merge_asof(toJoin, vH, left_on=colonne,
                               right_on='classes', direction='backward')
        toJoin[fonction] = toJoin['hauteurs']
        toJoin = toJoin.drop(columns=['classes', 'hauteurs'])
        # On met à jour df
        df = pd.concat([df[df['clusterID'] != c], toJoin])
    df[fonction].fillna(0)

    return df


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
