# 💻 Guide d'Utilisation MS-RCPSP

## 🚀 Démarrage ultra-rapide

### **Option 1 : Tout automatique (Recommandé)**
```bash
python3 run_project.py
```
**Résultat** : Système complet opérationnel en ~50 secondes

### **Option 2 : Interface simple**
```bash
python3 assistant_ml.py
```
**Résultat** : Interface guidée pour tester vos projets

## 📋 Utilisation détaillée

### 🎮 **Interfaces disponibles**

#### 1. **`run_project.py` - Lanceur automatique**
```bash
python3 run_project.py
```

**Ce qui se passe** :
1. ✅ Vérification des dépendances Python
2. ✅ Génération des données d'entraînement (20 instances)
3. ✅ Entraînement du modèle IA 
4. ✅ Tests sur 5 projets représentatifs
5. ✅ Création des graphiques d'analyse
6. ✅ Rapport final complet

**Sortie attendue** :
```
🎉 FÉLICITATIONS ! PROJET 100% OPÉRATIONNEL ! 🎉
✅ Étapes réussies: 6/6
📊 Taux de succès: 100.0%
```

#### 2. **`assistant_ml.py` - Interface simple**
```bash
python3 assistant_ml.py
```

**Menu interactif** :
```
🤖 ASSISTANT MS-RCPSP avec IA
1. 📋 Analyser un fichier spécifique
2. 🎲 Analyser un fichier aléatoire  
3. 📊 Voir les statistiques du modèle
4. ❌ Quitter

Votre choix (1-4):
```

**Exemple d'utilisation** :
```
Choix 1 → Saisir le nom du fichier
Choix 2 → Test automatique sur fichier aléatoire
Résultat : Recommandations IA + résultats optimaux
```

#### 3. **`demo_ml_integration.py` - Démonstration complète**
```bash
python3 demo_ml_integration.py
```

**Fonctionnalités** :
- Comparaison avec/sans IA
- Analyse détaillée des performances
- Exemples concrets avec explications
- Validation sur plusieurs instances

#### 4. **`detail_resultat_ml.py` - Analyse avancée**
```bash
python3 detail_resultat_ml.py
```

**Options** :
```
1️⃣  Analyser un résultat spécifique avec graphiques
2️⃣  Comparer plusieurs résultats avec graphiques
```

**Graphiques générés** :
- Performance par algorithme
- Comparaisons IA vs optimal
- Analyses détaillées avec matplotlib

### 🎯 **Scripts spécialisés**

#### **Génération de données** 
```bash
python3 makespan_calculator.py
```
- Traite les instances dans `./Instances/`
- Génère les résultats dans `./resultats/makespan_details/`
- Teste les 7 algorithmes sur chaque instance

#### **Entraînement ML manuel**
```bash
python3 binary_relevance_msrcpsp.py
```

**Menu** :
```
1. Entraîner un nouveau modèle ML
2. Utiliser le modèle ML pour résoudre des instances  
3. Démonstration de l'intégration ML
4. Traitement en lot avec ML
```

#### **Tests massifs**
```bash
python3 solution_finale.py
```
- Diagnostic complet du système
- Tests sur 5 projets représentatifs
- Validation des performances IA
- Génération des rapports

#### **Visualisations**
```bash
python3 nettoyage_et_graphiques.py
```

**Options** :
```
1. 🧹 Supprimer fichiers non nécessaires
2. 📊 Créer graphiques makespan
3. 🤖 Créer graphiques ML  
4. 🎯 Tout faire (recommandé)
```

## 📁 Gestion des fichiers

### **Structure des entrées**
```
Instances/
├── MSLIB_Set1_*.msrcp    # 6600+ instances de test
└── ...                  # Format MSRCPSP standard
```

### **Structure des sorties**
```
resultats/
├── binary_relevance_model.pkl      # Modèle IA (~930KB)
├── makespan_details/               # Données d'entraînement
│   ├── MSLIB_Set1_*_results.json   # Résultats par instance
│   └── ...
└── graphiques/                     # Visualisations PNG
    ├── analyse_makespan.png        # Performance algorithmes
    ├── analyse_ml.png              # Performance IA
    ├── tendances_makespan.png      # Évolutions
    └── rapport_performance_ia.json # Métriques JSON

resultats_ml/
├── MSLIB_Set1_*_ml_results.json   # Résultats avec IA
└── ...                            # Un fichier par test
```

## 🎯 Cas d'usage typiques

### **Cas 1 : Nouveau utilisateur**
```bash
# 1. Premier lancement
python3 run_project.py

# 2. Test d'un projet spécifique
python3 assistant_ml.py
# → Choisir option 1
# → Saisir nom du fichier (ex: MSLIB_Set1_4799.msrcp)

# 3. Voir les résultats
ls resultats_ml/
cat resultats_ml/MSLIB_Set1_4799_ml_results.json
```

### **Cas 2 : Analyse de performance**
```bash
# 1. Analyser avec graphiques détaillés
python3 detail_resultat_ml.py
# → Choisir option 1 pour analyse individuelle
# → Choisir option 2 pour comparaison multiple

# 2. Créer visualisations complètes
python3 nettoyage_et_graphiques.py
# → Choisir option 4 (tout faire)

# 3. Consulter les graphiques
open resultats/graphiques/analyse_ml.png
open resultats/graphiques/analyse_makespan.png
```

### **Cas 3 : Développement et recherche**
```bash
# 1. Générer nouvelles données
python3 makespan_calculator.py

# 2. Réentraîner le modèle
python3 binary_relevance_msrcpsp.py
# → Choisir option 1

# 3. Valider les performances
python3 solution_finale.py

# 4. Tests massifs
python3 test_massif_projets.py  # Si disponible
```

### **Cas 4 : Traitement par lots**
```bash
# 1. Traitement automatique de toutes les instances
python3 binary_relevance_msrcpsp.py
# → Choisir option 4 (traitement en lot)

# 2. Analyse comparative complète
python3 detail_resultat_ml.py
# → Choisir option 2 (comparaison multiple)
```

## 📊 Interprétation des résultats

### **Format de sortie standard**
```json
{
  "instance": "MSLIB_Set1_4799",
  "ml_recommended_algorithms": ["EST", "LPT", "LST", "SPT"],
  "best_algorithm": "EST", 
  "best_makespan": 143.0,
  "all_results": {
    "EST": {"makespan": 143.0, "computation_time": 0.05},
    "LPT": {"makespan": 143.0, "computation_time": 0.03},
    "LST": {"makespan": 143.0, "computation_time": 0.04},
    "SPT": {"makespan": 143.0, "computation_time": 0.03},
    "FCFS": {"makespan": 149.0, "computation_time": 0.02}
  },
  "features_used": 43,
  "ai_accuracy": true
}
```

### **Indicateurs de performance**

#### **Réussite IA**
```
✅ IA correcte  : L'algorithme optimal était dans les recommandations
❌ IA incorrecte : L'algorithme optimal n'était pas recommandé
```

#### **Qualité des recommandations**
```
1-2 algorithmes recommandés : IA très sélective
3-4 algorithmes recommandés : IA équilibrée  
5+ algorithmes recommandés : IA très confiante (ou incertaine)
```

#### **Performance relative**
```
Écart 0% : Optimal trouvé
Écart 1-5% : Très bon résultat
Écart 5-10% : Résultat acceptable
Écart >10% : Résultat sous-optimal
```

### **Codes de sortie des scripts**

#### **run_project.py**
```
Code 0 : Succès complet (6/6 étapes)
Code 1 : Échec partiel ou erreur critique
```

#### **assistant_ml.py**
```
Affichage normal : Succès
"Erreur" dans sortie : Problème identifié
```

## 🔧 Résolution de problèmes

### **Problèmes courants**

#### **1. Modèle non trouvé**
```
Erreur : "❌ Modèle non trouvé !"
Solution : 
  python3 run_project.py
  # OU
  python3 binary_relevance_msrcpsp.py (option 1)
```

#### **2. Dossier vide**
```
Erreur : "❌ Dossier resultats_ml vide"
Solution :
  python3 solution_finale.py
  # OU
  python3 assistant_ml.py (faire quelques tests)
```

#### **3. Dépendances manquantes**
```
Erreur : "ImportError: No module named 'sklearn'"
Solution :
  pip install scikit-learn matplotlib pandas seaborn numpy
  # OU lancer run_project.py qui installe automatiquement
```

#### **4. Fichier instance non trouvé**
```
Erreur : "FileNotFoundError: MSLIB_Set1_XXXX.msrcp"
Solution :
  ls Instances/  # Vérifier les fichiers disponibles
  # Utiliser un nom de fichier existant
```

#### **5. Graphiques non générés**
```
Erreur : "❌ Impossible de créer les graphiques"
Solution :
  pip install matplotlib seaborn
  python3 nettoyage_et_graphiques.py
```

### **Diagnostic automatique**
```bash
# Script de diagnostic complet
python3 solution_finale.py

# Vérifications effectuées :
# ✅ Modèle ML disponible et chargeable
# ✅ Dossiers créés correctement  
# ✅ Tests sur instances représentatives
# ✅ Validation des performances IA
```

### **Logs et débogage**

#### **Activer le mode verbose**
```python
# Dans les scripts, ajouter :
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Vérifier les tailles de fichiers**
```bash
# Modèle IA (doit faire ~930KB)
ls -lh resultats/binary_relevance_model.pkl

# Résultats ML (un fichier par test)  
ls -lh resultats_ml/

# Graphiques (plusieurs MB)
ls -lh resultats/graphiques/
```

## 📈 Optimisation des performances

### **Accélération du traitement**
```bash
# Traitement parallèle (si supporté)
export PYTHONHASHSEED=0
python3 -c "import multiprocessing; print(multiprocessing.cpu_count())"

# Réduction du dataset pour tests rapides
# Modifier MAX_INSTANCES dans makespan_calculator.py
```

### **Gestion mémoire**
```python
# Pour de gros volumes de données
import gc
gc.collect()  # Forcer le garbage collection

# Traitement par lots
for batch in split_instances_in_batches(instances, batch_size=10):
    process_batch(batch)
    gc.collect()
```

### **Optimisation du modèle ML**
```python
# Réglage des hyperparamètres
n_estimators = 50   # Au lieu de 100 pour plus rapide
max_depth = 10      # Limiter la profondeur des arbres
```

## 🎯 Utilisation avancée

### **Personnalisation des seuils**
```python
# Dans binary_relevance_msrcpsp.py, modifier :
TOLERANCE = 0.1  # Tolérance pour labels (0.1% par défaut)
```

### **Ajout de nouvelles instances**
```bash
# Copier vos fichiers .msrcp dans Instances/
cp mon_projet.msrcp Instances/

# Régénérer les données
python3 makespan_calculator.py

# Réentraîner le modèle
python3 binary_relevance_msrcpsp.py (option 1)
```

### **Export des résultats**
```python
# Convertir JSON en CSV
import pandas as pd
import json

with open('resultats_ml/results.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.to_csv('results.csv', index=False)
```

### **Intégration dans d'autres systèmes**
```python
# API simple pour intégration
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP

# Initialiser
ml_solver = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl')

# Résoudre
result = ml_solver.solve_with_ml_guidance('mon_projet.msrcp', './resultats_ml/')

# Utiliser le résultat
best_makespan = result['best_makespan']
recommended_algos = result['ml_recommended_algorithms']
```
