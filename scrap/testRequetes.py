import psycopg2
import utils

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

print(utils.getIdChanson(cur, "La parisienne"))
print(utils.getIdChanson(cur, "Marie-Jeanne"))
