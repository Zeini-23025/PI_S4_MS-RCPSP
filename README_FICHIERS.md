# 📋 Guide des fichiers - Projet MS-RCPSP avec Machine Learning

## 🎯 Vue d'ensemble

Ce document décrit tous les fichiers du projet et leur utilisation. Utilisez-le comme référence pour naviguer dans le projet.

## 📁 Fichiers par catégorie

### 🧠 Système Machine Learning (Nouveaux)

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **`binary_relevance_msrcpsp.py`** | Module ML principal (1400+ lignes) | Pour entraîner des modèles ML et résoudre avec IA |
| **`assistant_ml.py`** | Interface guidée intuitive | **Idéal pour débuter** - Menu simple en français |
| **`exemple_ml.py`** | Exemples et démonstrations | Pour comprendre le fonctionnement avec des exemples |
| **`demo_ml_integration.py`** | Tests interactifs et benchmarks | Pour tester des instances spécifiques et voir les performances |
| **`test_automatique.py`** | Tests automatisés complets | Pour valider que tout fonctionne correctement |

### 🔧 Solveur de base (Existants)

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **`msrcpsp_final.py`** | Cœur du solveur, toutes les heuristiques | Base technique - utilisé par les autres modules |
| **`msrcpsp_optimized.py`** | Interface principale optimisée | **Version classique** sans ML, avec menu |
| **`msrcpsp_complete.py`** | Version complète pour analyse massive | Pour analyser de très nombreuses instances |
| **`validate.py`** | Validation des solutions | Pour vérifier la validité des plannings générés |
| **`demo.py`** | Démonstration simple | Test rapide du solveur de base |

### 📚 Documentation

| Fichier | Description | Pour qui |
|---------|-------------|----------|
| **`README.md`** | Documentation principale du projet | **Tout le monde** - Vue d'ensemble complète |
| **`README_ML.md`** | Documentation technique ML complète | Développeurs, utilisateurs avancés |
| **`GUIDE_ML.md`** | Guide utilisateur ML simplifié | **Débutants** - Explications simples |
| **`COMMENT_TESTER.md`** | Guide pour tester le projet | **Validation** - Comment s'assurer que tout fonctionne |
| **`GUIDE_TEST_COMPLET.md`** | Tests détaillés et diagnostics | Tests approfondis, dépannage |
| **`RÉSUMÉ_ML.md`** | Résumé de l'implémentation ML | Vue d'ensemble rapide du ML |
| **`INDEX_FICHIERS_ML.md`** | Index de tous les fichiers ML | Navigation dans les fichiers ML |
| **`README_FICHIERS.md`** | Ce fichier - Guide des fichiers | Comprendre la structure du projet |

### 📂 Répertoires de données

| Répertoire | Contenu | Usage |
|------------|---------|--------|
| **`Instances/`** | 6600+ fichiers .msrcp | Données d'entrée pour l'entraînement et les tests |
| **`resultats/`** | Résultats du solveur, modèles ML | Sorties du solveur classique et modèles entraînés |
| **`resultats_ml/`** | Résultats spécifiques au ML | Prédictions, rapports et analyses ML |
| **`__pycache__/`** | Cache Python | Fichiers temporaires (générés automatiquement) |

## 🚀 Chemins d'utilisation recommandés

### 🔰 Je débute avec le projet
```
1. README.md                    ← Vue d'ensemble
2. python3 assistant_ml.py      ← Interface guidée
3. GUIDE_ML.md                  ← Explications simples
4. python3 exemple_ml.py        ← Exemples concrets
```

### 🎓 Je veux comprendre le ML
```
1. RÉSUMÉ_ML.md                 ← Résumé rapide
2. python3 exemple_ml.py        ← Voir des exemples
3. README_ML.md                 ← Documentation technique
4. python3 demo_ml_integration.py ← Tests interactifs
```

### 👨‍💻 Je veux utiliser le système complet
```
1. README_ML.md                 ← Documentation technique
2. python3 binary_relevance_msrcpsp.py ← Système principal
3. python3 test_automatique.py  ← Validation
4. GUIDE_TEST_COMPLET.md        ← Tests approfondis
```

### 🛠️ Je veux modifier ou déboguer
```
1. INDEX_FICHIERS_ML.md         ← Structure complète
2. binary_relevance_msrcpsp.py  ← Code principal ML
3. msrcpsp_final.py             ← Solveur de base
4. test_automatique.py          ← Tests pour validation
```

## 🎯 Fichiers par objectif

### Pour **tester rapidement** le projet
- `python3 assistant_ml.py` → Option 1 ou 6
- `python3 test_automatique.py --quick`
- `python3 exemple_ml.py`

### Pour **entraîner un modèle ML**
- `python3 binary_relevance_msrcpsp.py` → Option 1
- `python3 assistant_ml.py` → Option 2

### Pour **résoudre des instances avec ML**
- `python3 binary_relevance_msrcpsp.py` → Option 2
- `python3 assistant_ml.py` → Option 3

### Pour **comparer les performances**
- `python3 demo_ml_integration.py` → Option 3
- `python3 binary_relevance_msrcpsp.py` → Option 4

### Pour **comprendre le système**
- `GUIDE_ML.md` - Explications utilisateur
- `README_ML.md` - Documentation technique
- `exemple_ml.py` - Exemples pratiques

### Pour **valider le fonctionnement**
- `python3 test_automatique.py`
- `COMMENT_TESTER.md`
- `GUIDE_TEST_COMPLET.md`

## 📊 Tailles et complexité des fichiers

### Fichiers principaux
| Fichier | Lignes | Complexité | Description |
|---------|--------|------------|-------------|
| `binary_relevance_msrcpsp.py` | ~1400 | ⭐⭐⭐ | Module ML complet |
| `msrcpsp_final.py` | ~800 | ⭐⭐⭐ | Solveur de base |
| `demo_ml_integration.py` | ~400 | ⭐⭐ | Interface démonstration |
| `test_automatique.py` | ~350 | ⭐⭐ | Tests automatisés |
| `assistant_ml.py` | ~180 | ⭐ | Interface simple |
| `exemple_ml.py` | ~300 | ⭐ | Exemples guidés |

### Documentation
| Fichier | Taille | Public cible |
|---------|--------|--------------|
| `README.md` | ~8KB | Général |
| `README_ML.md` | ~15KB | Technique |
| `GUIDE_ML.md` | ~12KB | Utilisateur |
| `COMMENT_TESTER.md` | ~7KB | Validation |
| `GUIDE_TEST_COMPLET.md` | ~25KB | Tests détaillés |

## 🔄 Flux de données entre fichiers

```
Instances/*.msrcp
    ↓
msrcpsp_final.py (parsing et résolution)
    ↓
binary_relevance_msrcpsp.py (extraction features + ML)
    ↓
resultats/ + resultats_ml/ (sauvegarde)
    ↓
Interfaces utilisateur (assistant_ml.py, demo_ml_integration.py, etc.)
```

## ⚙️ Dépendances entre fichiers

### Fichiers indépendants
- `assistant_ml.py` - Interface autonome
- `exemple_ml.py` - Exemples autonomes
- `test_automatique.py` - Tests autonomes
- Tous les fichiers `.md` - Documentation

### Fichiers avec dépendances
- `binary_relevance_msrcpsp.py` → Peut utiliser `msrcpsp_final.py`
- `demo_ml_integration.py` → Utilise `binary_relevance_msrcpsp.py`
- `validate.py` → Utilise `msrcpsp_final.py`

## 🚨 Dépannage par fichier

### Si `assistant_ml.py` ne fonctionne pas
1. Vérifier les modules : `numpy`, `pandas`, `sklearn`
2. Tester : `python3 -c "import numpy, pandas, sklearn; print('OK')"`

### Si `binary_relevance_msrcpsp.py` a des erreurs
1. Vérifier que `msrcpsp_final.py` existe
2. Tester : `python3 -c "from binary_relevance_msrcpsp import *; print('OK')"`

### Si les tests échouent
1. Lancer : `python3 test_automatique.py --quick`
2. Consulter : `GUIDE_TEST_COMPLET.md`

### Si les instances ne se chargent pas
1. Vérifier : `ls -la Instances/`
2. Compter : `find Instances/ -name "*.msrcp" | wc -l`

## 📋 Checklist pour nouveaux utilisateurs

- [ ] **Lire** `README.md` pour la vue d'ensemble
- [ ] **Installer** numpy, pandas, scikit-learn
- [ ] **Tester** `python3 assistant_ml.py`
- [ ] **Exécuter** `python3 test_automatique.py --quick`
- [ ] **Consulter** `GUIDE_ML.md` pour comprendre
- [ ] **Essayer** `python3 exemple_ml.py`

## 🏆 Commandes rapides par fichier

```bash
# Tests et validation
python3 test_automatique.py              # Tests complets
python3 test_automatique.py --quick      # Tests rapides

# Interfaces utilisateur
python3 assistant_ml.py                  # Menu guidé
python3 exemple_ml.py                    # Exemples
python3 demo_ml_integration.py           # Démonstrations

# Système principal
python3 binary_relevance_msrcpsp.py      # ML complet
python3 msrcpsp_optimized.py             # Solveur classique

# Diagnostic
python3 -c "from binary_relevance_msrcpsp import *; print('✅ ML OK')"
ls -la Instances/ | head -5              # Vérifier instances
ls -la resultats/                        # Vérifier résultats
```

---

## 🎯 Résumé pour navigation rapide

| Je veux... | Fichier à utiliser | Commande |
|------------|-------------------|----------|
| **Démarrer rapidement** | `assistant_ml.py` | `python3 assistant_ml.py` |
| **Voir des exemples** | `exemple_ml.py` | `python3 exemple_ml.py` |
| **Entraîner un modèle** | `binary_relevance_msrcpsp.py` | Option 1 |
| **Résoudre avec ML** | `binary_relevance_msrcpsp.py` | Option 2 |
| **Tester le système** | `test_automatique.py` | `python3 test_automatique.py` |
| **Comprendre le ML** | `GUIDE_ML.md` | Lire la documentation |
| **Résoudre un problème** | `GUIDE_TEST_COMPLET.md` | Guide de dépannage |

**🎉 Votre projet contient maintenant 17 fichiers avec un système ML complet et une documentation exhaustive !**
