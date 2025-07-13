#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test automatisé pour le projet MS-RCPSP avec ML
Exécute une série de tests pour valider tout le système
"""

import os
import sys
import time
import subprocess
import traceback
from typing import List, Dict, Any


class TestRunner:
    """Gestionnaire de tests automatisés"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.verbose = True
    
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        if level == "ERROR":
            print(f"[{timestamp}] ❌ {message}")
        elif level == "SUCCESS":
            print(f"[{timestamp}] ✅ {message}")
        elif level == "WARNING":
            print(f"[{timestamp}] ⚠️  {message}")
        else:
            print(f"[{timestamp}] ℹ️  {message}")
    
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> bool:
        """Exécute un test et enregistre le résultat"""
        self.log(f"Démarrage du test: {test_name}")
        try:
            start = time.time()
            result = test_func(*args, **kwargs)
            duration = time.time() - start
            
            if result:
                self.log(f"Test réussi: {test_name} ({duration:.2f}s)", "SUCCESS")
                self.test_results[test_name] = {"status": "PASS", "duration": duration}
                return True
            else:
                self.log(f"Test échoué: {test_name}", "ERROR")
                self.test_results[test_name] = {"status": "FAIL", "duration": duration}
                return False
                
        except Exception as e:
            self.log(f"Erreur dans {test_name}: {e}", "ERROR")
            self.test_results[test_name] = {"status": "ERROR", "error": str(e)}
            if self.verbose:
                traceback.print_exc()
            return False
    
    def test_python_environment(self) -> bool:
        """Test de l'environnement Python"""
        # Vérifier la version Python
        if sys.version_info < (3, 7):
            self.log(f"Python {sys.version} < 3.7 requis", "ERROR")
            return False
        
        # Vérifier les modules requis
        required_modules = ['numpy', 'pandas', 'sklearn']
        for module in required_modules:
            try:
                __import__(module)
                self.log(f"Module {module} disponible")
            except ImportError:
                self.log(f"Module {module} manquant", "ERROR")
                return False
        
        return True
    
    def test_file_structure(self) -> bool:
        """Test de la structure des fichiers"""
        required_files = [
            'msrcpsp_final.py',
            'binary_relevance_msrcpsp.py',
            'exemple_ml.py',
            'demo_ml_integration.py',
            'assistant_ml.py'
        ]
        
        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                self.log(f"Fichier trouvé: {file}")
            else:
                missing_files.append(file)
                self.log(f"Fichier manquant: {file}", "WARNING")
        
        # Vérifier le répertoire d'instances
        if os.path.exists("Instances"):
            instance_files = [f for f in os.listdir("Instances") 
                            if f.endswith(('.dzn', '.msrcp'))]
            self.log(f"Instances trouvées: {len(instance_files)}")
        else:
            self.log("Répertoire Instances manquant", "WARNING")
        
        return len(missing_files) == 0
    
    def test_ml_imports(self) -> bool:
        """Test des imports ML"""
        try:
            from binary_relevance_msrcpsp import (
                InstanceFeatureExtractor,
                BinaryRelevanceClassifier,
                MLIntegratedMSRCPSP
            )
            self.log("Imports ML réussis")
            return True
        except Exception as e:
            self.log(f"Échec des imports ML: {e}", "ERROR")
            return False
    
    def test_ml_functionality(self) -> bool:
        """Test des fonctionnalités ML de base"""
        try:
            from binary_relevance_msrcpsp import InstanceFeatureExtractor
            
            # Test d'extraction de features
            extractor = InstanceFeatureExtractor()
            
            # Données de test
            test_data = {
                'nActs': 5, 'nRes': 2, 'nSkills': 3,
                'dur': [1, 2, 3, 1, 2],
                'sreq': [[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 1], [1, 1, 1]],
                'mastery': [[1, 1, 0], [0, 1, 1]],
                'precedence_graph': {0: {'successors': [1], 'predecessors': []}},
                'est': [0, 1, 2, 3, 4], 'lst': [0, 1, 2, 3, 4],
                'lft': [1, 3, 5, 4, 6], 'float_dyn': [0, 0, 0, 0, 0]
            }
            
            features = extractor.extract_all_features(test_data)
            
            if len(features) > 40:  # Attendu: 43 features
                self.log(f"Features extraites: {len(features)}")
                return True
            else:
                self.log(f"Trop peu de features: {len(features)}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Erreur fonctionnalité ML: {e}", "ERROR")
            return False
    
    def test_ml_training_simulation(self) -> bool:
        """Test de simulation d'entraînement ML"""
        try:
            import numpy as np
            from binary_relevance_msrcpsp import BinaryRelevanceClassifier
            
            # Créer des données simulées
            np.random.seed(42)
            n_samples, n_features = 20, 10
            algorithms = ['EST', 'LFT', 'MSLF']
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.randint(0, 2, (n_samples, len(algorithms)))
            
            # Entraîner le modèle
            classifier = BinaryRelevanceClassifier()
            classifier.fit(X, y, algorithms, [f"feature_{i}" for i in range(n_features)])
            
            # Test de prédiction
            X_test = np.random.randn(5, n_features)
            predictions = classifier.predict(X_test)
            best_rules = classifier.get_best_rules(X_test, top_k=2)
            
            if len(best_rules) == 5 and len(best_rules[0]) == 2:
                self.log("Simulation d'entraînement réussie")
                return True
            else:
                self.log("Prédictions incorrectes", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Erreur simulation entraînement: {e}", "ERROR")
            return False
    
    def test_run_example_script(self) -> bool:
        """Test d'exécution du script d'exemple"""
        try:
            # Lancer exemple_ml.py avec input automatisé
            cmd = [sys.executable, "exemple_ml.py"]
            process = subprocess.Popen(
                cmd, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Simuler l'input utilisateur (choix "1")
            stdout, stderr = process.communicate(input="1\n")
            
            if process.returncode == 0:
                self.log("Script exemple_ml.py exécuté avec succès")
                return True
            else:
                self.log(f"Échec exemple_ml.py: {stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Erreur exécution exemple: {e}", "ERROR")
            return False
    
    def test_instances_parsing(self) -> bool:
        """Test de parsing d'instances"""
        instances_dir = "Instances"
        if not os.path.exists(instances_dir):
            self.log("Pas d'instances à tester", "WARNING")
            return True
        
        try:
            from binary_relevance_msrcpsp import parse_dzn_file, compute_temporal_metrics
            
            instance_files = [f for f in os.listdir(instances_dir) 
                            if f.endswith(('.dzn', '.msrcp'))]
            
            if not instance_files:
                self.log("Aucun fichier d'instance trouvé", "WARNING")
                return True
            
            # Tester le premier fichier
            test_file = os.path.join(instances_dir, instance_files[0])
            
            data = parse_dzn_file(test_file)
            data = compute_temporal_metrics(data)
            
            required_keys = ['nActs', 'nRes', 'nSkills']
            for key in required_keys:
                if key not in data:
                    self.log(f"Clé manquante dans parsing: {key}", "ERROR")
                    return False
            
            self.log(f"Parsing réussi pour {instance_files[0]}")
            return True
            
        except Exception as e:
            self.log(f"Erreur parsing instances: {e}", "ERROR")
            return False
    
    def test_model_integration(self) -> bool:
        """Test d'intégration du modèle ML"""
        model_path = "./resultats/binary_relevance_model.pkl"
        
        if not os.path.exists(model_path):
            self.log("Modèle ML non trouvé - test skippé", "WARNING")
            return True
        
        try:
            from binary_relevance_msrcpsp import MLIntegratedMSRCPSP
            
            ml_system = MLIntegratedMSRCPSP(model_path)
            self.log("Modèle ML chargé avec succès")
            
            # Test avec une instance si disponible
            instances_dir = "Instances"
            if os.path.exists(instances_dir):
                instance_files = [f for f in os.listdir(instances_dir) 
                                if f.endswith(('.dzn', '.msrcp'))]
                if instance_files:
                    test_instance = os.path.join(instances_dir, instance_files[0])
                    recommendations = ml_system.predict_best_algorithms(test_instance, top_k=3)
                    
                    if recommendations and len(recommendations) <= 3:
                        self.log(f"Prédictions ML: {recommendations}")
                        return True
                    else:
                        self.log("Prédictions ML incorrectes", "ERROR")
                        return False
            
            return True
            
        except Exception as e:
            self.log(f"Erreur intégration modèle: {e}", "ERROR")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Exécute tous les tests"""
        self.log("🚀 DÉMARRAGE DES TESTS AUTOMATISÉS")
        self.log("=" * 50)
        
        tests = [
            ("Environnement Python", self.test_python_environment),
            ("Structure des fichiers", self.test_file_structure),
            ("Imports ML", self.test_ml_imports),
            ("Fonctionnalités ML", self.test_ml_functionality),
            ("Simulation entraînement", self.test_ml_training_simulation),
            ("Script exemple", self.test_run_example_script),
            ("Parsing instances", self.test_instances_parsing),
            ("Intégration modèle", self.test_model_integration),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if self.run_test(test_name, test_func):
                passed += 1
            print()  # Ligne vide entre les tests
        
        # Résumé final
        duration = time.time() - self.start_time
        self.log("=" * 50)
        self.log("📊 RÉSUMÉ DES TESTS")
        self.log("=" * 50)
        
        for test_name, result in self.test_results.items():
            status = result["status"]
            if status == "PASS":
                self.log(f"✅ {test_name}", "SUCCESS")
            elif status == "FAIL":
                self.log(f"❌ {test_name}", "ERROR")
            else:
                self.log(f"⚠️  {test_name} - {result.get('error', 'Erreur')}", "WARNING")
        
        self.log("=" * 50)
        self.log(f"Tests réussis: {passed}/{total}")
        self.log(f"Temps total: {duration:.2f} secondes")
        
        if passed == total:
            self.log("🎉 TOUS LES TESTS SONT PASSÉS!", "SUCCESS")
        else:
            self.log(f"⚠️  {total - passed} test(s) en échec", "WARNING")
    
        return {
            "passed": passed,
            "total": total,
            "duration": duration,
            "results": self.test_results
        }


def main():
    """Fonction principale"""
    print("🤖 TEST AUTOMATISÉ - PROJET MS-RCPSP avec ML")
    print("=" * 60)
    print()
    
    # Options de ligne de commande simples
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    quick = "--quick" in sys.argv or "-q" in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python test_automatique.py [options]")
        print("Options:")
        print("  -v, --verbose    Mode verbose (plus de détails)")
        print("  -q, --quick      Tests rapides seulement")
        print("  -h, --help       Affiche cette aide")
        return
    
    runner = TestRunner()
    runner.verbose = verbose
    
    if quick:
        runner.log("Mode rapide - tests essentiels seulement")
    
    try:
        results = runner.run_all_tests()
        
        # Code de sortie
        if results["passed"] == results["total"]:
            sys.exit(0)  # Succès
        else:
            sys.exit(1)  # Échec
            
    except KeyboardInterrupt:
        runner.log("Tests interrompus par l'utilisateur", "WARNING")
        sys.exit(130)
    except Exception as e:
        runner.log(f"Erreur critique: {e}", "ERROR")
        sys.exit(2)


if __name__ == "__main__":
    main()
