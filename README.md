# Challenge_OPSIE-SISE
March 2023
​#### Quick summary
Log analysis: creation of a streamlit application including a dataviz part with many graphs and an attack detection part using unsupervised models such as isolation forest or kmeans

## Introduction

### Quelques précisions 
Le fichier analyse_donnees.zip correspond à la question 1.1 du sujet pour le challenge OPSIE/SISE.

## Organisation du dépôt Git 

Le dossier app contient les scripts notebooks des analyses descriptives réalisées sur les jeux de données fournit pour le challenge. Il contient l'analyse global sur le fichier log et les analyses plus poussées sur les adresses IP sources. 

Le dossier model contient les scripts notebooks des différents modèles testés pour prédire le risque d'attaque par adresse IP, il contient principalement des modèles non supervisés, dont l'IsolationForest qui sera utilisé pour l'application streamlit. 

Les différents fichiers functions sont utilisés et sont appelés par l'application streamlit dans la préparation des données, la création des graphiques et la partie prédiction.

## Afin de lancer l'application il faut :

Créer un environnement et réaliser un git clone du dépôt dans un dossier de votre choix.

Dans la console bash :
```
git clone https://github.com/Skarbkit/Challenge_OPSIE-SISE.git
```

Installer le fichier requirements.txt :
```
$pip install -r requirements.txt
```


Lancer l'application Streamlit :
```
python -m streamlit run Accueil.py
```

