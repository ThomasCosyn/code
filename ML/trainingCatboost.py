import pandas as pd
import os
from catboost import CatBoostClassifier, Pool
import numpy as np
import sklearn.metrics as skl

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
train_labels = train['categorie']
train = train.drop(columns=['categorie'])
train_data = train
test_labels = test['categorie']
test = test.drop(columns=['categorie'])
test_data = test
test_pool = Pool(test_data,
                 test_labels,
                 cat_features=['titre', 'artiste'])

# Training model
print("Training the CatBoost model...")
model = CatBoostClassifier(iterations=50,
                           depth=10,
                           learning_rate=1,
                           loss_function='MultiClass',
                           verbose=True,
                           class_weights=[0.025, 0.025, 0.025, 0.025, 0.025, 0.425, 0.425, 0.025])
model.fit(train_data, train_labels, cat_features=['titre', 'artiste'])

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
print(skl.confusion_matrix(test_data['labels'], test_data['pred']))
