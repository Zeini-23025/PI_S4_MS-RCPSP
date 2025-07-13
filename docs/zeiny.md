# Guide d'Utilisation Rapide - Projet MS-RCPSP avec ML

## Résumé du Projet

Ce projet utilise des techniques de Machine Learning (ML) pour prédire les meilleurs algorithmes à utiliser pour résoudre le problème de planification de projet avec contraintes de ressources multi-compétences (MS-RCPSP). L'objectif est d'améliorer l'efficacité de la résolution en choisissant intelligemment l'heuristique la plus performante pour une instance donnée.

## Comment Utiliser le Projet (Flux de travail)

Voici les étapes pour utiliser le système, de la génération des données à l'utilisation du modèle ML.

### Étape 1 : Générer les Données de Performance (Makespan)

Le modèle ML a besoin de données pour apprendre. Ce script exécute plusieurs algorithmes de planification sur les instances de test et sauvegarde leurs performances (makespan).

**Exécutez la commande suivante :**
```bash
python3 msrcpsp_final.py
```
- **Ce que ça fait :** Ce script traite les instances du dossier `/Instances`, calcule le makespan pour chaque algorithme de planification, et sauvegarde les résultats détaillés dans le dossier `resultats/makespan_details/`. Ces fichiers sont essentiels pour l'étape suivante.

### Étape 2 : Entraîner le Modèle de Machine Learning

Une fois les données de performance générées, vous pouvez entraîner le modèle ML. Le modèle apprendra à associer les caractéristiques d'une instance aux algorithmes les plus performants.

**Exécutez la commande suivante :**
```bash
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"
```
- **Ce que ça fait :** Ce script charge les données de makespan, extrait les caractéristiques des instances, entraîne un modèle de classification (Binary Relevance avec Random Forest), et sauvegarde le modèle entraîné dans `resultats/binary_relevance_model.pkl`.

### Étape 3 : Utiliser le Modèle pour Résoudre une Instance

Avec un modèle entraîné, vous pouvez maintenant l'utiliser pour obtenir des recommandations d'algorithmes pour une nouvelle instance et la résoudre.

**Exécutez la commande suivante (exemple avec `MSLIB_Set1_1.msrcp`) :**
```bash
python3 -c "from binary_relevance_msrcpsp import MLIntegratedMSRCPSP; ml_system = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl'); result = ml_system.solve_with_ml_guidance('Instances/MSLIB_Set1_1.msrcp'); print(result)"
```
- **Ce que ça fait :** Ce script charge le modèle ML, prédit les 3 meilleurs algorithmes pour l'instance spécifiée, les exécute, et retourne le meilleur résultat (makespan) trouvé.

## Scripts Interactifs (Optionnel)

Pour une utilisation plus conviviale, vous pouvez utiliser les scripts suivants qui fournissent des menus interactifs :

- `python3 assistant_ml.py`: Un assistant complet pour tester, entraîner et utiliser le système.
- `python3 demo_ml_integration.py`: Des démonstrations interactives pour voir le système en action.
- `python3 binary_relevance_msrcpsp.py`: Le menu principal pour interagir avec le système ML.

---
Ce guide vous donne le flux de travail de base pour utiliser le projet. Chaque script a des fonctionnalités plus avancées que vous pouvez explorer en lisant leur code source.
