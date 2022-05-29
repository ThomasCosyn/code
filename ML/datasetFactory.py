import util
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np

conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

dates = ["2021-01-01"]

for date in dates:

    # Message de début du process
    print("Requête pour la date {0}".format(date))

    # On fait la requête de génération du dataset
    df = pd.read_sql_query(
        "SELECT * FROM public.\"GenereDatasetClassif\"('{0}', ('{0}'::date - INTERVAL'30 day')::date) WHERE \"année\" <= {1}".format(date, date[0:4]), con=conn)

    # On écrit
    df.to_csv('classificationDataset.csv', sep=";",
              encoding='utf8', mode="a", header=False)

    # Message de fin du process
    print("Fin du process pour la date {0}".format(date))
