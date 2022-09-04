# Ce fichier doit prendre un entrée un fichier CSV contenant les chansons qui sont tombées
# mon passage à l'emission, puis mettre à jour dans la base de donnée la colonne "tombee"
# de la table "Chanson". La valeur doit donc être true pour les chansons qui sont tombées.

# Lecture du fichier à déposer dans majJourJ
import os
import csv
chansons = []
with open('ML/MAJ jour J/majJourJ.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=";")
    for row in spamreader:
        chansons.append(row[0])

print(chansons)

# MAJ de la colonne en base
homePath = "C:/Users/thoma/OneDrive - CentraleSupelec/NOPLP/code/ML"
os.chdir(homePath)
import shutil
shutil.copy(homePath + "/util.py", homePath + "/MAJ jour J/")
import util
conn, cursor = util.connexion()
for c in chansons:
    cursor.execute("UPDATE public.\"Chanson\" SET tombee = true WHERE titre = \'{}\'".format(c.replace("'", "''")))
conn.commit()
