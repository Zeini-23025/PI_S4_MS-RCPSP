# Analyse et Comparaison d'Algorithmes pour le MS-RCPSP

Ce projet vise à analyser et comparer différentes règles de priorité pour la résolution du problème d'ordonnancement de projets avec contraintes de ressources et de compétences multiples (Multi-Skill Resource-Constrained Project Scheduling Problem - MS-RCPSP). Il permet de calculer le makespan (durée totale du projet) pour les ordonnancements générés par divers algorithmes heuristiques et d'évaluer leur performance. De plus, il intègre une fonctionnalité de calcul du flot maximal pour l'analyse de faisabilité d'allocation de ressources.

## Description du Problème (MS-RCPSP)

Le MS-RCPSP est un problème d'optimisation complexe où il s'agit d'ordonnancer un ensemble de tâches (activités) interdépendants, en tenant compte de ressources limitées et de compétences spécifiques requises par chaque tâche et possédées par les ressources. L'objectif principal est généralement de minimiser le makespan, c'est-à-dire la durée totale nécessaire pour achever toutes les tâches du projet.

## Fonctionnalités

*   **Parsing des Fichiers d'Instance (.dzn):** Lecture et interprétation des données d'instances du MS-RCPSP à partir de fichiers au format `.dzn`.
*   **Calcul des Métriques Temporelles:** Détermination des temps de début et de fin au plus tôt (EST, EFT) et au plus tard (LST, LFT), ainsi que du flottement dynamique pour chaque activité.
*   **Algorithmes de Priorité:** Implémentation de plusieurs règles de priorité heuristiques pour générer des ordres d'activités (e.g., HRPW*, LST, LFT, MTS, TIMROS, HRU1, TIMRES, HRU2, STFD, EFT).
*   **Calcul du Makespan:** Évaluation de la durée totale du projet pour chaque ordonnancement généré, en respectant les contraintes de précédence et de disponibilité des ressources/compétences.
*   **Analyse de Flot Maximal:** Une fonction de calcul du flot maximal (Edmonds-Karp) est incluse, avec une application spécifique pour construire un réseau de flot afin d'évaluer la faisabilité d'allocation de ressources basée sur les compétences.
*   **Génération de Rapports:**
    *   Fichiers JSON détaillés pour chaque instance et chaque algorithme, incluant le makespan, l'ordonnancement et l'ordre des activités.
    *   Un fichier CSV de comparaison (`makespan_comparison.csv`) récapitulant les makespans et les écarts par rapport au meilleur pour chaque instance et algorithme.
    *   Un fichier CSV de statistiques récapitulatives (`summary_statistics.csv`) présentant les makespans moyens, minimums, maximums, les temps d'exécution moyens, le nombre de victoires et le taux de succès pour chaque algorithme.
*   **Identification du Meilleur Algorithme:** Le script principal identifie et affiche l'algorithme le plus performant basé sur le makespan moyen.

## Structure du Projet

```
.
├── Comparison_of_Heuristic_Priority_Rules_in_the_Solu.pdf
├── debug_test.py
├── makespan_calculator.py       # Logique de calcul du makespan et de l'analyse comparative
├── paste.py                     # Parsing des fichiers .dzn, métriques temporelles, algorithmes de priorité, et calcul du flot maximal
├── README.md                    # Ce fichier
├── run_analysis.py              # Script principal pour lancer l'analyse complète
├── __pycache__/
├── .git/
├── instances/                   # Contient les fichiers d'instances .dzn
│   └── inst_set1a_sf0.5_nc1.5_n20_m10_00.dzn
│   └── ...
└── resultats/                   # Répertoire de sortie pour tous les rapports générés
    ├── HRPW*/
    ├── LST*/
    └── ...
    ├── makespan_details/
    ├── makespan_comparison.csv
    └── summary_statistics.csv
```

## Installation

### Prérequis

Assurez-vous d'avoir Python 3 installé sur votre système.

Les bibliothèques Python suivantes sont nécessaires :

*   `pandas`
*   `networkx`

Vous pouvez les installer via pip :

```bash
pip install pandas networkx
```

## Utilisation

1.  **Placez vos fichiers d'instances:** Mettez vos fichiers d'instances MS-RCPSP au format `.dzn` dans le répertoire `instances/`.
2.  **Exécutez le script principal:**

    ```bash
    python3 run_analysis.py
    ```

Le script va :
*   Vérifier et créer les répertoires nécessaires (`instances/`, `resultats/`).
*   Exécuter les algorithmes de priorité pour chaque instance et sauvegarder les ordres d'activités.
*   Calculer le makespan pour chaque ordonnancement.
*   Générer les fichiers de comparaison et de statistiques.
*   Afficher un résumé de l'analyse, y compris le meilleur algorithme global.

## Fichiers de Résultats

Tous les fichiers de sortie sont générés dans le répertoire `resultats/`:

*   `resultats/<ALGORITHME>/<INSTANCE_NAME>.json`: Contient l'ordre des activités, le makespan et l'ordonnancement détaillé pour chaque algorithme et instance.
*   `resultats/makespan_comparison.csv`: Un tableau comparatif des makespans pour toutes les instances et tous les algorithmes.
*   `resultats/summary_statistics.csv`: Statistiques agrégées sur la performance de chaque algorithme (makespan moyen, victoires, etc.).
*   `resultats/makespan_details/`: Contient des fichiers JSON détaillés par instance avec les résultats de tous les algorithmes.

# Analyse des Résultats des Algorithmes Heuristiques

Ce document présente les résultats comparatifs de plusieurs algorithmes heuristiques pour résoudre le problème d'ordonnancement de projet à ressources contraintes (MS-RCPSP).

## Tableau Récapitulatif des Performances

Le tableau ci-dessous synthétise les performances de chaque algorithme sur un ensemble d'instances de test.

| Algo    | Avg Makespan ↓ | Std Dev | Avg Time (s) | Wins | Remarque                                   |
| ------- | -------------- | ------- | ------------ | ---- | ------------------------------------------ |
| **LFT** | **77.34**      | 24.45   | 0.000316     | 136  |  Meilleur en moyenne et max de victoires |
| MTS     | 77.74          | 24.20   | 0.000322     | 122  | Très bon aussi                             |
| EFT     | 78.05          | 23.84   | 0.000337     | 109  | Bon                                        |
| LST     | 79.13          | 23.60   | 0.000318     | 96   | Moyen                                      |
| HRPW\*  | 79.13          | 23.60   | 0.000320     | 96   | Idem LST                                   |
| HRU1    | 80.25          | 22.79   | 0.000335     | 100  | Moins bon que LFT                          |
| HRU2    | 84.50          | 21.07   | 0.000327     | 71   | Faible perf                                |
| TIMRES  | 84.50          | 21.07   | 0.000324     | 71   | Idem HRU2                                  |
| TIMROS  | 84.79          | 20.81   | 0.000333     | 73   | Décevant                                   |
| STFD    | 87.77          | 20.16   | 0.000328     | 62   | Le plus faible                             |

### Explication des Colonnes

*   **Algo**: Le nom de l'algorithme heuristique testé.
*   **Avg Makespan ↓**: La durée moyenne du projet (makespan) calculée par l'algorithme sur toutes les instances. L'objectif est de minimiser cette valeur (indiqué par la flèche ↓). Une valeur plus faible est meilleure.
*   **Std Dev**: L'écart-type (Standard Deviation) des makespans. Une valeur plus faible indique que les résultats de l'algorithme sont plus constants et moins dispersés à travers les différentes instances.
*   **Avg Time (s)**: Le temps d'exécution moyen de l'algorithme en secondes.
*   **Wins**: Le nombre de fois où l'algorithme a obtenu le meilleur makespan (ou un makespan égal au meilleur) parmi tous les algorithmes pour une instance donnée.
*   **Remarque**: Une observation qualitative sur la performance de l'algorithme.

### Synthèse des Résultats

L'algorithme **LFT (Latest Finish Time)** se distingue comme le plus performant en moyenne, avec le **Avg Makespan** le plus bas (77.34) et le plus grand nombre de victoires (136). Il est suivi de près par **MTS (Most Total Successors)** et **EFT (Earliest Finish Time)**.

Les algorithmes comme **HRU2, TIMRES, TIMROS, et STFD** montrent des performances nettement inférieures, avec des makespans moyens plus élevés et moins de victoires.

En termes de temps de calcul, tous les algorithmes sont extrêmement rapides, avec des temps moyens de l'ordre de 0.3 millisecondes, ce qui les rend très efficaces pour une utilisation pratique.
