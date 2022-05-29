import random as rd

max = 443
nbBornes = max//100 + 1
bornes = [100*(i+1) for i in range(nbBornes)]
bornes[-1] = max


def s(n):
    s = 0
    for i in range(n):
        s += 1/(2**(i+1))
    return s


probas = [s(i+1) for i in range(nbBornes)]

tirage = rd.random()

ok = False
for i, p in enumerate(probas):
    if tirage < p and not ok:
        ok = True
        if i == len(probas)-1:
            print(rd.randint(i*100+1, max))
        else:
            print(rd.randint(i*100+1, (i+1)*100))

if not ok:
    print(rd.randint((max//100)*100+1, max))
