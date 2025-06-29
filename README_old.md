# 📊 MS-RCPSP Analysis - Multi-Skill Resource-Constrained Project Scheduling

Ce projet implémente une suite complète d'algorithmes heuristiques pour l'ordonnancement de projs de ressources (MS-RCPSP). Il analyse et compare différentes règles de priorité pour optimiser le makespan (durée totale du projet).

## 🚀 Fonctionnalités Principales

- **10 algorithmes de priorité** : HRPW*, LST, LFT, MTS, TIMROS, HRU1, TIMRES, HRU2, STFD, EFT
- **5 algorithmes de makespan** : EDD, SPT, LPT, FCFS, RANDOM
- **Analyse comparative complète** avec statistiques détaillées
- **Gestion automatique des contraintes** de précédence et de ressources
- **Export des résultats** en formats JSON et CSV
- **Interface en ligne de commande** simple et intuitive

## 📁 Structure du Projet

```
MS-RCPSP-Analysis/
├── instances/                    # Fichiers d'instances .dzn
│   ├── inst_set1a_sf0_nc1.5_n20_m10_*.dzn
│   ├── inst_set1a_sf0_nc1.8_n20_m20_*.dzn
│   └── ...
├── resultats/                    # Résultats générés
│   ├── HRPW*/                   # Résultats par algorithme
│   ├── LST/
│   ├── LFT/
│   ├── ...
│   ├── makespan_comparison.csv   # Comparaison détaillée
│   ├── summary_statistics.csv   # Statistiques résumées
│   └── makespan_details/        # Détails par instance
├── paste.py                     # Algorithmes de priorité
├── makespan_calculator.py       # Calculateur de makespan
├── run_analysis.py             # Script principal
├── debug_test.py               # Tests de débogage
└── README.md                   # Cette documentation
```

## ⚙️ Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)


## 📊 Résultats Générés

### Fichiers de Sortie

1. **`makespan_comparison.csv`** - Comparaison détaillée de tous les algorithmes
   ```csv
   Instance,Algorithm,Makespan,Efficiency_Score,Resource_Utilization
   inst_set1a_sf0_nc1.5_n20_m10_00,HRPW*,45,0.85,0.78
   inst_set1a_sf0_nc1.5_n20_m10_00,LST,43,0.87,0.82
   ```

2. **`summary_statistics.csv`** - Statistiques résumées par algorithme
   ```csv
   Algorithm,Avg_Makespan,Min_Makespan,Max_Makespan,Std_Dev,Success_Rate
   HRPW*,42.3,35,52,4.2,100%
   LST,41.8,34,51,4.1,100%
   ```

3. **`makespan_details/`** - Détails par instance et algorithme
   ```json
   {
     "instance": "inst_set1a_sf0_nc1.5_n20_m10_00",
     "algorithm": "HRPW*",
     "makespan": 45,
     "schedule": [...],
     "resource_usage": [...]
   }
### Dépendances
```bash
pip install pandas numpy networkx
```

## 🎯 Algorithmes Implémentés

### 🏆 Algorithmes de Priorité (Heuristiques)

| Rang | Algorithme | Abréviation | Description |
|------|------------|-------------|-------------|
| 1 | **Highest Rank Positional Weight** | `HRPW*` | Priorise selon le poids positionnel maximal |
| 2 | **Late Start Time** | `LST` | Ordonne par temps de début tardif |
| 3 | **Late Finish Time** | `LFT` | Ordonne par temps de fin tardif |
| 4 | **Maximum Total Successors** | `MTS` | Priorise les tâches avec le plus de successeurs |
| 5 | **TIMROS** | `TIMROS` | Heuristique temps/ressources optimisée |
| 6 | **Highest Resource Utilization 1** | `HRU1` | Utilisation maximale des ressources (v1) |
| 7 | **TIMRES** | `TIMRES` | Variante de TIMROS |
| 8 | **Highest Resource Utilization 2** | `HRU2` | Utilisation maximale des ressources (v2) |
| 9 | **Smallest Dynamic Total Float** | `STFD` | Marge dynamique minimale |
| 10 | **Early Finish Time** | `EFT` | Temps de fin précoce |

### ⚡ Algorithmes de Makespan

| Algorithme | Description |
|------------|-------------|
| `EDD` | Earliest Due Date - Échéance la plus proche |
| `SPT` | Shortest Processing Time - Durée la plus courte |
| `LPT` | Longest Processing Time - Durée la plus longue |
| `FCFS` | First Come First Served - Premier arrivé, premier servi |
| `RANDOM` | Ordonnancement aléatoire |

## 🚀 Utilisation

### Démarrage Rapide
```bash
# Exécuter l'analyse complète
python run_analysis.py
```

Cette commande unique :
1. ✅ Vérifie et crée les répertoires nécessaires
2. ✅ Exécute tous les algorithmes de priorité
3. ✅ Calcule les makespans pour tous les algorithmes
4. ✅ Génère les statistiques comparatives
5. ✅ Sauvegarde tous les résultats

### Utilisation Avancée

#### Tester un algorithme spécifique
```bash
python debug_test.py
```

#### Exécuter seulement les algorithmes de priorité
```python
from paste import MSRCPSPPriorityAlgorithms, parse_dzn_file
instance_data = parse_dzn_file("instances/mon_instance.dzn")
algorithms = MSRCPSPPriorityAlgorithms(instance_data)
orders = algorithms.get_all_priority_orders()
```

#### Calculer seulement les makespans
```python
from makespan_calculator import MakespanCalculator
calculator = MakespanCalculator()
calculator.run_complete_analysis()
```

## 📁 Structure du Projet

```
MS-RCPSP-Analysis/
├── instances/                    # Fichiers d'instances .dzn
│   ├── inst_set1a_sf0_nc1.5_n20_m10_*.dzn
│   ├── inst_set1a_sf0_nc1.8_n20_m20_*.dzn
│   └── ...
├── resultats/                    # Résultats générés
│   ├── HRPW*/                   # Résultats par algorithme
│   ├── LST/
│   ├── LFT/
│   ├── ...
│   ├── makespan_comparison.csv   # Comparaison détaillée
│   ├── summary_statistics.csv   # Statistiques résumées
│   └── makespan_details/        # Détails par instance
├── paste.py                     # Algorithmes de priorité
├── makespan_calculator.py       # Calculateur de makespan
├── run_analysis.py             # Script principal
├── debug_test.py               # Tests de débogage
└── README.md                   # Cette documentation
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


## 🏆 Performances des Algorithmes (Résultats Expérimentaux)

Les algorithmes ont été classés selon leurs performances moyennes sur différents types d'instances. Les résultats détaillés sont générés automatiquement lors de l'analyse complète.

**Note** : Les performances peuvent varier selon le type d'instance et les contraintes spécifiques. Utilisez `run_analysis.py` pour obtenir des comparaisons détaillées sur vos propres instances.

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

### Format des Résultats JSON
```json
{
  "instance": "inst_set1a_sf0_nc1.5_n20_m10_00",
  "rule": "HRPW*",
  "n_activities": 22,
  "ordered_activities": [1, 2, 4, 3, 5, 7, 10, 11, 6, 9, 8, 13, 14, 15, 16, 18, 12, 17, 20, 19, 21, 22],
  "durations": [0, 9, 6, 5, 8, 4, 2, 8, 9, 9, 9, 9, 1, 1, 6, 5, 3, 3, 9, 10, 3, 0]
}
```

## 📈 Analyse des Performances

### Métriques Calculées
- **Makespan** : Durée totale du projet
- **Efficacité** : Ratio entre makespan optimal et makespan calculé
- **Utilisation des ressources** : Pourcentage d'utilisation moyenne
- **Taux de succès** : Pourcentage d'instances résolues avec succès

### Visualisation des Résultats
Les résultats peuvent être analysés avec n'importe quel outil de visualisation (Excel, Python matplotlib, R, etc.) en important les fichiers CSV générés.

## 🔧 Format des Instances

Les instances sont au format `.dzn` (MiniZinc) avec la structure suivante :

```dzn
nActs = 22;                    % Nombre d'activités
nRes = 10;                     % Nombre de ressources
dur = [0, 9, 6, 5, 8, ...];    % Durées des activités
rreq = [|0,0,0,0,0,0,0,0,0,0|  % Ressources requises
        |1,2,0,0,0,0,0,0,0,0|   % par activité
        |...                 |];
pred = [|0,0,0,0,0,0,0,0,0,0|   % Prédécesseurs
        |1,0,0,0,0,0,0,0,0,0|   % par activité
        |...                 |];
```

## 🐛 Résolution de Problèmes

### Erreurs Communes

1. **"'list' object has no attribute 'get'"**
   - ✅ **Résolu** : Cette erreur a été corrigée dans la version actuelle
   - Cause : Mauvaise gestion des structures de données dans les calculs de ressources

2. **"No module named 'paste'"**
   ```bash
   # Vérifiez que paste.py est dans le même répertoire
   ls -la paste.py
   ```

3. **"Aucune instance .dzn trouvée"**
   ```bash
   # Vérifiez le contenu du répertoire instances
   ls -la instances/
   ```

### Debug Mode
Pour déboguer un problème spécifique :
```bash
python debug_test.py
```

## 📚 Références

- **MS-RCPSP** : Multi-Skill Resource-Constrained Project Scheduling Problem
- **Heuristiques de priorité** : Règles de dispatching pour l'ordonnancement
- **Makespan** : Critère d'optimisation principal (durée totale du projet)

## 📝 Changelog

### Version 1.1.0 (Actuelle)
- ✅ **Correction majeure** : Résolution de l'erreur "'list' object has no attribute 'get'"
- ✅ **Amélioration** : Gestion robuste des ressources avec vérification de limites
- ✅ **Optimisation** : Refactorisation du code pour de meilleures performances
- ✅ **Interface** : Script principal unifié (`run_analysis.py`)
- ✅ **Documentation** : README complet et détaillé

### Version 1.0.0
- 🎯 Implémentation initiale des 10 algorithmes de priorité
- 📊 Calculateur de makespan avec 5 algorithmes
- 📁 Structure de projet organisée
- 📈 Export des résultats en JSON et CSV

---

**🎯 Objectif** : Fournir une suite complète d'outils pour l'analyse comparative d'algorithmes d'ordonnancement MS-RCPSP avec une interface simple et des résultats détaillés.

**📞 Support** : Pour toute question ou problème, ouvrez une issue sur le repository GitHub.


