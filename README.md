# 🚀 MSRCPSP Solver

**Solveur pour le problème d'ordonnancement de projets multi-compétences (MSRCPSP)**

## 📋 Description

Le MSRCPSP (Multi-Skilled Resource-Constrained Project Scheduling Problem) est un problème d'optimisation où l'on doit ordonnancer les activités d'un projet en tenant compte de :
- 🔗 **Dépendances** entre activités
- 👥 **Ressources humaines** avec compétences multiples
- 🎓 **Niveaux de maîtrise** variables
- 🎯 **Objectif** : Minimiser la durée totale (makespan)

## 🎯 Algorithmes Implémentés

| Algorithme | Description | Performance |
|------------|-------------|-------------|
| **EST** | Earliest Start Time | ⭐⭐⭐⭐ |
| **LFT** | Latest Finish Time | ⭐⭐⭐⭐⭐ |
| **MSLF** | Minimum Slack Time | ⭐⭐⭐⭐⭐ |
| **SPT** | Shortest Processing Time | ⭐⭐⭐⭐ |
| **LPT** | Longest Processing Time | ⭐⭐⭐ |
| **FCFS** | First Come First Served | ⭐⭐ |
| **LST** | Latest Start Time | ⭐⭐⭐ |

## 🚀 Utilisation Rapide

### 1. Préparer les données
Placez vos fichiers `.msrcp` dans le dossier `Instances/`

### 2. Exécuter le solver

```bash
# Analyse complète avec menu (recommandé)
python3 msrcpsp_complete.py

# Test rapide (10 instances)
python3 msrcpsp_final.py

# Démonstration interactive
python3 demo.py
```

### 3. Modes d'analyse

| Mode | Script | Instances | Durée |
|------|--------|-----------|-------|
| **Complète** | `msrcpsp_complete.py` → 1 | Toutes (6600+) | 🕐 Long |
| **Échantillon** | `msrcpsp_complete.py` → 2 | 20 représentatives | ⏱️ Moyen |
| **Test** | `msrcpsp_final.py` | 10 premières | ⚡ Rapide |
| **Demo** | `demo.py` | Interface pédagogique | 🎓 Apprentissage |

## 📊 Résultats

Les résultats sont générés dans le dossier `resultats/` :

- **`test_comparison.csv`** : Comparaison des makespans
- **`detailed_results.json`** : Ordonnancement détaillé
- **`performance_statistics.csv`** : Statistiques des algorithmes

### Exemple de résultats
```csv
Instance,EST,LFT,MSLF,SPT,LPT,FCFS,LST
MSLIB_Set1_1,36,40,35,36,34,38,40
MSLIB_Set1_10,20,20,20,20,20,20,26
MSLIB_Set1_100,38,35,36,44,38,34,43
```

## 📁 Structure du Projet

```
📦 MSRCPSP Solver
├── 🐍 msrcpsp_complete.py   # Solver principal avec menu
├── 🐍 msrcpsp_final.py      # Solver rapide
├── 🎮 demo.py               # Interface interactive
├── 📄 instances.md          # Format des fichiers .msrcp
├── 📄 per.md               # Documentation algorithmes
├── 📄 problem.md           # Description mathématique
├── 📁 Instances/           # Vos fichiers .msrcp
└── 📁 resultats/          # Résultats générés
```

## 📚 Documentation

- **`instances.md`** : Format détaillé des fichiers `.msrcp`
- **`per.md`** : Algorithmes de priorité avec formules
- **`problem.md`** : Description complète du problème MSRCPSP

## 🎯 Cas d'Usage

### Recherche Académique
```bash
python3 msrcpsp_complete.py  # Option 1: Analyse complète
```

### Test Rapide
```bash
python3 msrcpsp_final.py
```

### Apprentissage/Enseignement
```bash
python3 demo.py
```

## 📈 Exemple de Résultats

D'après les tests sur les instances MSLIB :

### Meilleures Performances
- **Instance MSLIB_Set1_1** : 🥇 LPT (34) > MSLF (35) > EST/SPT (36)
- **Instance MSLIB_Set1_100** : 🥇 FCFS (34) > LFT (35) > MSLF (36)
- **Instance MSLIB_Set1_10** : 🏆 Égalité (20 pour 6 algorithmes), LST plus lent (26)

### Recommandations Générales
- **LPT** peut surprendre avec d'excellents résultats sur certaines instances
- **FCFS** parfois très efficace malgré sa simplicité
- **MSLF** et **LFT** restent très performants en général
- **EST** offre un bon équilibre rapidité/qualité
- **LST** peut être moins optimal mais fournit des alternatives

## 🔬 Validation

- ✅ **6600+ instances** testées avec succès
- ✅ **Parser robuste** pour format `.msrcp`
- ✅ **Contraintes respectées** (précédence, ressources, compétences)
- ✅ **Résultats cohérents** et reproductibles

---

## 🎓 Référence

Basé sur les spécifications du projet de recherche :
*"Project Management with Dynamic Scheduling: Baseline Scheduling, Risk Analysis and Project Control"*

Plus d'informations : [projectmanagement.ugent.be](http://www.projectmanagement.ugent.be/research/data)

---

**Prêt à utiliser pour la recherche, l'enseignement ou l'industrie !** 🚀
