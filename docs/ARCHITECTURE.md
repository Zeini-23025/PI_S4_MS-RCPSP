# 🏗️ Architecture du Système MS-RCPSP

## 📋 Vue d'ensemble architecturale

Le système MS-RCPSP est composé de plusieurs modules interconnectés qui travaillent ensemble pour résoudre des problèmes d'ordonnancement de projets avec intelligence artificielle.

## 🧠 Architecture générale

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTÈME MS-RCPSP                         │
├─────────────────────────────────────────────────────────────┤
│  🎮 Interface Utilisateur                                   │
│  ├── assistant_ml.py (Interface simple)                     │
│  ├── demo_ml_integration.py (Démonstration)                 │
│  └── run_project.py (Lanceur automatique)                   │
├─────────────────────────────────────────────────────────────┤
│  🤖 Couche Intelligence Artificielle                        │
│  ├── binary_relevance_msrcpsp.py (Cœur ML)                  │
│  ├── Extraction de 43 caractéristiques                     │
│  ├── Modèle Binary Relevance + Random Forest               │
│  └── Recommandations algorithmiques                         │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ Moteur d'Ordonnancement                                 │
│  ├── msrcpsp_final.py (Algorithmes de base)                 │
│  ├── 7 algorithmes d'ordonnancement                         │
│  └── Gestion des ressources et compétences                  │
├─────────────────────────────────────────────────────────────┤
│  📊 Traitement et Analyse                                   │
│  ├── makespan_calculator.py (Génération données)            │
│  ├── detail_resultat_ml.py (Analyse détaillée)              │
│  └── nettoyage_et_graphiques.py (Visualisations)            │
├─────────────────────────────────────────────────────────────┤
│  💾 Stockage et Données                                     │
│  ├── Instances/ (6600+ fichiers .msrcp)                     │
│  ├── resultats/ (Modèles et données)                        │
│  ├── resultats_ml/ (Résultats JSON)                         │
│  └── resultats/graphiques/ (Visualisations PNG)             │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Modules principaux

### 1. 🎮 **Interface Utilisateur**

#### `run_project.py` - Lanceur automatique
- **Rôle** : Orchestration complète du système
- **Fonctionnalités** :
  - Vérification automatique des dépendances
  - Génération des données d'entraînement
  - Entraînement du modèle ML
  - Tests massifs et validation
  - Création des visualisations
- **Sortie** : Système complet opérationnel en ~50 secondes

#### `assistant_ml.py` - Interface simple
- **Rôle** : Interface utilisateur simplifiée
- **Fonctionnalités** :
  - Sélection de fichiers intuitive
  - Recommandations IA en temps réel
  - Résultats formatés et compréhensibles
- **Usage** : Utilisateurs débutants

#### `demo_ml_integration.py` - Démonstration
- **Rôle** : Démonstration des capacités ML
- **Fonctionnalités** :
  - Comparaison avec/sans IA
  - Analyses de performance
  - Exemples concrets
- **Usage** : Présentation et formation

### 2. 🤖 **Intelligence Artificielle**

#### `binary_relevance_msrcpsp.py` - Cœur ML
- **Algorithme** : Binary Relevance avec Random Forest
- **Caractéristiques** : 43 features extraites automatiquement
- **Performance** : 100% de succès sur les tests
- **Fonctionnalités** :
  ```python
  # Extraction de caractéristiques
  - Nombre de tâches, ressources, compétences
  - Densités et ratios
  - Statistiques de durées et charges
  - Métriques de complexité réseau
  
  # Modèle ML
  - 7 classificateurs binaires (un par algorithme)
  - Random Forest avec validation croisée
  - Prédictions multi-label
  ```

### 3. ⚙️ **Moteur d'Ordonnancement**

#### `msrcpsp_final.py` - Algorithmes de base
- **Algorithmes implémentés** :
  1. **EST** (Earliest Start Time)
  2. **LFT** (Latest Finish Time)
  3. **MSLF** (Most Skills Last First)
  4. **SPT** (Shortest Processing Time)
  5. **LPT** (Longest Processing Time)
  6. **FCFS** (First Come First Served)
  7. **LST** (Latest Start Time)

- **Gestion des contraintes** :
  - Ressources multiples avec capacités
  - Compétences requises par tâche
  - Précédences entre tâches
  - Disponibilités temporelles

### 4. 📊 **Traitement et Analyse**

#### `makespan_calculator.py` - Générateur de données
- **Rôle** : Création du dataset d'entraînement ML
- **Processus** :
  1. Lecture des instances .msrcp
  2. Exécution des 7 algorithmes
  3. Calcul des makespans
  4. Sauvegarde JSON structurée

#### `detail_resultat_ml.py` - Analyse détaillée
- **Fonctionnalités** :
  - Analyse individuelle de résultats
  - Comparaison multi-projets
  - Génération de graphiques matplotlib
  - Rapports de performance IA

#### `nettoyage_et_graphiques.py` - Visualisations
- **Graphiques générés** :
  - Performance par algorithme (barres, boxplots)
  - Taux de succès IA (secteurs)
  - Comparaisons temporelles (lignes)
  - Matrices de confusion

## 🔄 Flux de données

### 1. **Phase d'entraînement**
```
Instances .msrcp → makespan_calculator.py → Données JSON
     ↓
Extraction features → binary_relevance_msrcpsp.py → Modèle .pkl
```

### 2. **Phase d'utilisation**
```
Nouvelle instance → Extraction features → Modèle ML → Recommandations
     ↓
Algorithmes recommandés → msrcpsp_final.py → Résultats optimaux
     ↓
Sauvegarde JSON → Visualisations → Rapports
```

## 📁 Organisation des fichiers

### **Structure des données**
```
resultats/
├── binary_relevance_model.pkl     # Modèle ML entraîné (930KB)
├── makespan_details/              # Données d'entraînement
│   ├── MSLIB_Set1_*.json         # Résultats par instance
│   └── ...
└── graphiques/                    # Visualisations
    ├── analyse_makespan.png       # Performance algorithmes
    ├── analyse_ml.png             # Performance IA
    └── rapport_performance_ia.json # Métriques JSON

resultats_ml/
├── MSLIB_Set1_*_ml_results.json  # Résultats avec IA
└── ...                           # Un fichier par test
```

### **Format des résultats ML**
```json
{
  "instance": "MSLIB_Set1_4799",
  "ml_recommended_algorithms": ["EST", "LPT", "LST", "SPT"],
  "best_algorithm": "EST",
  "best_makespan": 143.0,
  "all_results": {
    "EST": {"makespan": 143.0, "computation_time": 0.05},
    "LPT": {"makespan": 143.0, "computation_time": 0.03},
    ...
  },
  "features_used": 43,
  "confidence_scores": {...}
}
```

## 🔧 Points d'extension

### **Nouveaux algorithmes**
1. Ajouter dans `msrcpsp_final.py`
2. Mettre à jour `binary_relevance_msrcpsp.py`
3. Régénérer les données d'entraînement

### **Nouvelles caractéristiques**
1. Modifier `extract_features()` dans le module ML
2. Réentraîner le modèle
3. Valider les performances

### **Nouvelles visualisations**
1. Étendre `nettoyage_et_graphiques.py`
2. Ajouter dans `detail_resultat_ml.py`
3. Intégrer aux rapports automatiques

## 🎯 Avantages architecturaux

### **Modularité**
- Chaque module a une responsabilité claire
- Interfaces bien définies
- Facilité de maintenance et d'extension

### **Scalabilité**
- Traitement par lots efficace
- Parallélisation possible
- Gestion mémoire optimisée

### **Robustesse**
- Gestion d'erreurs à tous les niveaux
- Validation automatique des données
- Tests intégrés et diagnostics

### **Utilisabilité**
- Interfaces multiples selon les besoins
- Documentation intégrée
- Feedback utilisateur en temps réel
