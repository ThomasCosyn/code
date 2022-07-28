import numpy as np
import psycopg2
import pandas as pd
from catboost import CatBoostClassifier
import sklearn.metrics as skl


# Fonction fabriquant un histogramme à partir d'un dataframe
# Prend en argument le dataframe et le nombre de classes


def histo(df, nbBins, type):
    tuples = []
    for j, bin in enumerate(nbBins):
        cluster = df[df['clusterID'] == j][type]
        n = cluster.count()
        # Nombre de classes
        k = bin
        minimum = cluster.min()
        maximum = cluster.max()
        largeur = (maximum-minimum)/k
        classes = [minimum + i*largeur for i in range(0, k+1)]
        hauteurs = [0]*(k+1)
        for elem in cluster:
            i = 1
            while elem > (minimum + largeur*i):
                i += 1
            hauteurs[i-1] += 1
        tuples.append((classes, hauteurs/n))
    return tuples


# Fonction récupérant les hauteurs et les classes d'un histogramme
def getHistoValues(histo):
    return {'classes': histo[0], 'hauteurs': histo[1]}


# Fonction renvoyant les scores pour un histogramme à partir des laps actuels
def scoreHisto(df, valeursHisto, colonne, fonction):

    # Initialisation du score et nettoyage des dates
    df[fonction] = np.nan
    df[colonne] = df[colonne].fillna(1000)

    # On itère sur chaque cluster
    for c in range(5):
        # Récupération des valeurs de l'histogramme
        vH = pd.DataFrame(valeursHisto[c])
        # On ne garde que les chansons appartenant au cluster courant et on les ordonne par date
        toJoin = df[df['clusterID'] == c].sort_values(by=colonne)
        # On fait la jointure approximative
        toJoin = pd.merge_asof(toJoin, vH, left_on=colonne,
                               right_on='classes', direction='backward')
        toJoin[fonction] = toJoin['hauteurs']
        toJoin = toJoin.drop(columns=['classes', 'hauteurs'])
        # On met à jour df
        df = pd.concat([df[df['clusterID'] != c], toJoin])
    df[fonction].fillna(0)

    return df


def connexion():
    conn = psycopg2.connect(host="localhost",
                            database="NOPLP",
                            user="postgres",
                            password="Objectifcentrale2019!")
    return (conn, conn.cursor())


def trainModel(train_data, train_labels, cat_features, class_weight=[1]*8):

    print("Training the CatBoost model...")
    model = CatBoostClassifier(iterations=10,
                               depth=10,
                               learning_rate=1,
                               loss_function='MultiClass',
                               class_weights=class_weight,
                               verbose=False)
    model.fit(train_data, train_labels, cat_features=cat_features)

    return model


def confusionMatrixCalculation(model, test_pool, test_data, test_labels):

    # Prediction on test set
    print("Predicting on the test set...")
    preds_class = model.predict(test_pool)
    preds_proba = model.predict_proba(test_pool)
    preds = model.predict_log_proba(test_pool)

    # Confusion matrix
    print("Confusion matrix :")
    test_data["pred"] = preds_class
    test_data["labels"] = test_labels
    confusionMatrix = skl.confusion_matrix(
        test_data['labels'], test_data['pred'])

    return confusionMatrix


def precisionOrRecall(metric, c, confusionMatrix):
    res = 0
    if metric == "Precision":
        s = sum(confusionMatrix[c, ])
        if s == 0:
            res = 0
        else:
            res = confusionMatrix[c, c]/s
    elif metric == "Recall":
        s = sum(confusionMatrix[:, c])
        if s == 0:
            res = 0
        else:
            res = confusionMatrix[c, c]/s
    else:
        raise("metric argument must be either Precision or Recall")
    return round(res * 100, 1)


def F1score(p, r):
    if p == 0 or r == 0:
        return 0
    else:
        return round(2/(1/p + 1/r), 1)


def metricCalculation(confusionMatrix):

    # Calcul de la précision
    P5 = precisionOrRecall("Precision", 5, confusionMatrix)
    print("P5 = {0}".format(P5))
    P6 = precisionOrRecall("Precision", 6, confusionMatrix)
    print("P6 = {0}".format(P6))
    l = 0.9
    precision = round(l*P5 + (1-l)*P6, 1)
    print("Precision = {0}".format(precision))

    # Calcul du recall
    R5 = precisionOrRecall("Recall", 5, confusionMatrix)
    print("R5 = {0}".format(R5))
    R6 = precisionOrRecall("Recall", 6, confusionMatrix)
    print("R6 = {0}".format(R6))
    mu = 0.5
    recall = round(mu*R5 + (1-mu)*R6, 1)
    print("Recall = {0}".format(recall))

    # Calcul du F1-score
    F1 = F1score(precision, recall)
    print("F1-score = {0}".format(F1))

    return {"Precision": precision, "Recall": recall, "F1score": F1}
