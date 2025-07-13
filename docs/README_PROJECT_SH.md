# 🚀 Script project.sh - Automatisation complète

## Vue d'ensemble
Le script `project.sh` automatise entièrement votre projet MS-RCPSP avec Machine Learning en 3 étapes séquentielles.

## Exécution simple
```bash
chmod +x project.sh
./project.sh
```

## Ce que fait le script

### ✅ 1. Vérifications préalables
- Python 3.7+ installé
- Modules numpy, pandas, sklearn disponibles  
- Fichiers msrcpsp_final.py et binary_relevance_msrcpsp.py présents
- Instances disponibles dans Instances/

### ⚙️ 2. Étape 1 - Génération des données (5-30 min)
```bash
python3 msrcpsp_final.py
```
- Exécute tous les algorithmes sur toutes les instances
- Crée les fichiers makespan dans `resultats/makespan_details/`
- Génère la base de données pour l'entraînement ML

### 🧠 3. Étape 2 - Entraînement ML (2-10 min)
```bash
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"
```
- Analyse les données de makespan générées
- Extrait 43 caractéristiques par instance
- Entraîne le modèle Binary Relevance avec Random Forest
- Sauvegarde le modèle dans `resultats/binary_relevance_model.pkl`

### 🎯 4. Étape 3 - Résolution guidée (<30s)
```bash
# Code complexe intégré dans le script
```
- Charge le modèle ML entraîné
- Trouve automatiquement une instance de test
- Prédit les 3-7 meilleurs algorithmes  
- Résout l'instance et affiche les résultats optimisés

## Sorties du script

### Fichiers créés
```
resultats/
├── binary_relevance_model.pkl          # Modèle ML entraîné
├── binary_relevance_metadata.json      # Performance du modèle
└── makespan_details/                   # Données d'entraînement
    ├── MSLIB_Set1_1_makespans.json
    └── ...
```

### Affichage final
```
📊 RÉSULTATS DE LA RÉSOLUTION GUIDÉE PAR IA :
============================================================
Instance : Instances/MSLIB_Set1_1.msrcp
Algorithmes recommandés : ['EST', 'LFT', 'MSLF']
Meilleur algorithme : EST
Meilleur makespan : 42

Détail des résultats :
  🏆 EST: 42
     LFT: 45
     MSLF: 44

Amélioration : 15% mieux que la moyenne
============================================================
```

## Résolution de problèmes

### Si le script s'arrête à l'Étape 1
```bash
# Vérifier les instances
ls -la Instances/
find Instances/ -name "*.msrcp" | wc -l

# Tester le solveur manuellement
python3 msrcpsp_final.py
```

### Si l'entraînement ML échoue (Étape 2)
```bash
# Vérifier les données générées
ls -la resultats/makespan_details/

# Utiliser la simulation ML à la place
python3 exemple_ml.py
```

### Si la résolution guidée échoue (Étape 3)
```bash
# Vérifier le modèle
ls -la resultats/binary_relevance_model.pkl

# Tester manuellement
python3 assistant_ml.py  # Option 3
```

## Personnalisation

### Limiter le nombre d'instances (plus rapide)
```bash
# Sauvegarder toutes les instances
mv Instances Instances_full

# Créer un sous-ensemble de test
mkdir Instances
cp Instances_full/MSLIB_Set1_[1-9].msrcp Instances/

# Exécuter le script
./project.sh

# Restaurer toutes les instances
mv Instances_full Instances
```

### Modifier l'instance de test
Éditer le script et changer :
```bash
test_instance="Instances/VOTRE_INSTANCE.msrcp"
```

## Temps d'exécution

| Nombre d'instances | Étape 1 | Étape 2 | Étape 3 | Total |
|-------------------|---------|---------|---------|-------|
| 10 instances      | 2 min   | 1 min   | 10s     | 3 min |
| 100 instances     | 10 min  | 3 min   | 10s     | 13 min |
| 1000 instances    | 45 min  | 8 min   | 10s     | 53 min |

## Alternatives

Si le script automatique pose des problèmes, utilisez les interfaces manuelles :

```bash
# Interface guidée complète
python3 assistant_ml.py

# Menu ML principal  
python3 binary_relevance_msrcpsp.py

# Tests automatisés
python3 test_automatique.py
```

## Validation

Après exécution du script, validez avec :
```bash
python3 test_automatique.py --quick
```

**Le script project.sh vous donne un système MS-RCPSP avec Intelligence Artificielle entièrement fonctionnel en une seule commande !** 🎉
