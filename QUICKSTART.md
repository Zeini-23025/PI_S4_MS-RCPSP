# 🚀 Démarrage Rapide - MSRCPSP Solver

## ⚡ En 3 étapes

### 1. Vérifiez vos données
```bash
ls Instances/*.msrcp | wc -l
# Doit afficher le nombre de vos fichiers .msrcp
```

### 2. Choisissez votre mode
```bash
# Mode recommandé - Menu complet
python3 msrcpsp_complete.py

# Mode rapide - 10 instances
python3 msrcpsp_final.py

# Mode apprentissage
python3 demo.py
```

### 3. Consultez les résultats
```bash
ls resultats/
# Fichiers générés :
# - test_comparison.csv      (tableau comparatif)
# - detailed_results.json    (résultats détaillés)
```

## 📊 Exemple de sortie

```
📊 Traitement de MSLIB_Set1_1...
  ✓ EST: 36
  ✓ LFT: 40  
  ✓ MSLF: 35  ← Meilleur
  ✓ SPT: 36
```

## 🎯 Algorithmes disponibles

- **EST** : Commence dès que possible
- **LFT** : Priorise par échéance
- **MSLF** : Priorise les tâches critiques ⭐
- **SPT** : Fait les tâches courtes d'abord

**MSLF** et **LFT** sont généralement les plus performants !

---
**Prêt ? Lancez `python3 msrcpsp_complete.py` !** 🚀
