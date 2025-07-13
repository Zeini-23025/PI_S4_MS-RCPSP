# 📋 Documentation du script project.sh

## 🎯 Vue d'ensemble

Le fichier `project.sh` est un script automatisé qui exécute le **flux de travail complet** du projet MS-RCPSP avec Machine Learning. Il automatise les 3 étapes principales : génération des données, entraînement ML, et résolution guidée.

## 🔄 Flux de travail automatisé

```bash
./project.sh
```

### Étape 1: Génération des données de performance
```bash
python3 msrcpsp_final.py
```
- **Objectif** : Créer la base de données d'entraînement
- **Action** : Exécute tous les algorithmes sur les instances
- **Sortie** : Fichiers de makespan dans `resultats/makespan_details/`
- **Durée** : 5-30 minutes selon le nombre d'instances

### Étape 2: Entraînement du modèle ML
```bash
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"
```
- **Objectif** : Entraîner l'Intelligence Artificielle
- **Action** : Analyse les données et crée le modèle Binary Relevance
- **Sortie** : 
  - `resultats/binary_relevance_model.pkl` (modèle entraîné)
  - `resultats/binary_relevance_metadata.json` (métadonnées)
- **Durée** : 2-10 minutes selon le dataset

### Étape 3: Résolution avec guidage ML
```bash
python3 -c "from binary_relevance_msrcpsp import MLIntegratedMSRCPSP; 
ml_system = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl'); 
result = ml_system.solve_with_ml_guidance('Instances/MSLIB_Set1_1.msrcp'); 
print(result)"
```
- **Objectif** : Démontrer l'utilisation du modèle entraîné
- **Action** : Prédit les meilleurs algorithmes et résout une instance
- **Sortie** : Résultat JSON avec makespan optimisé
- **Durée** : <30 secondes

## ✅ Prérequis avant exécution

### Vérifications essentielles
```bash
# 1. Vérifier Python et modules
python3 --version  # Python 3.7+
python3 -c "import numpy, pandas, sklearn; print('Modules OK')"

# 2. Vérifier les fichiers requis
ls -la msrcpsp_final.py binary_relevance_msrcpsp.py
ls -la Instances/ | head -5

# 3. Vérifier l'espace disque
du -sh Instances/ resultats/
```

### Modules Python requis
```bash
pip install numpy pandas scikit-learn
```

## 🚀 Modes d'exécution

### Exécution automatique complète
```bash
./project.sh
```

### Exécution étape par étape (recommandé pour debug)
```bash
# Étape 1 seulement
python3 msrcpsp_final.py

# Étape 2 seulement (nécessite Étape 1)
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"

# Étape 3 seulement (nécessite Étape 2)
python3 -c "from binary_relevance_msrcpsp import MLIntegratedMSRCPSP; ml_system = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl'); result = ml_system.solve_with_ml_guidance('Instances/MSLIB_Set1_1.msrcp'); print(result)"
```

### Alternative avec interfaces utilisateur
```bash
# Interface guidée complète
python3 assistant_ml.py

# Menu ML principal
python3 binary_relevance_msrcpsp.py
```

## 📊 Sorties attendues

### Après Étape 1 (Génération données)
```
resultats/
├── makespan_details/
│   ├── MSLIB_Set1_1_makespans.json
│   ├── MSLIB_Set1_2_makespans.json
│   └── ...
└── (autres fichiers de résultats)
```

### Après Étape 2 (Entraînement ML)
```
resultats/
├── binary_relevance_model.pkl       # Modèle ML entraîné
├── binary_relevance_metadata.json   # Performance et config
└── makespan_details/ (existant)
```

### Après Étape 3 (Résolution guidée)
```json
{
  "instance": "MSLIB_Set1_1.msrcp",
  "recommended_algorithms": ["EST", "LFT", "MSLF"],
  "best_algorithm": "EST",
  "best_makespan": 42,
  "all_results": {
    "EST": 42,
    "LFT": 45,
    "MSLF": 44
  },
  "improvement": "15% mieux que la moyenne"
}
```

## 🔧 Personnalisation du script

### Modifier l'instance de test (Étape 3)
```bash
# Remplacer MSLIB_Set1_1.msrcp par votre instance
sed -i 's/MSLIB_Set1_1.msrcp/VOTRE_INSTANCE.msrcp/g' project.sh
```

### Limiter le nombre d'instances (Étape 1)
Modifier `msrcpsp_final.py` ou utiliser :
```bash
# Créer un sous-dossier avec moins d'instances
mkdir Instances_test
cp Instances/MSLIB_Set1_[1-9].msrcp Instances_test/
```

### Changer les paramètres ML (Étape 2)
Dans `binary_relevance_msrcpsp.py`, modifier :
- Tolérance de diversité
- Nombre d'arbres Random Forest
- Méthodes de validation croisée

## 🚨 Dépannage

### Erreur: "Module msrcpsp_final non trouvé"
```bash
# Vérifier le fichier
ls -la msrcpsp_final.py

# Tester l'import
python3 -c "import msrcpsp_final; print('OK')"
```

### Erreur: "Aucune instance trouvée"
```bash
# Vérifier le répertoire Instances
find Instances/ -name "*.msrcp" | wc -l

# Créer des instances de test
mkdir -p Instances
# Copier quelques instances pour test
```

### Erreur: "Pas assez de données pour ML"
```bash
# Solution 1: Générer plus de données (Étape 1)
python3 msrcpsp_final.py

# Solution 2: Utiliser la simulation
python3 exemple_ml.py
```

### Erreur: "Modèle non trouvé" (Étape 3)
```bash
# Vérifier le modèle
ls -la resultats/binary_relevance_model.pkl

# Re-entraîner si nécessaire
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"
```

## ⏱️ Temps d'exécution estimés

| Étape | Instances | Temps estimé | Ressources |
|-------|-----------|--------------|------------|
| **Génération données** | 100 | 5 min | CPU intensif |
| **Génération données** | 1000 | 20 min | CPU intensif |
| **Génération données** | 6600 | 2h | CPU très intensif |
| **Entraînement ML** | 100 instances | 2 min | RAM (2GB) |
| **Entraînement ML** | 1000 instances | 5 min | RAM (4GB) |
| **Résolution guidée** | 1 instance | 10s | Léger |

## 🎯 Recommandations d'utilisation

### Pour tests rapides
```bash
# Limiter à 10-20 instances
mkdir Instances_test
cp Instances/MSLIB_Set1_[1-9].msrcp Instances_test/
mv Instances Instances_full
mv Instances_test Instances
./project.sh
```

### Pour évaluation complète
```bash
# Utiliser toutes les instances (long)
./project.sh 2>&1 | tee project_full.log
```

### Pour développement
```bash
# Exécuter étape par étape avec debug
python3 msrcpsp_final.py
python3 -c "from binary_relevance_msrcpsp import train_new_model; train_new_model()"
python3 assistant_ml.py  # Option 3 pour test guidé
```

## 📋 Checklist avant exécution

- [ ] **Python 3.7+** installé
- [ ] **Modules** numpy, pandas, sklearn installés
- [ ] **Fichiers** msrcpsp_final.py et binary_relevance_msrcpsp.py présents
- [ ] **Instances** dans le dossier Instances/ (au moins 5-10 fichiers)
- [ ] **Espace disque** libre (2GB+ pour grands datasets)
- [ ] **Permissions** script exécutable (`chmod +x project.sh`)

## 🏆 Résultats attendus

Après exécution complète, vous devriez avoir :
- ✅ **Base de données** de makespan générée
- ✅ **Modèle ML** entraîné et sauvegardé
- ✅ **Démonstration** de résolution guidée par IA
- ✅ **Amélioration** mesurable du makespan (10-30%)

**🎉 Votre système MS-RCPSP avec Intelligence Artificielle est prêt à optimiser automatiquement la résolution d'instances !**
