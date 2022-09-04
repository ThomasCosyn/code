import pandas as pd
from catboost import CatBoostClassifier, Pool
import sklearn.metrics as skl
import matplotlib.pyplot as plt
import util

# Chargement du dataset
print("Dataset loading...")
df = pd.read_csv("classificationDataset.csv", sep=";")

# Data Cleaning
print("Data cleaning...")
df = df.drop(columns=['Unnamed: 0', 'id', 'Chanson_id'])
reversed_cat = {'50': 1, '40': 2, '30': 3,
                '20': 4, '10': 5, 'MC': 6, '20k': 7, None: 8}
df = df.replace({'categorie': reversed_cat})

# Split train / test
print("Spliting in train and test...")
train = df[0:int(len(df)*0.8)]
print("Taille du dataset de train : " + str(len(train)))
test = df[int(len(df)*0.8)+1:]
print("Taille du dataset de test : " + str(len(test)))

# Tau resampling
tau = 0.3
dataset = util.buildDataset(train, tau)
train_labels = dataset['categorie']
trainSL = dataset.drop(columns=['categorie'])
train_data = trainSL

test_labels = test['categorie']
test = test.drop(columns=['categorie'])
test_data = test
test_pool = Pool(test_data,
                 test_labels,
                 cat_features=['titre', 'artiste', 'clusterid'])


# Training model
print("Training the CatBoost model...")
model = CatBoostClassifier(iterations=10,
                           depth=10,
                           learning_rate=1,
                           loss_function='MultiClassOneVsAll',
                           verbose=True,
                           class_weights=[0.25, 0.65, 0.325, 0.425, 0.175, 1.9375, 3.875, 0.1])
model.fit(train_data, train_labels, cat_features=[
          'titre', 'artiste', 'clusterid'])

# Feature importance
print("Features importance :")
for f in range(len(model.feature_names_)):
    print(model.feature_names_[f] + " : " + str(model.feature_importances_[f]))

# Sauvegarde du modèle
print("Saving model...")
model.save_model("ML/catboostModel.cbm", format="cbm")

# Prediction on test set
print("Predicting on the test set...")
preds_class = model.predict(test_pool)
preds_proba = model.predict_proba(test_pool)

# Confusion matrix
print("Confusion matrix :")
test_data["pred"] = preds_class
test_data["labels"] = test_labels
cm = skl.confusion_matrix(
    test_data['labels'], test_data['pred'])
dispCM = skl.ConfusionMatrixDisplay(cm)
dispCM.plot()
plt.show()

# Calcul des métriques
resMetriques = util.metricCalculation(cm)
print("F1-score : ", resMetriques["F1score"])
