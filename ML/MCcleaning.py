import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import csv

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

# On récupère toutes les mêmes chansons
cur.execute(
    "SELECT titre, artiste, \"année\", nbpassages FROM public.\"MêmesChansons\"	ORDER BY nbpassages DESC;")
memesChansons = cur.fetchall()
print(memesChansons)

memesChansonsDeltas = []
h1 = []
h2 = []
h3 = []
h4 = []


for mc in memesChansons:
    print()
    print(mc)
    mc = [mc[i] for i in range(len(mc))]
    if mc[3] > 1:
        mc[0] = mc[0].replace("'", "''")
        cur.execute("SELECT * FROM public.\"HistoriqueChansonMC\"('" +
                    str(mc[0]) + "') ORDER BY date DESC")
        derniersPassages = cur.fetchall()
        # print(derniersPassages)
        deltasDate = []
        deltasEmission = []
        for i, dp in enumerate(derniersPassages):
            if i < len(derniersPassages)-1:
                lastDeltaDates = (
                    derniersPassages[i][0] - derniersPassages[i+1][0]).days
                deltasDate.append(lastDeltaDates)
                lastDeltaEmission = derniersPassages[i][3] - \
                    derniersPassages[i+1][3]
                deltasEmission.append(lastDeltaEmission)

        deltaDateMoy = sum(deltasDate)/len(deltasDate)
        mc.append(float(deltaDateMoy))
        h1.append(float(deltaDateMoy))
        mc.append(int(deltasDate[0]))
        h2.append(int(deltasDate[0]))
        deltaEmissionMoy = sum(deltasEmission)/len(deltasEmission)
        mc.append(int(deltaEmissionMoy))
        h3.append(int(deltaEmissionMoy))
        mc.append(int(deltasEmission[0]))
        h4.append(int(deltasEmission[0]))
        memesChansonsDeltas.append(mc)
        print(mc)

    else:
        for _ in range(4):
            mc.append(None)
        memesChansonsDeltas.append(mc)
        print(mc)

'''
# Observations
plt.figure()

plt.subplot(2, 2, 1)
plt.title("Histogramme selons les deltaDateMoy")
plt.hist(h1, bins=30)

plt.subplot(2, 2, 2)
plt.title("Histogramme selons les lastDeltaDate")
plt.hist(h2, bins=30)

plt.subplot(2, 2, 3)
plt.title("Histogramme selons les deltaEmissionMoy")
plt.hist(h3, bins=30)

plt.subplot(2, 2, 4)
plt.title("Histogramme selons les lastDeltaEmission")
plt.hist(h4, bins=30)

plt.show()
'''

# Ecriture dans un fichier csv
with open('dataset.csv', 'w', newline='', encoding='utf-8') as file:
    rd = csv.writer(file, delimiter=';')
    rd.writerows(memesChansonsDeltas)
