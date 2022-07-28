import pandas as pd
import psycopg2
import util
import numpy as np
import csv

fonctions = {'f': ('mcdpmoy', 'DeltaDate'), 'g': (
    'mcdp', 'DeltaDate'), 'h': ('mcmcdpmoy', 'DeltaDateMC')}


def requetes(dateStr):
    return {'f': '(SELECT AVG(laps) FROM public."LapsMCDP"(titre,\'' + dateStr +
            '\')) AS MCDPmoy, public."DeltaDate"(titre, \'' + dateStr + '\',\'' + dateStr + '\') FROM public."MêmesChansons"', 'g': '(SELECT laps FROM public."LapsMCDP"(titre,\'' + dateStr + '\') LIMIT 1 ) AS MCDP, public."DeltaDate"(titre, \'' + dateStr + '\',\'' + dateStr + '\') FROM public."MêmesChansons"', 'h': '(SELECT AVG(laps) FROM public."LapsMCMCDP"(titre,\'' + dateStr + '\')) AS MCMCDPmoy, public."DeltaDateMC"(titre, \'' + dateStr + '\',\'' + dateStr + '\') FROM public."MêmesChansons"'}


def optimisation(binInit, binMax, fonction):

    # Connexion à la base de données locale
    conn = psycopg2.connect(host="localhost",
                            database="NOPLP",
                            user="postgres",
                            password="Objectifcentrale2019!")
    cur = conn.cursor()

    # On génère la plage de dates sur laquelle on veut travailler
    datesDF = pd.date_range(start='2021-01-01', end='2021-08-31')

    # On initialise le score à 100000
    dernier = 1000000
    score = 1000

    # Tant que le score calculé est meilleur que le précédent on réitère l'algorithme
    for bins in range(binInit, binMax+1):

        scores = []

        # On parcourt les dates considérées
        for date in datesDF:

            dateStr = date.strftime('%Y-%m-%d')
            print("La date du jour est : " + dateStr)
            # On récupère les données dans le contexte du jour en cours
            df = pd.read_sql_query(
                'SELECT titre, artiste, "année", nbpassages, ' + requetes(dateStr)[fonction], con=conn)

            # Calcul des coefs de l'histogramme pour l'hyperparamètre bins
            histo = util.histo(df[fonctions[fonction][0]], bins)
            valeursHisto = util.getHistoValues(histo)

            # Calcul des valeurs de f pour chaque chanson
            df = util.scoreHisto(
                df, valeursHisto, fonctions[fonction][1], fonction)

            # On trie le dataframe
            df = df.sort_values(by=fonction, ascending=False)
            df.reset_index(drop=True, inplace=True)

            # On récupère les mêmes chansons tombées à la date considérée
            cur.execute(
                "SELECT titre FROM public.\"DernieresMC\" WHERE date = '{0}';".format(dateStr))
            # Puis on regarde quel était leur rang
            for row in cur:
                mc = row[0]
                try:
                    rang = np.where(df['titre'] == mc)[0][0]
                    print(rang)
                    scores.append(rang)
                # Cas où la chanson n'est jamais tombé (Ca fait mal)
                except IndexError:
                    scores.append(356)

        scores = np.array(scores)
        # Résumé de ce cas
        print("Pour {0} barres d'histogrammes".format(bins))
        print("La moyenne est de : {0}".format(scores.mean()))
        print("La médiane est de : {0}".format(np.median(scores)))
        print()

        # On écrit le résultat dans un fichier
        with open('resultats_{0}.csv'.format(fonction), mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([bins, scores.mean(), np.median(scores)])


optimisation(10, 30, 'f')
