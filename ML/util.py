import numpy as np
import psycopg2

# Fonction fabriquant un histogramme à partir d'un dataframe
# Prend en argument le dataframe et le nombre de classes


def histo(df, nbBins):
    n = df.shape[0]
    # Nombre de classes
    k = nbBins
    minimum = df.min()
    maximum = df.max()
    largeur = (maximum-minimum)/k
    classes = [minimum + i*largeur for i in range(0, k+1)]
    hauteurs = [0]*k
    for elem in df:
        i = 1
        while elem > (minimum + largeur*i):
            i += 1
        hauteurs[i-1] += 1
    return (classes, hauteurs)


# Fonction récupérant les hauteurs et les classes d'un histogramme
def getHistoValues(histo):
    return {'classes': histo[0], 'hauteurs': histo[1]}


# Fonction renvoyant les scores pour un histogramme à partir des laps actuels
def scoreHisto(df, valeursHisto, colonne, fonction):
    taille = df.shape[0]
    nb_classes = len(valeursHisto['classes'])
    taille_ech = sum(valeursHisto['hauteurs'])
    df[fonction] = np.nan

    for i in range(taille):
        classe = 0
        while df[colonne][i] > valeursHisto['classes'][classe] and classe < nb_classes-1:
            classe += 1
        df[fonction][i] = valeursHisto['hauteurs'][classe-1]/taille_ech

    return df

# Fonction se connectant à la base locale


def connexion():
    conn = psycopg2.connect(host="localhost",
                            database="NOPLP",
                            user="postgres",
                            password="Objectifcentrale2019!")
    return (conn, conn.cursor())
