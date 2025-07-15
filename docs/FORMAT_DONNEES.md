# 📊 Format des Données

## 📋 Vue d'ensemble

Le système MS-RCPSP utilise plusieurs formats de données pour les instances d'entrée, les résultats intermédiaires et les sorties finales. Cette documentation détaille tous les formats utilisés.

## 📁 Format des instances d'entrée (.msrcp)

### **Structure générale**
Les fichiers d'instances suivent le format standard **MSRCPSP** (Multi-Skill Resource-Constrained Project Scheduling Problem).

### **Exemple de fichier MSLIB_Set1_4799.msrcp**
```
ProjectID: MSLIB_Set1_4799
Jobs: 30
Resources: 8
Skills: 10
Horizon: 200

PRECEDENCE RELATIONS:
1 2
2 3 5
3 4
5 6
...

RESOURCE AVAILABILITY:
R1 4 S1 S3 S7
R2 3 S2 S5
R3 2 S1 S4 S8
...

JOB DETAILS:
J1 0 0 0
J2 5 2 S1:2 S3:1
J3 8 1 S2:1
...
```

### **Section par section**

#### **En-tête du projet**
```
ProjectID: MSLIB_Set1_4799    # Identifiant unique
Jobs: 30                      # Nombre de tâches
Resources: 8                  # Nombre de ressources
Skills: 10                    # Nombre de compétences
Horizon: 200                  # Horizon de planification (optionnel)
```

#### **Relations de précédence**
```
PRECEDENCE RELATIONS:
1 2        # La tâche 1 doit être terminée avant la tâche 2
2 3 5      # La tâche 2 doit être terminée avant les tâches 3 et 5
3 4        # La tâche 3 doit être terminée avant la tâche 4
```

**Format** : `tâche_prédécesseur tâche_successeur1 [tâche_successeur2 ...]`

#### **Disponibilité des ressources**
```
RESOURCE AVAILABILITY:
R1 4 S1 S3 S7    # Ressource R1, capacité 4, compétences S1, S3, S7
R2 3 S2 S5       # Ressource R2, capacité 3, compétences S2, S5
R3 2 S1 S4 S8    # Ressource R3, capacité 2, compétences S1, S4, S8
```

**Format** : `ressource_id capacité compétence1 [compétence2 ...]`

#### **Détails des tâches**
```
JOB DETAILS:
J1 0 0 0              # Tâche J1, durée 0 (tâche fictive de début)
J2 5 2 S1:2 S3:1      # Tâche J2, durée 5, 2 modes, besoins S1:2 et S3:1
J3 8 1 S2:1           # Tâche J3, durée 8, 1 mode, besoin S2:1
```

**Format** : `tâche_id durée nombre_modes compétence1:quantité [compétence2:quantité ...]`

## 📊 Format des résultats makespan

### **Fichier JSON de résultats détaillés**
**Chemin** : `resultats/makespan_details/MSLIB_Set1_*.json`

```json
{
  "instance": "MSLIB_Set1_4799",
  "timestamp": "2025-07-15T14:10:32",
  "algorithms_tested": ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"],
  "results": {
    "EST": {
      "makespan": 143.0,
      "computation_time": 0.052,
      "schedule": [
        {"job": "J1", "start": 0, "end": 0, "resources": []},
        {"job": "J2", "start": 0, "end": 5, "resources": ["R1", "R3"]},
        {"job": "J3", "start": 5, "end": 13, "resources": ["R2"]}
      ],
      "resource_utilization": 0.73,
      "critical_path": ["J1", "J2", "J5", "J8", "J12"],
      "success": true
    },
    "LFT": {
      "makespan": 149.0,
      "computation_time": 0.048,
      "schedule": [...],
      "resource_utilization": 0.69,
      "critical_path": [...],
      "success": true
    }
  },
  "best_algorithm": "EST",
  "best_makespan": 143.0,
  "statistics": {
    "makespan_range": 6.0,
    "algorithms_optimal": ["EST", "LPT", "LST", "SPT"],
    "worst_algorithm": "LFT",
    "improvement_potential": 4.0
  }
}
```

### **Structure détaillée**

#### **Métadonnées**
```json
{
  "instance": "MSLIB_Set1_4799",           # Nom de l'instance
  "timestamp": "2025-07-15T14:10:32",      # Date/heure de traitement
  "algorithms_tested": ["EST", "LFT", ...] # Liste des algorithmes testés
}
```

#### **Résultats par algorithme**
```json
"EST": {
  "makespan": 143.0,                      # Durée totale du projet
  "computation_time": 0.052,              # Temps de calcul (secondes)
  "schedule": [...],                      # Planning détaillé (optionnel)
  "resource_utilization": 0.73,          # Taux d'utilisation des ressources
  "critical_path": ["J1", "J2", ...],    # Chemin critique (optionnel)
  "success": true                         # Succès de l'ordonnancement
}
```

#### **Statistiques globales**
```json
"statistics": {
  "makespan_range": 6.0,                 # Écart min-max
  "algorithms_optimal": ["EST", "LPT"],  # Algorithmes à l'optimal
  "worst_algorithm": "LFT",              # Pire algorithme
  "improvement_potential": 4.0           # Amélioration possible (%)
}
```

## 🤖 Format des résultats ML

### **Fichier JSON de résultats ML**
**Chemin** : `resultats_ml/MSLIB_Set1_*_ml_results.json`

```json
{
  "instance": "MSLIB_Set1_4799",
  "timestamp": "2025-07-15T14:11:15",
  "ml_model_version": "binary_relevance_v1.0",
  "features_used": 43,
  "ml_recommended_algorithms": ["EST", "LPT", "LST", "SPT", "FCFS"],
  "confidence_scores": {
    "EST": 0.87,
    "LPT": 0.91,
    "LST": 0.83,
    "SPT": 0.76,
    "FCFS": 0.72,
    "LFT": 0.34,
    "MSLF": 0.28
  },
  "all_results": {
    "EST": {
      "makespan": 143.0,
      "computation_time": 0.052,
      "predicted": true,
      "rank": 1
    },
    "LPT": {
      "makespan": 143.0,
      "computation_time": 0.031,
      "predicted": true,
      "rank": 1
    },
    "LST": {
      "makespan": 143.0,
      "computation_time": 0.043,
      "predicted": true,
      "rank": 1
    },
    "SPT": {
      "makespan": 143.0,
      "computation_time": 0.034,
      "predicted": true,
      "rank": 1
    },
    "FCFS": {
      "makespan": 149.0,
      "computation_time": 0.022,
      "predicted": true,
      "rank": 5
    },
    "LFT": {
      "makespan": 149.0,
      "computation_time": 0.048,
      "predicted": false,
      "rank": 5
    },
    "MSLF": {
      "makespan": 149.0,
      "computation_time": 0.041,
      "predicted": false,
      "rank": 5
    }
  },
  "best_algorithm": "EST",
  "best_makespan": 143.0,
  "ml_accuracy": true,
  "ml_performance": {
    "algorithms_recommended": 5,
    "algorithms_tested": 7,
    "optimal_in_recommended": true,
    "recommendation_precision": 0.80,
    "improvement_vs_random": 23.4
  },
  "extracted_features": {
    "num_jobs": 30,
    "num_resources": 8,
    "num_skills": 10,
    "avg_duration": 7.3,
    "skill_density": 0.67,
    "resource_utilization": 0.73,
    "network_density": 0.15,
    "complexity_ratio": 2.34
  }
}
```

### **Structure détaillée ML**

#### **Informations du modèle**
```json
{
  "ml_model_version": "binary_relevance_v1.0",  # Version du modèle
  "features_used": 43,                          # Nombre de caractéristiques
  "timestamp": "2025-07-15T14:11:15"            # Date/heure de prédiction
}
```

#### **Recommandations IA**
```json
{
  "ml_recommended_algorithms": ["EST", "LPT", "LST", "SPT", "FCFS"],
  "confidence_scores": {
    "EST": 0.87,     # Score de confiance (0-1)
    "LPT": 0.91,     # Plus élevé = plus confiant
    "LST": 0.83,
    "SPT": 0.76,
    "FCFS": 0.72,
    "LFT": 0.34,     # Non recommandé (score < seuil)
    "MSLF": 0.28     # Non recommandé
  }
}
```

#### **Performance ML**
```json
"ml_performance": {
  "algorithms_recommended": 5,              # Nombre d'algorithmes recommandés
  "algorithms_tested": 7,                   # Nombre total d'algorithmes
  "optimal_in_recommended": true,           # L'optimal était-il recommandé ?
  "recommendation_precision": 0.80,         # Précision des recommandations
  "improvement_vs_random": 23.4             # Amélioration vs sélection aléatoire
}
```

#### **Caractéristiques extraites (échantillon)**
```json
"extracted_features": {
  "num_jobs": 30,                 # Nombre de tâches
  "num_resources": 8,             # Nombre de ressources
  "num_skills": 10,               # Nombre de compétences
  "avg_duration": 7.3,            # Durée moyenne des tâches
  "skill_density": 0.67,          # Densité des compétences
  "resource_utilization": 0.73,   # Utilisation des ressources
  "network_density": 0.15,        # Densité du réseau de précédences
  "complexity_ratio": 2.34        # Ratio de complexité
}
```

## 📈 Format des rapports de performance

### **Rapport JSON global**
**Chemin** : `resultats/graphiques/rapport_performance_ia.json`

```json
{
  "generation_date": "2025-07-15T14:12:00",
  "system_version": "MS-RCPSP v2.0",
  "dataset_info": {
    "total_instances": 20,
    "instances_tested": 5,
    "training_instances": 14,
    "validation_instances": 6
  },
  "ml_performance": {
    "global_accuracy": 100.0,
    "average_precision": 88.9,
    "average_recall": 80.0,
    "average_f1_score": 83.2,
    "hamming_loss": 16.7
  },
  "algorithm_statistics": {
    "most_often_optimal": {
      "LPT": 40.0,
      "LST": 40.0,
      "EST": 20.0
    },
    "most_often_recommended": {
      "EST": 100.0,
      "LPT": 80.0,
      "LST": 80.0,
      "SPT": 60.0,
      "FCFS": 40.0,
      "LFT": 20.0,
      "MSLF": 0.0
    },
    "average_makespans": {
      "EST": 89.2,
      "LFT": 90.3,
      "MSLF": 90.8,
      "SPT": 89.8,
      "LPT": 88.7,
      "FCFS": 91.1,
      "LST": 89.1
    }
  },
  "performance_metrics": {
    "average_improvement": 3.6,
    "max_improvement": 7.2,
    "min_improvement": 0.0,
    "instances_with_improvement": 4,
    "average_execution_time": 0.041
  }
}
```

## 🔧 Format de configuration du modèle

### **Métadonnées du modèle ML**
**Inclus dans** : `resultats/binary_relevance_model.pkl`

```python
# Structure interne du modèle (Python pickle)
{
    'classifiers': {
        'EST': RandomForestClassifier(...),
        'LFT': RandomForestClassifier(...),
        'MSLF': RandomForestClassifier(...),
        'SPT': RandomForestClassifier(...),
        'LPT': RandomForestClassifier(...),
        'FCFS': RandomForestClassifier(...),
        'LST': RandomForestClassifier(...)
    },
    'feature_names': [
        'num_jobs', 'num_resources', 'num_skills',
        'total_duration', 'avg_duration', 'min_duration',
        # ... 37 autres caractéristiques
    ],
    'algorithm_names': ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST'],
    'training_metadata': {
        'training_date': '2025-07-15T14:10:45',
        'training_instances': 14,
        'validation_instances': 6,
        'tolerance': 0.1,
        'cross_validation_folds': 5,
        'random_state': 42
    },
    'performance_metrics': {
        'cross_val_accuracy': {
            'EST': 0.933, 'LFT': 0.733, 'MSLF': 0.800,
            'SPT': 0.783, 'LPT': 0.867, 'FCFS': 0.800,
            'LST': 0.917
        },
        'feature_importance': {
            'num_jobs': 0.123,
            'resource_utilization': 0.118,
            'skill_density': 0.102,
            # ... autres importances
        }
    }
}
```

## 📊 Format des exports CSV

### **Export des résultats pour analyse**
```python
# Code pour générer CSV
import pandas as pd
import json

# Charger les résultats ML
results = []
for file in os.listdir('resultats_ml/'):
    with open(f'resultats_ml/{file}') as f:
        data = json.load(f)
        results.append(data)

# Convertir en DataFrame
df = pd.DataFrame(results)
df.to_csv('results_export.csv', index=False)
```

### **Structure CSV résultante**
```csv
instance,best_algorithm,best_makespan,ml_accuracy,algorithms_recommended,confidence_avg
MSLIB_Set1_4799,EST,143.0,true,5,0.758
MSLIB_Set1_5060,LST,115.0,true,5,0.812
MSLIB_Set1_4109,LPT,143.0,true,5,0.734
...
```

## 🎯 Validation des formats

### **Schémas de validation JSON**

#### **Validation résultat ML**
```python
ML_RESULT_SCHEMA = {
    "type": "object",
    "required": ["instance", "ml_recommended_algorithms", "best_algorithm", "best_makespan"],
    "properties": {
        "instance": {"type": "string"},
        "ml_recommended_algorithms": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "best_algorithm": {"type": "string"},
        "best_makespan": {"type": "number", "minimum": 0},
        "all_results": {
            "type": "object",
            "patternProperties": {
                "^(EST|LFT|MSLF|SPT|LPT|FCFS|LST)$": {
                    "type": "object",
                    "required": ["makespan"],
                    "properties": {
                        "makespan": {"type": "number", "minimum": 0},
                        "computation_time": {"type": "number", "minimum": 0}
                    }
                }
            }
        }
    }
}
```

### **Fonctions de validation**
```python
import jsonschema

def validate_ml_result(data):
    """Valide un résultat ML contre le schéma"""
    try:
        jsonschema.validate(data, ML_RESULT_SCHEMA)
        return True, "Valide"
    except jsonschema.ValidationError as e:
        return False, str(e)

def validate_makespan_result(data):
    """Valide un résultat de makespan"""
    required_fields = ['instance', 'results', 'best_algorithm', 'best_makespan']
    
    for field in required_fields:
        if field not in data:
            return False, f"Champ manquant: {field}"
    
    if data['best_makespan'] <= 0:
        return False, "Makespan invalide"
    
    return True, "Valide"
```

## 📁 Organisation des fichiers de données

### **Structure complète des données**
```
📁 MS-RCPSP/
├── 📁 Instances/                           # Instances d'entrée
│   ├── 📄 MSLIB_Set1_*.msrcp              # Format MSRCPSP standard
│   └── ...                                # 6600+ fichiers
├── 📁 resultats/                          # Résultats et modèles
│   ├── 📄 binary_relevance_model.pkl      # Modèle ML (930KB)
│   ├── 📁 makespan_details/               # Données d'entraînement
│   │   ├── 📄 MSLIB_Set1_*_results.json   # Résultats makespan détaillés
│   │   └── ...
│   └── 📁 graphiques/                     # Visualisations
│       ├── 📄 analyse_makespan.png        # Graphiques makespans
│       ├── 📄 analyse_ml.png              # Graphiques ML
│       ├── 📄 tendances_makespan.png      # Évolutions
│       ├── 📄 comparaison_ml.png          # Comparaisons
│       ├── 📄 detail_*.png                # Analyses individuelles
│       └── 📄 rapport_performance_ia.json # Rapport JSON
├── 📁 resultats_ml/                       # Résultats avec IA
│   ├── 📄 MSLIB_Set1_*_ml_results.json    # Résultats ML par instance
│   └── ...
└── 📁 docs/                               # Documentation
    └── 📄 FORMAT_DONNEES.md               # Ce fichier
```

### **Tailles typiques des fichiers**
```
Instance .msrcp              : 1-10 KB
Résultat makespan .json      : 2-5 KB
Résultat ML .json           : 3-8 KB
Modèle ML .pkl              : 930 KB
Graphique .png              : 250-500 KB
Rapport performance .json    : < 1 KB
```
