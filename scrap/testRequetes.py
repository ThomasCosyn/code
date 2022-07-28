import psycopg2
import utils

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

print(utils.getIdChanson(cur, "Laisse-moi vivre ma vie"))
print(utils.getIdChanson(cur, "Jusqu''au bout (Amel Bent et Imen Es)"))
