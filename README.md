# MSRCPSP Solver - Multi-Skill Resource-Constrained Project Scheduling Problem

Ce projet propose un solveur avancé pour le problème d'ordonnancement de projet à ressources multiples et compétences multiples (MSRCPSP). Il intègre plusieurs heuristiques et une gestion intelligente des ressources pour garantir la diversité et la robustesse des solutions.

## Fonctionnalités principales
- **Analyse complète ou échantillonnée** de toutes les instances du dossier `Instances/`
- **Comparaison de 7 heuristiques** : EST, LFT, MSLF, SPT, LPT, FCFS, LST
- **Gestion avancée des ressources** : prise en compte des niveaux de compétence, multi-compétences, relaxation progressive
- **Détection et évitement des deadlocks**
- **Statistiques détaillées** sur la performance et la diversité des solutions
- **Export CSV/JSON** des résultats et des comparaisons

## Structure du projet
```
PI_S4_MS-RCPSP/
├── Instances/                # Dossier contenant les fichiers d'instances .msrcp
├── resultats/                # Résultats générés (CSV, JSON)
├── msrcpsp_final.py          # Cœur du solveur (logique et heuristiques)
├── msrcpsp_optimized.py      # Interface principale optimisée (menu, analyse, stats)
├── msrcpsp_complete.py       # Version complète (analyse massive)
├── test_comparison.csv       # Exemple de résultats comparatifs
└── README.md                 # Ce fichier
```

## Utilisation rapide
1. **Pré-requis** : Python 3.8+
2. **Placer vos instances** dans le dossier `Instances/` (format `.msrcp`)
3. **Lancer le solveur** :
   ```bash
   python msrcpsp_optimized.py
   ```
4. **Choisir le mode** :
   - 1️⃣ Analyse optimisée (échantillon)
   - 2️⃣ Analyse complète (toutes les instances)
   - 3️⃣ Test rapide (diagnostic)

## Explication des heuristiques
- **EST** : Earliest Start Time
- **LFT** : Latest Finish Time
- **MSLF** : Minimum Slack First
- **SPT** : Shortest Processing Time
- **LPT** : Longest Processing Time
- **FCFS** : First Come First Served
- **LST** : Latest Start Time

## Sorties et résultats
- Les résultats sont sauvegardés dans le dossier `resultats/` sous forme de fichiers CSV et JSON.
- Un fichier de comparaison (`*_comparison_*.csv`) permet de comparer les makespans de chaque heuristique sur chaque instance.
- Des statistiques détaillées sont générées automatiquement.

## Auteurs et contact
- Projet universitaire 2025 - Zeini-23025

---
**NB :** Ce projet est conçu pour la recherche et l'enseignement. Pour toute utilisation industrielle, merci de contacter l'auteur.
