import psycopg2
import utils

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

print(utils.getIdChanson(cur, "Un monde parfait (Ilona Mitrecey)"))
print(utils.getIdChanson(cur, "Va y avoir du sport"))
