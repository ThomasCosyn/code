import util
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np


def updateQuery(c, titre):
    titre = titre.replace("'", "''")
    return "UPDATE public.\"Chanson\" SET \"clusterID\"= {} WHERE titre = '{}';".format(c, titre)


def clustering():

    print("Starting clustering function...")

    # Requête
    print("Querying data...")
    conn, cur = util.connexion()
    df = pd.read_sql_query('SELECT titre, public."NbPassagesMC"(titre,current_date), public."NbPassages50"(titre,current_date),	public."NbPassages40"(titre,current_date), public."NbPassages30"(titre,current_date), public."NbPassages20"(titre,current_date), public."NbPassages20k"(titre,current_date) FROM public."Chanson"', con=conn)

    # K-means pour n = 5
    print("K-means")
    kmeans = KMeans(n_clusters=5).fit(
        df[['NbPassagesMC', 'NbPassages50', 'NbPassages40', 'NbPassages30', 'NbPassages20', 'NbPassages20k']])
    centroids = kmeans.cluster_centers_
    print(centroids)
    df['cluster'] = kmeans.labels_

    # On met à jour les clusters dans la base
    print("Database update", end="\n")
    for row in df.iterrows():
        cur.execute(updateQuery(row[1]['cluster'], row[1]['titre']))
        conn.commit()


def prediction(dateSimule):

    print("Starting prediction for date : ", dateSimule)

    # Requête
    print("Querying data...")
    conn, cur = util.connexion()
    df = pd.read_sql_query('SELECT titre, artiste, "année",	nb_mots, "clusterID", (SELECT AVG(laps) FROM public."LapsMCDP"(titre,' + dateSimule + ')) AS MCDPmoy, (SELECT laps FROM public."LapsMCDP"(titre,' + dateSimule + ') LIMIT 1 ) AS MCDP, (SELECT AVG(laps) FROM public."LapsMCMCDP"(titre,' + dateSimule +
                           ')) AS MCMCDPmoy, (SELECT laps FROM public."LapsMCMCDP"(titre,' + dateSimule + ') LIMIT 1 ) AS MCMCDP, public."DeltaDate"(titre, ' + dateSimule + ',(' + dateSimule + '::date - INTERVAL\'30 day\')::date), public."DeltaDateMC"(titre, ' + dateSimule + ',(' + dateSimule + '::date - INTERVAL\'30 day\')::date) FROM public."MêmesChansons"', con=conn)

    # Calcul des coefs
    print("Coef calculation...")
    bins = [13, 13, 13, 13, 13]
    histoMCDPmoy = util.histo(df, bins, 'mcdpmoy')
    valeursHistoMCDPmoy = [util.getHistoValues(h) for h in histoMCDPmoy]
    histoMCDP = util.histo(df, bins, 'mcdp')
    valeursHistoMCDP = [util.getHistoValues(h) for h in histoMCDP]
    histoMCMCDPmoy = util.histo(df, bins, 'mcmcdpmoy')
    valeursHistoMCMCDPmoy = [util.getHistoValues(h) for h in histoMCMCDPmoy]
    histoMCMCDP = util.histo(df, bins, 'mcmcdp')
    valeursHistoMCMCDP = [util.getHistoValues(h) for h in histoMCMCDP]

    # Calcul des scores à partir des coefs
    print("Score calculation...")
    df = util.scoreHisto(df, valeursHistoMCDPmoy, 'DeltaDate', 'f')
    df = util.scoreHisto(df, valeursHistoMCDP, 'DeltaDate', 'g')
    df = util.scoreHisto(df, valeursHistoMCMCDPmoy, 'DeltaDateMC', 'h')
    df = util.scoreHisto(df, valeursHistoMCMCDP, 'DeltaDateMC', 'i')
    df['score'] = df['f']*df['g']*df['h']*df['i']*10000

    # Ecriture dans le fichier de sortie
    print("Writing the output to csv file...")
    df = df.sort_values(by='score', ascending=False)
    df.to_csv('ML/test.csv', sep=";", encoding='utf8')


clustering()
input("Please change the definition of Mêmes Chansons in PostgreSQL")
prediction("'2022-05-07'")
print("Pipeline has successfully run !")
