def secsToTimestamp(time):
    min = time // 60
    secs = time % 60
    return "{0}:{1}".format(int(min), int(secs))


def timestampToSecs(timestamp):
    str_split = timestamp.split(":")
    secs = int(str_split[0])*60 + int(str_split[1])
    return secs


def getBreaksInSecs(musicLength, introLength):

    # On transforme la durée de la musique en secondes
    str_split = musicLength.split(":")
    musicLengthInSecs = int(str_split[0])*60 + int(str_split[1])

    # On calcule les breaks
    breaksInSecs = [int(musicLengthInSecs/(2**k) + introLength)
                    for k in range(1, 6)]
    breaksInSecs.append(0)
    breaksInSecs = breaksInSecs[::-1]

    return breaksInSecs


def test():
    musicLength = input("Entrer la durée de la chanson au format m:ss : ")
    introLength = int(input("Entrer la durée de l'intro en secondes : "))
    str_split = musicLength.split(":")
    musicLengthInSecs = int(str_split[0])*60 + int(str_split[1])

    breaks = []
    breaksInSecs = []
    for k in range(1, 6):
        breaks.append(secsToTimestamp(musicLengthInSecs/(2**k) + introLength))
        breaksInSecs.append(int(musicLengthInSecs/(2**k) + introLength))

    # print(breaks)
    breaks = breaks[::-1]
    breaksInSecs = breaksInSecs[::-1]
    print(breaks)
    print(breaksInSecs)
