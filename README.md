# 📋 Ordonnancement de Projets avec Algorithmes de Priorité

Ce projet implémente différentes heuristiques d'ordonnancement de tâches à partir de fichiers `.dzn`, en prenant en compte les contraintes de précédence et de ressources. Il analyse ensuite la qualité des ordonnancements via des graphes de flot (NetworkX) et génère des résultats au format JSON et CSV.

## 📁 Structure du Projet

```
.
├── instances/             # Fichiers .dzn à parser (définition des tâches)
├── resultats/             # Résultats de chaque heuristique (JSON)
│   └── <heuristique>/     # Résultats spécifiques à chaque règle de priorité
├── algorithmes.py         # Génération des ordonnancements
├── ford_fulkerson.py        # Analyse par flot maximum et export CSV
├── README.md              # Documentation principale
```
```
projet/
├── instances/              # Fichiers .dzn d'instances
├── resultats/              # Résultats des algorithmes
│   ├── HRPW*/             # Résultats HRPW*
│   ├── LST/               # Résultats LST
│   ├── ...                # Autres algorithmes
│   ├── makespan_comparison.csv
│   ├── summary_statistics.csv
│   └── makespan_details/  # Détails par instance
├── paste.py               # Votre code des algorithmes
├── makespan_calculator.py # Calculateur de makespan
└── run_analysis.py        # Script principal
```
## ⚙️ Installation

### Dépendances

- Python 3.8+
- networkx
- re, json, os, csv, glob (librairies standard)

Installez la dépendance principale avec :
```bash
pip install networkx
```

## 🚀 Utilisation

### 1. Générer les ordonnancements

```bash
python algorithmes.py
```
Cela lit les fichiers `.dzn` dans `./instances/`, applique les heuristiques de priorité, respecte les contraintes de précédence, et sauvegarde les résultats ordonnés dans `./resultats/<heuristique>/`.

### 2. Lancer l’analyse des ordonnancements

```bash
python ford_fulkerson.py
```
Cela :
- reconstruit différents types de graphes (précédence, ressource, temporel),
- applique l’algorithme de flot maximum (Edmonds-Karp),
- mesure des métriques (efficacité, durée totale, validité),
- exporte les résultats dans un CSV.


## 🏆 Top 5 des règles selon les performances (résultats expérimentaux)

### En allocation séquentielle (Serial Allocation) :

| Rang  | Règle      | Performance (plus faible augmentation de la durée projet) |
|-------|------------|----------------------------------------------------------|
| 🥇 1  | **LST**    | Meilleure dans la plupart des cas                        |
| 🥈 2  | **HRPW\*** | Très performante avec plusieurs ressources               |
| 🥉 3  | **LFT**    | Également très efficace                                  |
| 🏅 4  | **MTS**    | Avantageuse dans certains cas                            |
| 🏅 5  | **MIS**    | Bon comportement dans certains scénarios                 |

### En allocation parallèle (Parallel Allocation) :

| Rang  | Règle             | Performance globale                  |
|-------|-------------------|--------------------------------------|
| 🥇 1  | **LFT**           | La meilleure globalement             |
| 🥈 2  | **LST**           | Excellente performance               |
| 🥉 3  | **HRPW\***        | Souvent dans le top 3                |
| 🏅 4  | **MTS**           | Forte avec plusieurs ressources      |
| 🏅 5  | **HRU1 / HRU2**   | Bonne dans les réseaux complexes     |




## 🏆 Top 10 des règles de priorité (ordonnées par performance globale)


|  Rang | Nom de la règle                      | Abréviation | Description simplifiée                                                          |
| ------- | ------------------------------------ | ----------- | ------------------------------------------------------------------------------- |
| 1     | **Highest Rank Positional Weight 2** | `HRPW*`     | Tient compte du poids des successeurs totaux (plus performant globalement).     |
| 2    | **Late Start Time**                  | `LST`       | Priorise les activités avec le début tardif le plus bas.                        |
| 3     | **Late Finish Time**                 | `LFT`       | Choisit l'activité avec la fin la plus tôt possible sans retarder le projet.    |
| 4     | **Maximum Total Successors**         | `MTS`       | Priorise les tâches avec le plus de successeurs au total.                       |
| 5     | **TIMROS**                           | `TIMROS`    | Heuristique basée sur le ratio du temps et de la disponibilité des ressources.  |
| 6     | **Highest Resource Utilization 1**   | `HRU1`      | Tient compte de l'utilisation cumulée des ressources sur les chemins critiques. |
| 7     | **TIMRES**                           | `TIMRES`    | Variante de TIMROS avec une formule de pondération différente.                  |
| 8     | **Highest Resource Utilization 2**   | `HRU2`      | Similaire à HRU1 mais pondéré par la durée des tâches.                          |
| 9     | **Smallest Dynamic Total Float**     | `STFD`      | Priorise les tâches avec le moins de marge dynamique.                           |
| 10      | **Early Finish Time**                | `EFT`       | Choisit les tâches qui finissent le plus tôt (simple mais efficace).            |
## 📊 Résultats générés

- **JSON** : Pour chaque instance et règle, le fichier contient :
  ```json
  
  "instance": "inst_set1a_sf0_nc1.5_n20_m10_03",
  "rule": "HRPW*",
  "ordered_activities": [
    1,2,4,3,5,7,10,11,6,
    9,8,13,14,15,16,18,12,
    17,20,19,21,22
  ],
  "durations": [
    0,9,6,5,8,4,2,8,
    9,9,9,9,1,1,6,5,
    3,3,9,10,3,0
  ]

  ```
- **CSV** :
  - `comparaison_algorithmes.csv` : comparai les resultat.
  - `resultats_details.csv` : Détails complets pour chaque instance et heuristique.

## 📦 Ajouter de nouvelles instances

Ajoutez simplement un fichier `.dzn` dans le dossier `instances/` contenant :
```dzn
nActs = 4;
dur = [3, 2, 1, 4];
pred = [1, 2];
succ = [2, 3];
```
Les graphes de précédence sont construits automatiquement.

## ❗ Remarques

- Les tâches sont numérotées à partir de 1.
- En l'absence d'information sur les ressources, 1 est utilisé par défaut.
- Le projet gère les dépendances circulaires en conservant l'ordre original.


