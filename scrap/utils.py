import selenium.common.exceptions

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

    if chanson == "La Parisienne":
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

    if chanson == "L''aventurier":
        rep = input(
            "Indochine ou Jacques Dutronc ? ")
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
