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
