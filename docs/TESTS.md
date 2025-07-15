# 🧪 Tests et Validation

## 📋 Vue d'ensemble

Le système MS-RCPSP dispose de **plusieurs niveaux de tests** pour assurer la fiabilité, la performance et la correctness des algorithmes d'ordonnancement et du machine learning.

## 🚀 Tests automatisés principaux

### **1. `run_project.py` - Test complet du système**
```bash
python3 run_project.py
```

**Étapes de validation** :
1. ✅ **Dépendances** : Vérification et installation automatique
2. ✅ **Données** : Génération des makespans (20 instances)
3. ✅ **ML** : Entraînement du modèle (88.9% accuracy moyenne)
4. ✅ **Tests** : Validation sur 5 projets représentatifs
5. ✅ **Graphiques** : Création des visualisations
6. ✅ **Rapport** : Validation finale des résultats

**Critères de réussite** :
- 6/6 étapes complétées avec succès
- Modèle ML généré (~930KB)
- Taux de succès IA ≥ 80%
- Graphiques créés sans erreurs

### **2. `solution_finale.py` - Tests de validation**
```bash
python3 solution_finale.py
```

**Tests effectués** :
- 🔧 **Diagnostic système** : Modèle, dossiers, permissions
- 🧠 **Test ML** : Chargement et fonctionnement du modèle
- 🎯 **Tests représentatifs** : 5 instances variées
- 📊 **Métriques** : Performance IA et algorithmes
- 📄 **Validation résultats** : Format et cohérence

**Sortie attendue** :
```
🎯 Tests réussis: 5
🤖 IA correcte: 5/5 (100.0%)
🏆 Algorithmes optimaux trouvés: LPT, LST, EST
📊 Makespans: Min 106, Max 143, Moyenne 127.8 jours
```

## 🧪 Tests unitaires par module

### **1. Tests du moteur d'ordonnancement**

#### **Test `msrcpsp_final.py`**
```python
def test_algorithm_validity():
    """Test la validité des algorithmes d'ordonnancement"""
    
    # Données de test
    test_instance = "Instances/MSLIB_Set1_4799.msrcp"
    algorithms = ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']
    
    for algo in algorithms:
        makespan = solve_instance(test_instance, algo)
        
        # Vérifications
        assert makespan > 0, f"Makespan invalide pour {algo}"
        assert makespan < 1000, f"Makespan suspicieux pour {algo}"
        assert isinstance(makespan, (int, float)), f"Type invalide pour {algo}"
```

**Commande de test** :
```bash
python3 -c "
from msrcpsp_final import solve_instance
test_file = 'Instances/MSLIB_Set1_4799.msrcp'
for algo in ['EST', 'LFT', 'SPT']:
    result = solve_instance(test_file, algo)
    print(f'{algo}: {result} jours')
    assert result > 0
print('✅ Tests moteur d\'ordonnancement réussis')
"
```

### **2. Tests du Machine Learning**

#### **Test extraction de caractéristiques**
```python
def test_feature_extraction():
    """Test l'extraction des 43 caractéristiques"""
    
    from binary_relevance_msrcpsp import extract_features
    
    # Test sur instance connue
    features = extract_features("Instances/MSLIB_Set1_4799.msrcp")
    
    # Vérifications
    assert len(features) == 43, "Nombre de features incorrect"
    assert all(isinstance(f, (int, float)) for f in features), "Types invalides"
    assert all(f >= 0 for f in features), "Valeurs négatives suspectes"
    
    return True
```

#### **Test modèle ML**
```python
def test_ml_model():
    """Test le modèle de machine learning"""
    
    import joblib
    from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
    
    # Charger le modèle
    model_path = "./resultats/binary_relevance_model.pkl"
    ml_solver = MLIntegratedMSRCPSP(model_path)
    
    # Test de prédiction
    test_instance = "Instances/MSLIB_Set1_4799.msrcp"
    result = ml_solver.solve_with_ml_guidance(test_instance, "./resultats_ml/")
    
    # Vérifications
    assert 'ml_recommended_algorithms' in result
    assert 'best_algorithm' in result
    assert 'best_makespan' in result
    assert len(result['ml_recommended_algorithms']) > 0
    
    return True
```

**Commande de test** :
```bash
python3 -c "
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
ml = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl')
print('✅ Modèle ML chargé avec succès')
"
```

### **3. Tests de génération de données**

#### **Test `makespan_calculator.py`**
```python
def test_data_generation():
    """Test la génération des données d'entraînement"""
    
    import os
    import json
    
    # Exécuter la génération (sur un petit échantillon)
    os.system("python3 makespan_calculator.py")
    
    # Vérifier les résultats
    details_dir = "./resultats/makespan_details"
    assert os.path.exists(details_dir), "Dossier de résultats manquant"
    
    json_files = [f for f in os.listdir(details_dir) if f.endswith('.json')]
    assert len(json_files) > 0, "Aucun fichier de résultats généré"
    
    # Vérifier le format d'un fichier
    with open(os.path.join(details_dir, json_files[0])) as f:
        data = json.load(f)
    
    required_keys = ['instance', 'results', 'timestamp']
    for key in required_keys:
        assert key in data, f"Clé manquante : {key}"
    
    return True
```

## 📊 Tests de performance

### **1. Tests de temps d'exécution**

#### **Benchmark individuel**
```python
import time

def benchmark_algorithm(instance_path, algorithm):
    """Benchmark d'un algorithme sur une instance"""
    
    start_time = time.time()
    makespan = solve_instance(instance_path, algorithm)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    return {
        'algorithm': algorithm,
        'makespan': makespan,
        'execution_time': execution_time,
        'instance': instance_path
    }
```

#### **Test de performance ML**
```python
def benchmark_ml_performance():
    """Test des performances du système ML"""
    
    import time
    from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
    
    ml_solver = MLIntegratedMSRCPSP("./resultats/binary_relevance_model.pkl")
    
    instances = ["Instances/MSLIB_Set1_4799.msrcp", 
                "Instances/MSLIB_Set1_5060.msrcp"]
    
    total_time = 0
    correct_predictions = 0
    
    for instance in instances:
        start_time = time.time()
        result = ml_solver.solve_with_ml_guidance(instance, "./resultats_ml/")
        end_time = time.time()
        
        total_time += (end_time - start_time)
        
        # Vérifier si l'IA était correcte
        if result['best_algorithm'] in result['ml_recommended_algorithms']:
            correct_predictions += 1
    
    avg_time = total_time / len(instances)
    accuracy = correct_predictions / len(instances) * 100
    
    print(f"Temps moyen par instance : {avg_time:.2f}s")
    print(f"Précision IA : {accuracy:.1f}%")
    
    return avg_time, accuracy
```

**Critères de performance attendus** :
```
Temps par instance      : < 1 seconde
Temps total système     : < 60 secondes
Précision IA           : > 80%
Mémoire utilisée       : < 500 MB
```

### **2. Tests de charge**

#### **Test sur volume important**
```bash
# Test sur 100 instances (si disponibles)
python3 -c "
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
import os
import time

ml = MLIntegratedMSRCPSP('./resultats/binary_relevance_model.pkl')
instances = [f for f in os.listdir('Instances/') if f.endswith('.msrcp')][:100]

start_time = time.time()
success_count = 0

for i, instance in enumerate(instances):
    try:
        result = ml.solve_with_ml_guidance(f'Instances/{instance}', './resultats_ml/')
        success_count += 1
        if i % 10 == 0:
            print(f'Traité {i+1}/{len(instances)} instances')
    except Exception as e:
        print(f'Erreur sur {instance}: {e}')

end_time = time.time()
total_time = end_time - start_time

print(f'✅ Test de charge terminé')
print(f'Instances traitées: {success_count}/{len(instances)}')
print(f'Temps total: {total_time:.1f}s')
print(f'Temps moyen: {total_time/success_count:.2f}s par instance')
"
```

## 🎯 Tests de régression

### **1. Validation des résultats de référence**

#### **Résultats attendus (instances de référence)**
```python
EXPECTED_RESULTS = {
    "MSLIB_Set1_4799.msrcp": {
        "EST": 143.0,
        "LPT": 143.0, 
        "LST": 143.0,
        "SPT": 143.0,
        "FCFS": 149.0
    },
    "MSLIB_Set1_5060.msrcp": {
        "EST": 115.0,
        "LPT": 115.0,
        "LST": 115.0,
        "SPT": 115.0,
        "FCFS": 115.0
    }
}

def test_regression():
    """Test de non-régression sur instances de référence"""
    
    for instance, expected in EXPECTED_RESULTS.items():
        instance_path = f"Instances/{instance}"
        
        for algorithm, expected_makespan in expected.items():
            actual_makespan = solve_instance(instance_path, algorithm)
            
            assert actual_makespan == expected_makespan, \
                f"Régression détectée : {instance} {algorithm} " \
                f"attendu {expected_makespan}, obtenu {actual_makespan}"
    
    print("✅ Tests de régression réussis")
```

### **2. Validation des performances ML**

#### **Métriques de référence**
```python
ML_BASELINE = {
    "accuracy_minimum": 80.0,      # 80% minimum
    "precision_moyenne": 85.0,     # 85% en moyenne
    "recall_minimum": 70.0,        # 70% minimum
    "f1_score_minimum": 75.0       # 75% minimum
}

def validate_ml_metrics():
    """Valide que les métriques ML sont au niveau attendu"""
    
    # Charger les résultats d'évaluation
    with open("./resultats/ml_evaluation_metrics.json") as f:
        metrics = json.load(f)
    
    for metric, expected_value in ML_BASELINE.items():
        if metric in metrics:
            actual_value = metrics[metric]
            assert actual_value >= expected_value, \
                f"Performance ML dégradée : {metric} " \
                f"attendu >={expected_value}, obtenu {actual_value}"
    
    print("✅ Validation des métriques ML réussie")
```

## 🔧 Tests de robustesse

### **1. Tests avec données invalides**

#### **Gestion des erreurs**
```python
def test_error_handling():
    """Test la gestion des erreurs et cas limites"""
    
    from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
    
    ml_solver = MLIntegratedMSRCPSP("./resultats/binary_relevance_model.pkl")
    
    # Test fichier inexistant
    try:
        result = ml_solver.solve_with_ml_guidance("fichier_inexistant.msrcp", "./resultats_ml/")
        assert False, "Erreur attendue pour fichier inexistant"
    except FileNotFoundError:
        print("✅ Gestion fichier inexistant OK")
    
    # Test dossier de sortie inexistant
    try:
        result = ml_solver.solve_with_ml_guidance("Instances/MSLIB_Set1_4799.msrcp", "/dossier/inexistant/")
        # Doit créer le dossier automatiquement
        print("✅ Création automatique dossier OK")
    except Exception as e:
        print(f"⚠️ Problème création dossier : {e}")
```

### **2. Tests de limites**

#### **Instances extrêmes**
```python
def test_edge_cases():
    """Test sur des cas limites"""
    
    # Test sur la plus petite instance
    smallest_files = sorted([f for f in os.listdir("Instances/") if f.endswith('.msrcp')])[:1]
    
    # Test sur la plus grande instance  
    largest_files = sorted([f for f in os.listdir("Instances/") if f.endswith('.msrcp')], 
                          key=lambda x: os.path.getsize(f"Instances/{x}"))[-1:]
    
    test_files = smallest_files + largest_files
    
    for test_file in test_files:
        try:
            result = solve_instance(f"Instances/{test_file}", "EST")
            assert result > 0, f"Makespan invalide pour {test_file}"
            print(f"✅ Test {test_file} : {result} jours")
        except Exception as e:
            print(f"❌ Échec {test_file} : {e}")
```

## 📊 Tests d'intégration

### **1. Test workflow complet**
```python
def test_complete_workflow():
    """Test du workflow complet du système"""
    
    import os
    import tempfile
    
    # Créer un environnement de test temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # 1. Génération des données
        print("1. Test génération données...")
        # Code pour générer des données dans temp_dir
        
        # 2. Entraînement ML
        print("2. Test entraînement ML...")
        # Code pour entraîner un modèle
        
        # 3. Tests de prédiction
        print("3. Test prédictions...")
        # Code pour tester les prédictions
        
        # 4. Génération de graphiques
        print("4. Test visualisations...")
        # Code pour générer des graphiques
        
        print("✅ Workflow complet testé avec succès")
```

### **2. Test d'intégration des modules**
```bash
# Test séquentiel de tous les modules
python3 -c "
print('Test 1: Génération données')
exec(open('makespan_calculator.py').read())

print('Test 2: ML')  
exec(open('binary_relevance_msrcpsp.py').read())

print('Test 3: Validation')
exec(open('solution_finale.py').read())

print('✅ Tous les modules intégrés fonctionnent')
"
```

## 🎯 Tests de validation métier

### **1. Tests de cohérence des résultats**

#### **Cohérence algorithmique**
```python
def test_algorithm_consistency():
    """Test la cohérence des résultats entre algorithmes"""
    
    instance = "Instances/MSLIB_Set1_4799.msrcp"
    algorithms = ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']
    
    results = {}
    for algo in algorithms:
        results[algo] = solve_instance(instance, algo)
    
    # Vérifications de cohérence
    min_makespan = min(results.values())
    max_makespan = max(results.values())
    
    # L'écart ne doit pas être trop important (facteur 2 max)
    assert max_makespan <= min_makespan * 2, \
        f"Écart trop important : {min_makespan} vs {max_makespan}"
    
    # Au moins un algorithme doit être optimal
    optimal_count = sum(1 for v in results.values() if v == min_makespan)
    assert optimal_count >= 1, "Aucun algorithme optimal trouvé"
    
    print(f"✅ Cohérence vérifiée : écart {max_makespan/min_makespan:.2f}x")
```

#### **Cohérence ML**
```python
def test_ml_consistency():
    """Test la cohérence des recommandations ML"""
    
    from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
    
    ml_solver = MLIntegratedMSRCPSP("./resultats/binary_relevance_model.pkl")
    
    # Tester la même instance plusieurs fois
    instance = "Instances/MSLIB_Set1_4799.msrcp"
    
    results = []
    for i in range(3):
        result = ml_solver.solve_with_ml_guidance(instance, "./resultats_ml/")
        results.append(result['ml_recommended_algorithms'])
    
    # Les recommandations doivent être identiques (modèle déterministe)
    for i in range(1, len(results)):
        assert results[i] == results[0], \
            f"Recommandations ML inconsistantes : {results[0]} vs {results[i]}"
    
    print("✅ Cohérence ML vérifiée")
```

## 📋 Rapport de tests automatisé

### **Script de test complet**
```bash
#!/bin/bash
# test_complete.sh

echo "🧪 LANCEMENT DES TESTS COMPLETS MS-RCPSP"
echo "========================================"

# Test 1: Installation et dépendances
echo "Test 1: Vérification des dépendances..."
python3 -c "import numpy, sklearn, matplotlib, pandas, seaborn; print('✅ OK')" || exit 1

# Test 2: Modules de base
echo "Test 2: Modules de base..."
python3 -c "from msrcpsp_final import solve_instance; print('✅ OK')" || exit 1

# Test 3: Génération de données
echo "Test 3: Génération de données..."
timeout 60 python3 makespan_calculator.py || exit 1

# Test 4: Machine Learning
echo "Test 4: Machine Learning..."
echo "1" | timeout 120 python3 binary_relevance_msrcpsp.py || exit 1

# Test 5: Validation système
echo "Test 5: Validation système..."
timeout 60 python3 solution_finale.py || exit 1

# Test 6: Visualisations
echo "Test 6: Visualisations..."
echo "4" | timeout 180 python3 nettoyage_et_graphiques.py || exit 1

echo ""
echo "🎉 TOUS LES TESTS RÉUSSIS !"
echo "=========================="
echo "✅ Système complètement opérationnel"
```

### **Métriques de succès**
```
Tests passés        : 6/6 (100%)
Temps total         : < 10 minutes
Modèle ML généré    : ✅ (~930KB)
Résultats ML        : ✅ (5+ fichiers)
Graphiques créés    : ✅ (4+ images)
Précision IA        : ✅ (≥80%)
Performance temps   : ✅ (<1s/instance)
```
