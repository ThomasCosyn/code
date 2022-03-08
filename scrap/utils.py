import selenium.common.exceptions
import psycopg2
import re

conversionMois = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
                  7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
mois = {"décembre": 12, "janvier": 1,
        "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11}
categories = {1: '50', 2: '40', 3: '30', 4: '20', 5: '10', 6: 'MC', 7: '20k'}

# Fonction qui renvoie, pour un thème, la chanson choisie puis la chanson non-choisie


def getChoisieNonChoisie(u, j, browser):

    em1chanson50c = ''
    em1chanson50nc = ''

    # Cas général
    try:
        em1chanson50c = browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/b[2]/a').text
        notBold = em1chanson50nc = browser.find_elements_by_xpath(
            '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
        em1chanson50nc = getNC(notBold)
    except selenium.common.exceptions.NoSuchElementException:

        # Cas Dumbo / Cendrillon 17 décembre 2019
        try:
            em1chanson50c = browser.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/b[2]/a').text
            notBold = em1chanson50nc = browser.find_elements_by_xpath(
                '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
            em1chanson50nc = getNC(notBold)

        except selenium.common.exceptions.NoSuchElementException:

            # Cas Ce matin / La tribu de Dana 18 décembre 2019
            try:
                em1chanson50c = browser.find_element_by_xpath(
                    '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a[2]/b').text
                notBold = browser.find_elements_by_xpath(
                    '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
                em1chanson50nc = getNC(notBold)

            except selenium.common.exceptions.NoSuchElementException:

                # Cas Le Loir-et-Cher / Wight is wight 19 décembre 2019
                try:
                    em1chanson50c = browser.find_element_by_xpath(
                        '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a[1]/b').text
                    notBold = browser.find_elements_by_xpath(
                        '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a[2]')
                    em1chanson50nc = getNC(notBold)
                except selenium.common.exceptions.NoSuchElementException:

                    # Cas No me mires mas / Besoin de rien envie de toi 26 décembre 2019
                    try:
                        em1chanson50c = browser.find_element_by_xpath(
                            '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a[2]/b').text
                        notBold = browser.find_elements_by_xpath(
                            '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
                        em1chanson50nc = getNC(notBold)
                    except selenium.common.exceptions.NoSuchElementException:

                        # Cas Colore / L'autre finistère 27 décembre 2019
                        try:
                            em1chanson50c = browser.find_element_by_xpath(
                                '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/b[1]/a').text
                            notBold = browser.find_elements_by_xpath(
                                '//*[@id = "mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
                            em1chanson50nc = getNC(notBold)
                        except selenium.common.exceptions.NoSuchElementException:
                            pass

    if (em1chanson50c, em1chanson50nc) == ('', ''):
        # Cas La fête / Ta fête 2 juin 2020
        try:
            chansons = browser.find_elements_by_xpath(
                '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']/a')
            print(chansons)
            (em1chanson50c, em1chanson50nc) = (
                chansons[0].text, chansons[1].text)
        except selenium.common.exceptions.NoSuchElementException:
            pass
        except IndexError:
            print("GROS PROBLEME SUR LE SITE")
            em1chanson50c = input(
                "Entrer la chanson choisie : ")
            em1chanson50nc = input(
                "Entrer la chanson non-choisie : ")

    return (em1chanson50c, em1chanson50nc)


# Fonction qui pour une chanson donnée, renvoie son id dans la table Chanson
def getIdChanson(cur, chanson):

    # On teste les cas chiants
    if chanson == "On écrit sur les murs":
        rep = input("Kids United ou Demis Roussos ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Elle me dit":
        rep = input("Mika ou Ben l''Oncle Soul ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "On ira":
        rep = input("Jean-Jacques Goldman ou Zaz ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Adieu":
        rep = input("Cœur de Pirate ou Slimane ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "La fête":
        rep = input("Michel Fugain et le Big Bazar ou Amir ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Les mots":
        rep = input("Keen''V ou Mylène Farmer ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Liberté":
        rep = input("Les Enfoirés ou Gilbert Montagné ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Sur la route":
        rep = input("De Palmas ou Raphaël & Jean-Louis Aubert ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Parle-moi":
        rep = input("Nâdiya ou Isabelle Boulay ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Je m''en vais":
        rep = input("Cali ou Vianney ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Hélène":
        rep = input("Julien Clerc ou Roch Voisine ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ta main":
        rep = input("Claudio Capéo ou Grégoire ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Tu vas me manquer":
        rep = input("Maître Gims ou P. Obispo ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Avant toi":
        rep = input("Vitaa & Slimane ou Calogero ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ça va ça vient":
        rep = input("Vitaa & Slimane ou Liane Foly ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Mon frère":
        rep = input("Les dix commandements ou Maxime Leforestier ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ma vie":
        rep = input("Dadju ou Alain Barrière ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Je vole":
        rep = input("Louane ou Michel Sardou ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Mon pays":
        rep = input("Faudel ou Christophe Maé ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Tout le monde":
        rep = input("Emmanuel Moire ou Zazie ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Demain":
        rep = input("Thomas Dutronc ou BigFlo et Oli ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ma sœur":
        rep = input("Clara Luciani ou Vitaa ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson in ["La Parisienne", "La parisienne"]:
        rep = input("Christophe Maé ou Marie-Paule Belle ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Lucie":
        rep = input("Pascal Obispo ou Daniel Balavoine ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ça ira":
        rep = input("Joyce Jonathan ou Vitaa & Slimane ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Avant de partir":
        rep = input("Roch Voisine ou Eve Angeli ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Je t''attends":
        rep = input("Axelle Red ou Johnny Hallyday ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Ensemble":
        rep = input(
            "Cœur de Pirate, Jean-Jacques Goldman, Les Frangines ou Sinclair ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Le temps":
        rep = input(
            "Charles Aznavour ou Tayc ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Dernière danse":
        rep = input(
            "Kyo ou Indila ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "L''aventurier":
        rep = input(
            "Indochine ou Jacques Dutronc ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson == "Un monde parfait":
        rep = input(
            "Ilona ou Les Innocents ? ")
        chanson = chanson + " (" + rep + ")"

    if chanson in ["Vous les copains", "Vous les copains (je ne vous oublierai jamais)"]:
        chanson = "Vous les copains (je ne vous oublierai jamais)"

    if chanson in ["Le brio", "Le Brio (Branchez la guitare)"]:
        chanson = "Le Brio (Branchez la guitare)"

    if chanson in ["Les yeux revolver", "Elle a les yeux revolver"]:
        chanson = "Elle a les yeux revolver"

    if chanson in ["Les petits papiers", "Les p'tits papiers"]:
        chanson = "Les p''tits papiers"

    if chanson in ['Maldón', 'Maldonne']:
        chanson = 'Maldonne'

    if chanson in ['La bicyclette', 'À bicyclette', 'A bicyclette']:
        chanson = 'La bicyclette'

    if chanson in ['Sympathique (Je ne veux pas travailler)', 'Sympathique', "Sympathique (je ne veux pas travailler)"]:
        chanson = 'Sympathique'

    if chanson in ["Demain (Big Flo et Oli & P'tit Biscuit)", 'Demain (BigFlo et Oli)', "Demain (Big Flo et Oli & P''tit Biscuit)"]:
        chanson = 'Demain (BigFlo et Oli)'

    if chanson in ["Big bisous", 'Big bisou']:
        chanson = 'Big bisous'

    if chanson in ["Help Myself", 'Help myself (Nous ne faisons que passer)']:
        chanson = 'Help Myself'

    if chanson in ["Bernard''s song (Il n''est de nulle part)", "Bernard''s song"]:
        chanson = "Bernard''s song"

    if chanson in ["Amor tambien (Tout l''monde chante)", "Amor tambien"]:
        chanson = "Amor tambien"

    if chanson in ["Le café des délices", "Au café des délices"]:
        chanson = "Au café des délices"

    if chanson in ["Le gorille", "Le gorille (Gare au gorille)"]:
        chanson = "Le gorille"

    if chanson in ["Le pétnitencier", "Le pénitencier"]:
        chanson = "Le pénitencier"

    if chanson in ["Long is the road (Américain)", "Long is the road"]:
        chanson = "Long is the road"

    if chanson in ["L''orange du marchand'", "L''orange"]:
        chanson = "L''orange du marchand"

    if chanson in ["Be bop a lula", "Be bop a lula 1960"]:
        chanson = "Be bop a lula 1960"

    if chanson in ["Les play-boys", "Les playboys"]:
        chanson = "Les playboys"

    if chanson in ["Sur la route (De Palmas)", "Sur la route (Gérald de Palmas)"]:
        chanson = "Sur la route (De Palmas)"

    if chanson in ["Prendre un enfant par la main", "Prendre un enfant"]:
        chanson = "Prendre un enfant par la main"

    if chanson in ["Le banana split", "Banana split"]:
        chanson = "Banana split"

    if chanson in ["La ballade de Jim", "Ballade de Jim"]:
        chanson = "La ballade de Jim"

    if chanson in ["Chanson des jumelles", "La chanson des jumelles"]:
        chanson = "La chanson des jumelles"

    if chanson in ["Félicie", "Félicie aussi"]:
        chanson = "Félicie"

    if chanson in ["Tu vas me manquer (Pascal Obispo)", "Tu vas me manquer (P. Obispo)"]:
        chanson = "Tu vas me manquer (P. Obispo)"

    if chanson in ["Mon truc en plume", "Mon truc en plumes"]:
        chanson = "Mon truc en plume"

    if chanson in ["Un monde parfait (Ilona)", "Un monde parfait (Ilona Mitrecey)"]:
        chanson = "Un monde parfait (Ilona)"

    cur.execute(
        "SELECT id FROM public.\"Chanson\" WHERE similarity(unaccent(titre), unaccent('" + chanson + "')) > 0.9;")

    for row in cur:
        return row[0]


# Création d'un nouveau passage dans la table Passage
def setNewPassage(cur, dateOk, categories, j, idEmission, idPassage, choisie):
    if choisie:
        cur.execute("INSERT INTO public.\"Passage\"(id, date, choisie, categorie, numero) VALUES ('" +
                    str(idPassage) + "','" + dateOk + "', true,'" + categories[j] + "', '" + str(idEmission) + "');")
    else:
        cur.execute("INSERT INTO public.\"Passage\"(id, date, choisie, categorie, numero) VALUES ('" +
                    str(idPassage) + "','" + dateOk + "', false,'" + categories[j] + "', '" + str(idEmission) + "');")


# Création d'une fonction qui gère la présence du lien 'Les années *0' que ces abrutis ont ajouté
def getNC(chaines):
    for chaine in chaines:
        chaineText = chaine.text
        if chaineText[:min(len(chaineText), 11)] != 'Les années ':
            em1chanson50nc = chaineText
    return em1chanson50nc


# Fonction se connectant à la base locale
def connexion():
    conn = psycopg2.connect(host="localhost",
                            database="NOPLP",
                            user="postgres",
                            password="Objectifcentrale2019!")
    return (conn, conn.cursor())

# Fonction retournant l'idPassage et l'idEmission de la base


def getSQLVariables(cur):
    cur.execute(
        "SELECT id, numero FROM public.\"Passage\" ORDER BY id DESC	LIMIT 1")
    for row in cur:
        idPassage = int(row[0]) + 1
        idEmission = int(row[1]) + 1
    print("idPassage initialisé à : " + str(idPassage))
    print("idEmission initialisé à : " + str(idEmission))
    return (idPassage, idEmission)

# Fonction retournant les dates des dernières émissions récupérés


def getLastDate(cur):
    cur.execute("SELECT date FROM public.\"Dernieres20k\" LIMIT 4")
    dates = []
    for row in cur:
        dates.append(row[0])
    for date in dates:
        if date != dates[0]:
            return "Erreur"
    return dates[0]

# Chanson définissant le chemin dynamique de l'URL


def chemin(date):
    annee = str(date.year)
    mois = conversionMois[date.month]
    return mois + "_" + annee

# Fonction récoltant les chansons pour un émission données


def emission(browser, u, cur, dateOk, idEmission, idPassage):

    chansons = []
    for j in range(1, 8):

        ligne = browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']').text

        if j <= 5 and 'non pris' not in ligne.lower():
            (c1, c2) = getChoisieNonChoisie(u, j, browser)
            chansons.append((c1, c2))
            print(chansons)
            c1 = c1.replace("'", "''")
            # Pour la chanson choisie
            setNewPassage(cur, dateOk, categories, j,
                          idEmission, idPassage, True)
            idChanson = getIdChanson(cur, c1)
            cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                        str(idChanson) + "', '" + str(idPassage) + "');")
            idPassage += 1
            # Pour la chanson non choisie
            c2 = c2.replace("'", "''")
            setNewPassage(cur, dateOk, categories,
                          j, idEmission, idPassage, False)
            idChanson = getIdChanson(cur, c2)
            cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                        str(idChanson) + "', '" + str(idPassage) + "');")
            idPassage += 1

        if j == 6:
            MC = ligne.split(' : ')[1].replace("'", "''")
            chansons.append(MC)
            print(chansons)
            setNewPassage(cur, dateOk, categories,
                          j, idEmission, idPassage, True)
            idChanson = getIdChanson(cur, MC)
            cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                        str(idChanson) + "', '" + str(idPassage) + "');")
            idPassage += 1

        if j == 7:
            (c1, c2) = getChoisieNonChoisie(u, j, browser)
            chansons.append((c1, c2))
            print(chansons)
            # Pour la chanson choisie
            c1 = c1.replace("'", "''")
            setNewPassage(cur, dateOk, categories,
                          j, idEmission, idPassage, True)
            idChanson = getIdChanson(cur, c1)
            cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                        str(idChanson) + "', '" + str(idPassage) + "');")
            idPassage += 1
            # Pour la chanson non choisie
            c2 = c2.replace("'", "''")
            setNewPassage(cur, dateOk, categories,
                          j, idEmission, idPassage, False)
            idChanson = getIdChanson(cur, c2)
            cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                        str(idChanson) + "', '" + str(idPassage) + "');")
            idPassage += 1
    print(chansons)
    return idPassage

# Fonction parcourant le calendrier et donnant la liste des jours pour lesquels il ne faut pas incrémenter le compteur u


def calendrier(browser):

    lignes = browser.find_elements_by_xpath(
        '/html/body/div[4]/div[3]/div[4]/main/div[3]/div/div/big[1]/table/tbody/tr')
    colonnes = browser.find_elements_by_xpath(
        '/html/body/div[4]/div[3]/div[4]/main/div[3]/div/div/big[1]/table/tbody/tr[2]/td')

    nbLignes, nbColonnes = len(lignes), len(colonnes)
    mauvaisJours = []
    speciales = []

    # On parcourt le calendrier
    for l in range(2, nbLignes + 1):
        for c in range(1, nbColonnes-1):

            try:
                # Récupération du jour et des couleurs de la case du calendrier
                case = browser.find_element_by_xpath(
                    '/html/body/div[4]/div[3]/div[4]/main/div[3]/div/div/big[1]/table/tbody/tr[{0}]/td[{1}]'.format(str(l), str(c)))
                rgb = case.value_of_css_property('background-color')
                couleurs = re.findall(r'[0-9]{1,3}', rgb)
                jour = case.text
                speciale = re.findall(r'[0-9]{1,2} - [A-Za-z]{1,}', jour)

                # Si c'est une émission annulée on récupère le jour auquel c'est arrivé
                if couleurs != ['57', '255', '20', '1'] and jour != '':
                    mauvaisJours.append(jour)

                # Si c'est une émission spéciale, on récupère également le jour
                elif len(speciale) > 0:
                    jour = re.findall(r'[0-9]{1,2}', speciale[0])[0]
                    speciales.append(jour)

            except selenium.common.exceptions.NoSuchElementException:
                pass

    return mauvaisJours, speciales
