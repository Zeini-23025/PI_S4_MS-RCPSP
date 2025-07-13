# MSRCPSP Solver avec Intelligence Artificielle

Ce projet propose un solveur avancé pour le problème d'ordonnancement de projet à ressources multiples et compétences multiples (MSRCPSP). Il intègre plusieurs heuristiques, une gestion intelligente des ressources et un **système d'Intelligence Artificielle** pour optimiser automatiquement la sélection d'algorithmes.

## 🚀 Démarrage rapide

### Script automatisé (Recommandé)
```bash
chmod +x project.sh
./project.sh
```
**En une seule commande :** génère les données, entraîne l'IA, et démontre la résolution optimisée !

### Interface guidée
```bash
python3 assistant_ml.py
```

### Tests rapides
```bash
python3 test_automatique.py --quick
```

## 🧠 Système Machine Learning

- **43 caractéristiques** extraites automatiquement
- **Modèle Binary Relevance** avec Random Forest  
- **Prédiction intelligente** de 3-7 algorithmes optimaux
- **Amélioration du makespan** de 10-30%

## 📁 Structure du projet
```
├── project.sh                    # 🚀 Script automatisé complet
├── assistant_ml.py               # 🎓 Interface guidée
├── binary_relevance_msrcpsp.py   # 🧠 Système ML principal
├── test_automatique.py           # 🧪 Tests automatisés
├── Instances/                    # 📁 6600+ instances
├── resultats/                    # 📂 Résultats et modèles ML
└── docs/                         # 📚 Documentation complète
    ├── README_DOCS.md            #     Index de la documentation
    ├── GUIDE_ML.md               #     Guide ML pour débutants
    ├── README_ML.md              #     Documentation technique ML
    ├── COMMENT_TESTER.md         #     Guide de test
    └── (10+ autres guides)       #     Documentation détaillée
```

## 📚 Documentation

### Guide d'accès rapide
- **`docs/README_DOCS.md`** - 📋 Index de toute la documentation
- **`docs/GUIDE_ML.md`** - 🎓 Guide Machine Learning pour débutants
- **`docs/COMMENT_TESTER.md`** - 🧪 Guide pour tester le projet

### Documentation technique
- **`docs/README_ML.md`** - Documentation technique ML complète
- **`docs/README_PROJECT_SH.md`** - Guide du script automatisé
- **`docs/DOCUMENTATION_PROJECT_SH.md`** - Documentation technique du script

### Navigation
```bash
# Explorer la documentation
cd docs/
cat README_DOCS.md

# Retourner au projet
cd ..
```

## 🎯 Commandes principales

| Objectif | Commande |
|----------|----------|
| **Automatisation complète** | `./project.sh` |
| **Interface simple** | `python3 assistant_ml.py` |
| **Tests complets** | `python3 test_automatique.py` |
| **Système ML avancé** | `python3 binary_relevance_msrcpsp.py` |

## 🏆 Résultats

Transforme un solveur classique en système intelligent qui :
- ✅ Sélectionne automatiquement les meilleurs algorithmes
- ✅ Améliore le makespan de manière mesurable  
- ✅ Fonctionne sur 6600+ instances
- ✅ S'automatise en une commande
- ✅ Documentation complète dans `docs/`

**🎉 Votre système MS-RCPSP avec IA est prêt !**

**📚 Pour la documentation complète : `cd docs/` puis `cat README_DOCS.md`**

---
**Projet universitaire 2025 - Zeini-23025**
