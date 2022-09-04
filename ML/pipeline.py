import util
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np
from catboost import CatBoostClassifier, Pool
import shutil


def updateQuery(c, titre):
    titre = titre.replace("'", "''")
    return "UPDATE public.\"Chanson\" SET \"clusterID\"= {} WHERE titre = '{}';".format(c, titre)


def clustering(n):

    print("Starting clustering function...")

    # Requête
    print("Querying data...")
    conn, cur = util.connexion()
    df = pd.read_sql_query('SELECT titre, public."NbPassagesMC"(titre,current_date), public."NbPassages50"(titre,current_date),	public."NbPassages40"(titre,current_date), public."NbPassages30"(titre,current_date), public."NbPassages20"(titre,current_date), public."NbPassages20k"(titre,current_date) FROM public."Chanson"', con=conn)

    # K-means pour le nombre de clusters entré en paramètre
    print("K-means")
    kmeans = KMeans(n_clusters=n).fit(
        df[['NbPassagesMC', 'NbPassages50', 'NbPassages40', 'NbPassages30', 'NbPassages20', 'NbPassages20k']])
    centroids = kmeans.cluster_centers_
    print(centroids)

    # On réordonne les clusters par croissance du nombre de passage moyen en MC
    dico = {}
    centro = centroids[:, 0].argsort()
    for i in range(0, 10):
        dico[centro[i]] = i

    print(dico)
    df['cluster'] = kmeans.labels_
    df['cluster'] = df['cluster'].map(dico)

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


def predictionCatboost(dateSimule):

    print("Starting prediction for date : ", dateSimule)

    # Requête
    print("Querying data...")
    conn, cur = util.connexion()
    df = pd.read_sql_query(
        "SELECT * FROM public.\"GenereDatasetClassif\"('{0}', ('{0}'::date - INTERVAL'30 day')::date) WHERE \"année\" <= {1}".format(dateSimule, dateSimule[0:4]), con=conn)

    # Data processing
    print("Processing data...")
    df = df[df["tombee"] != True]
    df = df.drop(columns=['id', 'Chanson_id', 'tombee'])
    reversed_cat = {'50': 1, '40': 2, '30': 3,
                    '20': 4, '10': 5, 'MC': 6, '20k': 7, None: 8}
    df = df.replace({'categorie': reversed_cat})
    test_labels = df['categorie']
    test_data = df.drop(columns=['categorie'])
    test_pool = Pool(test_data,
                     test_labels,
                     cat_features=['titre', 'artiste', 'clusterid'])

    # Chargement du modèle
    print("Model loading...")
    from_file = CatBoostClassifier()
    model = from_file.load_model("ML/catboostModel.cbm", format="cbm")

    # Prédiction
    print("Predicting probabilities...")
    test_data["pred"] = model.predict(test_pool)
    preds_proba = model.predict_proba(test_pool)
    test_data["proba50"] = preds_proba[:, 0]
    test_data["proba40"] = preds_proba[:, 1]
    test_data["proba30"] = preds_proba[:, 2]
    test_data["proba20"] = preds_proba[:, 3]
    test_data["proba10"] = preds_proba[:, 4]
    test_data["probaMC"] = preds_proba[:, 5]
    test_data["proba20k"] = preds_proba[:, 6]
    test_data["probaPP"] = preds_proba[:, 7]

    # Ecriture dans le fichier de sortie
    print("Writing the output to csv file...")
    test_data.to_csv('ML/predCatboost.csv', sep=";", encoding='utf8')
    shutil.copyfile("ML/predCatboost.csv",
                    "archive/{0}.csv".format(dateSimule))


# clustering(10)
# input("Please change the definition of Mêmes Chansons in PostgreSQL")
predictionCatboost("2022-09-05")
#print("Pipeline has successfully run !")
