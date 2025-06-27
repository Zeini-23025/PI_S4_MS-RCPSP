# Analyse comparative d'algorithmes d'ordonnancement

Ce projet permet de comparer différents algorithmes d'ordonnancement sur des instances de problèmes, en utilisant des graphes de flot pour évaluer la qualité des solutions.

## Fonctionnalités

- Chargement automatique des instances et résultats d'algorithmes.
- Calcul du flot maximal (max flow) via plusieurs méthodes (précédence, ressources, direct).
- Analyse de la qualité des ordonnancements (durée totale, utilisation des ressources, etc.).
- Export des résultats comparatifs et détaillés au format CSV.

## Dépendances

- Python 3.x
- [networkx](https://networkx.org/)
- [csv](https://docs.python.org/3/library/csv.html)
- [json](https://docs.python.org/3/library/json.html)

Installez les dépendances principales avec :
```bash
pip install networkx
```

## Structure des dossiers

- `instances/` : contient les fichiers `.dzn` décrivant les instances.
- `resultats/` : contient les résultats JSON des différents algorithmes.
- `resultats/ford_fulkerson/` : résultats d'analyse comparative et exports CSV.

## Utilisation

Lancez l'analyse comparative avec :
```bash
python algorithmes.py
```

Les résultats seront générés dans `resultats/ford_fulkerson/`.

## Auteur

Projet développé par Zeiny.
