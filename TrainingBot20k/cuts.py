def secsToTimestamp(time):
    min = time // 60
    secs = time % 60
    return "{0}:{1}".format(int(min), int(secs))


musicLength = input("Entrer la durée de la chanson au format m:ss : ")
introLength = int(input("Entrer la durée de l'intro en secondes : "))
str_split = musicLength.split(":")
musicLengthInSecs = int(str_split[0])*60 + int(str_split[1])

breaks = []
for k in range(1, 6):
    breaks.append(secsToTimestamp(musicLengthInSecs/(2**k)+introLength))

# print(breaks)
breaks = breaks[::-1]
print(breaks)
