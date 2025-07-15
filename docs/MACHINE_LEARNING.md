# 🤖 Guide du Machine Learning

## 📋 Vue d'ensemble

Le système MS-RCPSP utilise une approche de **Machine Learning multi-label** pour recommander automatiquement les meilleurs algorithmes d'ordonnancement pour chaque instance de projet.

## 🧠 Approche Binary Relevance

### **Principe**
Au lieu de prédire un seul algorithme optimal, le système :
1. **Prédit pour chaque algorithme** s'il est "bon" ou "mauvais"
2. **Recommande plusieurs algorithmes** simultanément
3. **Augmente les chances** de trouver l'optimal

### **Architecture ML**
```
Instance de projet
     ↓
Extraction de 43 caractéristiques
     ↓
7 Classificateurs binaires (Random Forest)
├── EST Classifier  → EST recommandé ? (Oui/Non)
├── LFT Classifier  → LFT recommandé ? (Oui/Non)
├── MSLF Classifier → MSLF recommandé ? (Oui/Non)
├── SPT Classifier  → SPT recommandé ? (Oui/Non)
├── LPT Classifier  → LPT recommandé ? (Oui/Non)
├── FCFS Classifier → FCFS recommandé ? (Oui/Non)
└── LST Classifier  → LST recommandé ? (Oui/Non)
     ↓
Liste d'algorithmes recommandés
```

## 📊 Extraction des caractéristiques

### **43 caractéristiques extraites**

#### 1. **Caractéristiques de base (7)**
```python
- num_jobs          # Nombre de tâches
- num_resources     # Nombre de ressources  
- num_skills        # Nombre de compétences
- total_duration    # Durée totale des tâches
- avg_duration      # Durée moyenne
- min_duration      # Durée minimale
- max_duration      # Durée maximale
```

#### 2. **Densités et ratios (8)**
```python
- skill_density           # Compétences par tâche
- resource_utilization    # Utilisation des ressources
- skills_per_resource     # Compétences par ressource
- resources_per_job       # Ressources par tâche
- job_resource_ratio      # Ratio tâches/ressources
- skill_resource_ratio    # Ratio compétences/ressources
- complexity_ratio        # Complexité générale
- network_density         # Densité du réseau de précédences
```

#### 3. **Statistiques avancées (12)**
```python
- duration_std, duration_variance  # Variabilité des durées
- workload_balance                 # Équilibrage des charges
- resource_contention             # Concurrence ressources
- skill_requirement_intensity     # Intensité compétences
- precedence_complexity          # Complexité précédences
- ... et autres métriques
```

#### 4. **Métriques de réseau (8)**
```python
- precedence_density    # Densité des précédences
- critical_path_length  # Longueur chemin critique
- parallelism_degree   # Degré de parallélisme
- bottleneck_intensity # Intensité goulots d'étranglement
- ... et autres
```

#### 5. **Caractéristiques de charge (8)**
```python
- peak_resource_demand     # Pic de demande ressource
- average_resource_load    # Charge moyenne
- resource_load_variance   # Variance de charge
- temporal_distribution    # Distribution temporelle
- ... et autres
```

### **Code d'extraction**
```python
def extract_features(instance_path):
    """Extrait 43 caractéristiques d'une instance"""
    
    # Chargement de l'instance
    jobs, resources, precedences = parse_instance(instance_path)
    
    # Caractéristiques de base
    features = {
        'num_jobs': len(jobs),
        'num_resources': len(resources),
        'num_skills': count_unique_skills(jobs),
        'total_duration': sum(job.duration for job in jobs),
        'avg_duration': np.mean([job.duration for job in jobs]),
        # ... 38 autres caractéristiques
    }
    
    return np.array(list(features.values()))
```

## 🎯 Création des labels d'entraînement

### **Stratégie de labeling**
```python
def create_labels(makespan_results, tolerance=0.1):
    """Crée les labels binaires avec tolérance"""
    
    # Trouver le makespan optimal
    optimal_makespan = min(makespan_results.values())
    
    # Label = 1 si dans la tolérance, 0 sinon
    labels = {}
    for algo, makespan in makespan_results.items():
        threshold = optimal_makespan * (1 + tolerance/100)
        labels[algo] = 1 if makespan <= threshold else 0
    
    return labels
```

### **Tolérances testées**
- **0.1%** : Très stricte (sélection finale)
- **1.0%** : Stricte (alternative)
- **5.0%** : Permissive (tests)

### **Distribution des labels (tolérance 0.1%)**
```
EST  : 85% des instances (17/20)
LPT  : 90% des instances (18/20) 
LST  : 70% des instances (14/20)
SPT  : 50% des instances (10/20)
LFT  : 35% des instances (7/20)
MSLF : 30% des instances (6/20)
FCFS : 30% des instances (6/20)
```

## 🔧 Configuration du modèle

### **Random Forest par classificateur**
```python
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(
    n_estimators=100,      # 100 arbres
    random_state=42,       # Reproductibilité
    class_weight='balanced' # Équilibrage classes
)
```

### **Validation croisée**
```python
from sklearn.model_selection import cross_val_score

# 5-fold cross-validation
cv_scores = cross_val_score(classifier, X_train, y_train, cv=5)
accuracy = cv_scores.mean()
```

## 📈 Performance du modèle

### **Métriques par algorithme**
```
Algorithme | Accuracy | Precision | Recall | F1-Score
-----------|----------|-----------|--------|----------
EST        | 100.0%   | 100.0%    | 100.0% | 100.0%
LPT        | 100.0%   | 100.0%    | 100.0% | 100.0%
LST        | 83.3%    | 100.0%    | 80.0%  | 88.9%
SPT        | 50.0%    | 50.0%     | 66.7%  | 57.1%
LFT        | 83.3%    | 100.0%    | 50.0%  | 66.7%
MSLF       | 83.3%    | 100.0%    | 50.0%  | 66.7%
FCFS       | 83.3%    | 100.0%    | 50.0%  | 66.7%
```

### **Métriques globales**
```
Hamming Loss      : 16.7%
Exact Match Ratio : 50.0%
Subset Accuracy   : 100.0%
```

### **Performance en production**
```
Tests réussis : 5/5 (100%)
IA correcte   : 5/5 (100%)
Amélioration  : 3.6% en moyenne
```

## 🔄 Pipeline d'entraînement

### **1. Préparation des données**
```python
# 1. Génération des données makespan
python3 makespan_calculator.py

# 2. Chargement et nettoyage
instances = load_instances_with_results("./resultats/makespan_details/")

# 3. Extraction des caractéristiques
X = np.array([extract_features(inst) for inst in instances])

# 4. Création des labels
y = np.array([create_labels(results) for results in makespan_results])
```

### **2. Division des données**
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

### **3. Entraînement**
```python
# Pour chaque algorithme
for i, algo in enumerate(['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']):
    
    # Entraîner le classificateur
    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train[:, i])
    
    # Valider
    accuracy = classifier.score(X_test, y_test[:, i])
    
    # Sauvegarder
    classifiers[algo] = classifier
```

### **4. Sauvegarde du modèle**
```python
import joblib

model_data = {
    'classifiers': classifiers,
    'feature_names': feature_names,
    'algorithm_names': algorithm_names,
    'training_stats': training_stats
}

joblib.dump(model_data, './resultats/binary_relevance_model.pkl')
```

## 🎯 Utilisation du modèle

### **Prédiction pour une nouvelle instance**
```python
# 1. Charger le modèle
model = joblib.load('./resultats/binary_relevance_model.pkl')

# 2. Extraire les caractéristiques
features = extract_features('nouvelle_instance.msrcp')

# 3. Prédire pour chaque algorithme
recommendations = []
for algo, classifier in model['classifiers'].items():
    if classifier.predict([features])[0] == 1:
        recommendations.append(algo)

# 4. Résultat
print(f"Algorithmes recommandés: {recommendations}")
```

### **Scores de confiance**
```python
# Obtenir les probabilités
confidence_scores = {}
for algo, classifier in model['classifiers'].items():
    proba = classifier.predict_proba([features])[0]
    confidence_scores[algo] = proba[1]  # Probabilité classe positive

# Trier par confiance
sorted_algos = sorted(confidence_scores.items(), 
                     key=lambda x: x[1], reverse=True)
```

## 🔧 Optimisations et améliorations

### **Réglage des hyperparamètres**
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1'
)
```

### **Ingénierie des caractéristiques**
- **Caractéristiques dérivées** : Ratios, produits, différences
- **Transformations** : Log, sqrt, normalisation
- **Sélection automatique** : Importance des features

### **Approches alternatives testées**
1. **Multi-class** : Un seul classificateur → Moins performant
2. **Ensemble methods** : Combinaison de modèles → Complexité accrue
3. **Deep Learning** : Réseaux de neurones → Overfitting sur petit dataset

## 📊 Analyse des résultats

### **Features les plus importantes**
```
1. num_jobs              (12.3%)
2. resource_utilization  (11.8%)
3. skill_density         (10.2%)
4. avg_duration          (9.7%)
5. complexity_ratio      (8.9%)
...
```

### **Patterns découverts**
- **EST/LPT dominants** : Algorithmes les plus souvent optimaux
- **Projets complexes** : IA recommande plus d'algorithmes
- **Ressources limitées** : LST et MSLF privilégiés
- **Tâches courtes** : SPT plus efficace

### **Cas d'échec analysés**
- **Instances parfaitement équilibrées** : Tous algorithmes équivalents
- **Contraintes très spécifiques** : Domaine non vu en entraînement
- **Taille de dataset** : Plus de données améliorerait les performances

## 🎯 Perspective d'amélioration

### **Données**
- **Plus d'instances** : 100+ au lieu de 20
- **Instances diversifiées** : Différentes tailles et complexités
- **Validation externe** : Benchmarks standards

### **Modèles**
- **Ensemble learning** : Combinaison de plusieurs approches
- **Transfer learning** : Pré-entraînement sur domaines similaires
- **Online learning** : Mise à jour continue du modèle

### **Features**
- **Features temporelles** : Évolution dans le temps
- **Features contextuelles** : Type de projet, industrie
- **Features méta** : Propriétés des algorithmes eux-mêmes
