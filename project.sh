#!/bin/bash

# Ce script exécute le flux de travail principal du projet MS-RCPSP avec Machine Learning.
# Il génère les données de performance, entraîne le modèle ML, puis utilise le modèle pour résoudre une instance.

# Étape 1: Générer les données de performance (Makespan)
# Ce script exécute les algorithmes de planification sur les instances et sauvegarde les résultats.
echo "
--- Étape 1: Génération des données de performance ---"
python3 msrcpsp_final.py

# Étape 2: Entraîner le Modèle de Machine Learning
# Ce script charge les données de makespan, extrait les caractéristiques et entraîne le modèle ML.
echo "
--- Étape 2: Entraînement du modèle ML ---"
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"

# Étape 3: Utiliser le Modèle pour Résoudre une Instance
# Ce script charge le modèle ML, prédit les meilleurs algorithmes et résout une instance spécifique.
echo "
--- Étape 3: Résolution d'une instance avec guidage ML ---"
python3 -c "from binary_relevance_msrcpsp import MLIntegratedMSRCPSP; ml_system = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl'); result = ml_system.solve_with_ml_guidance('Instances/MSLIB_Set1_1.msrcp'); print(result)"

echo "
--- Flux de travail terminé avec succès! ---"

