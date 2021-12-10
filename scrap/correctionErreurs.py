import psycopg2

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cur = conn.cursor()

chansonDoute = input("Entrer la chanson sur laquelle vous avez un doute : ")

cur.execute(
    "SELECT * FROM public.\"HistoriqueChanson\"('" + str(chansonDoute) + "')")

# Lecture des passages de la chanson sur laquelle on a un doute
passages = []
for row in cur:
    passages.append(row)

for p in passages:
    print(p)
    passageId = p[-1]
    erreur = input("Y a-t-il une erreur ? [o] pour oui [n] pour non : ")
    if erreur == "o":
        chansonRemplacante = input(
            "Entrer la chanson qui est effectivement passée : ")
        cur.execute("SELECT * FROM public.\"Chanson\" WHERE titre = '" +
                    str(chansonRemplacante) + "'")
        idChansonRemplacante = cur.fetchone()[0]
        cur.execute("UPDATE public.\"Chanson_Passage\" SET \"Chanson_id\" = " +
                    str(idChansonRemplacante) + " WHERE \"Passage_id\" = " + str(passageId))

    conn.commit()
