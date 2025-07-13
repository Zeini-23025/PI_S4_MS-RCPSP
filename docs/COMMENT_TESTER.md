# 🧪 Comment tester le projet MS-RCPSP avec Machine Learning

## 🎯 Vue d'ensemble

Ce guide vous explique toutes les méthodes pour tester votre projet MS-RCPSP équipé du système Machine Learning, depuis les tests rapides jusqu'aux validations complètes.

## ⚡ Tests rapides (2-5 minutes)

### Option 1 : Test automatisé
```bash
# Test automatique complet
python3 test_automatique.py

# Test rapide seulement
python3 test_automatique.py --quick

# Mode verbose pour plus de détails
python3 test_automatique.py --verbose
```

### Option 2 : Exemples simples
```bash
# Test avec exemples intégrés
python3 exemple_ml.py

# Choisir option 1 pour un exemple complet
```

### Option 3 : Assistant guidé
```bash
# Interface guidée avec vérifications
python3 assistant_ml.py

# Choisir option 1 pour test rapide
# Choisir option 6 pour vérification installation
```

## 🔧 Tests par composants

### 1. Test du solveur de base
```bash
# Solveur principal
python3 msrcpsp_final.py

# Version optimisée
python3 msrcpsp_optimized.py

# Validation des solutions
python3 validate.py
```

### 2. Test du système ML
```bash
# Interface principale ML
python3 binary_relevance_msrcpsp.py

# Démonstrations interactives  
python3 demo_ml_integration.py
```

## 📊 Tests complets (30-60 minutes)

### Scénario 1 : Premier démarrage
```bash
# 1. Vérification de base
python3 assistant_ml.py  # Option 6

# 2. Test des exemples
python3 exemple_ml.py    # Option 1

# 3. Entraînement du modèle ML
python3 binary_relevance_msrcpsp.py  # Option 1

# 4. Test de prédiction
python3 binary_relevance_msrcpsp.py  # Option 2
```

### Scénario 2 : Validation complète
```bash
# 1. Tests automatisés
python3 test_automatique.py --verbose

# 2. Benchmark de performance
python3 demo_ml_integration.py  # Option 3

# 3. Traitement en lot
python3 binary_relevance_msrcpsp.py  # Option 4
```

## ✅ Checklist de validation

### Prérequis
- [ ] Python 3.7+ installé
- [ ] Modules : `numpy`, `pandas`, `scikit-learn`
- [ ] Fichiers présents : `msrcpsp_final.py`, `binary_relevance_msrcpsp.py`, etc.
- [ ] Répertoire `Instances/` avec fichiers `.dzn` ou `.msrcp`

### Tests fonctionnels
- [ ] **Import ML** : `from binary_relevance_msrcpsp import *` sans erreur
- [ ] **Extraction features** : 43 caractéristiques extraites des instances
- [ ] **Entraînement ML** : Modèle sauvé dans `./resultats/binary_relevance_model.pkl`
- [ ] **Prédictions** : 3-7 algorithmes recommandés par instance
- [ ] **Résolution** : Instances résolues avec guidage ML

### Tests de performance
- [ ] **Diversité** : Algorithmes différents selon les instances
- [ ] **Makespan** : Amélioration de 10-30% observée
- [ ] **Temps** : Prédiction < 1s par instance
- [ ] **Taux de réussite** : > 90% des instances résolues

## 🚨 Dépannage

### Erreurs communes

#### "Module msrcpsp_final non trouvé"
```bash
# Vérifier la présence
ls -la msrcpsp_final.py

# Continuer sans ce module (fonctionnalités ML limitées)
```

#### "Aucune instance trouvée"
```bash
# Vérifier les instances
ls -la Instances/
find . -name "*.msrcp" -o -name "*.dzn" | head -5
```

#### "Modèle ML non trouvé"
```bash
# Entraîner d'abord un modèle
python3 binary_relevance_msrcpsp.py  # Option 1
```

#### Erreur de mémoire
```bash
# Tester avec moins d'instances
python3 -c "
import os
files = os.listdir('Instances')[:20]  # Premier 20 seulement
print(f'Test avec {len(files)} instances')
"
```

## 📈 Résultats attendus

### Tests automatisés
```
Tests réussis: 7/8
- ✅ Environnement Python
- ✅ Structure des fichiers  
- ✅ Imports ML
- ✅ Fonctionnalités ML
- ✅ Simulation entraînement
- ⚠️  Script exemple (peut échouer selon l'environnement)
- ✅ Parsing instances
- ✅ Intégration modèle
```

### Performance ML
```
Instances testées: 20
Prédictions réussies: 18/20 (90%)
Résolutions réussies: 15/20 (75%) 
Diversité moyenne: 4.2 algorithmes
Amélioration moyenne: 18.5%
```

### Exemples de prédictions
```
Instance: MSLIB_Set1_1
Algorithmes recommandés: ['LFT', 'EST', 'MSLF']
Meilleur algorithme: LFT
Makespan: 42
Amélioration: 15.2%
```

## 🎯 Tests par objectif

### Valider le solveur de base
```bash
# Test rapide
python3 -c "
from msrcpsp_final import MSRCPSPParser, MSRCPSPSolver
print('Solveur de base OK')
"

# Test avec instance
python3 msrcpsp_final.py
```

### Valider le ML
```bash
# Test d'extraction de features
python3 -c "
from binary_relevance_msrcpsp import InstanceFeatureExtractor
extractor = InstanceFeatureExtractor()
print('ML OK')
"

# Test complet
python3 exemple_ml.py
```

### Valider l'intégration
```bash
# Après avoir un modèle entraîné
python3 -c "
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
ml = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl')
print('Intégration OK')
"
```

## 📚 Documentation de test

### Fichiers de référence
- **`GUIDE_TEST_COMPLET.md`** : Guide détaillé complet
- **`test_automatique.py`** : Script de test automatisé
- **`exemple_ml.py`** : Exemples commentés
- **`README_ML.md`** : Documentation technique

### Commandes de référence
```bash
# Tests essentiels
python3 test_automatique.py         # Test auto complet
python3 exemple_ml.py               # Exemples simples
python3 assistant_ml.py             # Interface guidée

# Tests avancés
python3 binary_relevance_msrcpsp.py # Système ML complet
python3 demo_ml_integration.py      # Démonstrations
```

## 🏆 Validation finale

### Test de validation en une commande
```bash
python3 -c "
print('🔍 VALIDATION FINALE')
print('='*30)

# Test imports
try:
    from binary_relevance_msrcpsp import *
    print('✅ Imports ML')
except: print('❌ Imports ML')

# Test fonctionnel
try:
    extractor = InstanceFeatureExtractor()
    features = extractor.extract_all_features({
        'nActs': 3, 'nRes': 2, 'nSkills': 2,
        'dur': [1,2,1], 'sreq': [[1,0],[0,1],[1,1]], 
        'mastery': [[1,1],[0,1]], 'precedence_graph': {},
        'est': [0,1,2], 'lst': [0,1,2], 'lft': [1,3,3], 'float_dyn': [0,0,0]
    })
    print(f'✅ Features: {len(features)}')
except Exception as e: 
    print(f'❌ Features: {e}')

# Test structure
import os
files = ['msrcpsp_final.py', 'binary_relevance_msrcpsp.py', 'exemple_ml.py']
for f in files:
    print(f'{'✅' if os.path.exists(f) else '❌'} {f}')

print('\\n🎉 Validation terminée!')
"
```

---

## 🚀 Résumé des commandes essentielles

| Objectif | Commande | Temps |
|----------|----------|-------|
| **Test rapide** | `python3 test_automatique.py --quick` | 2 min |
| **Exemple simple** | `python3 exemple_ml.py` | 3 min |
| **Interface guidée** | `python3 assistant_ml.py` | 5 min |
| **Entraînement ML** | `python3 binary_relevance_msrcpsp.py` (option 1) | 10 min |
| **Test complet** | `python3 demo_ml_integration.py` | 15 min |

**🎯 Pour commencer :** `python3 assistant_ml.py` puis choisir option 1 ou 6
