import util
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np
import os

conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

dates = ["2021-02-08", "2021-02-09", "2021-02-10", "2021-02-11", "2021-02-12",
         "2021-02-15", "2021-02-16", "2021-02-17", "2021-02-18", "2021-02-19", "2021-02-20", "2021-02-22", "2021-02-23", "2021-02-24", "2021-02-25", "2021-02-26"]

for date in dates:

    # Message de début du process
    print("Requête pour la date {0}".format(date))

    # On fait la requête de génération du dataset
    df = pd.read_sql_query(
        "SELECT * FROM public.\"GenereDatasetClassif\"('{0}', ('{0}'::date - INTERVAL'30 day')::date) WHERE \"année\" <= {1}".format(date, date[0:4]), con=conn)

    # On écrit
    mode = "w"
    header = True
    if os.path.exists('classificationDataset.csv'):
        mode, header = "a", False
    df.to_csv('classificationDataset.csv', sep=";",
              encoding='utf8', mode=mode, header=header)

    # Message de fin du process
    print("Fin du process pour la date {0}".format(date))
