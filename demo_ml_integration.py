#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démonstration pour l'intégration ML dans MS-RCPSP
"""

import os
import sys
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP, demonstrate_ml_integration


def quick_demo():
    """Démonstration rapide du système ML"""
    print("=" * 70)
    print("DÉMONSTRATION RAPIDE - INTÉGRATION ML MS-RCPSP")
    print("=" * 70)
    
    # Vérifier les fichiers nécessaires
    model_path = "./resultats/binary_relevance_model.pkl"
    instances_dir = "./Instances"
    
    print("Vérification des prérequis:")
    print(f"  - Modèle ML: {'✓' if os.path.exists(model_path) else '✗'} {model_path}")
    print(f"  - Instances: {'✓' if os.path.exists(instances_dir) else '✗'} {instances_dir}")
    
    if not os.path.exists(model_path):
        print("\n⚠️  Modèle ML non trouvé!")
        print("   Exécutez d'abord: python binary_relevance_msrcpsp.py")
        print("   Et choisissez l'option 1 pour entraîner un modèle.")
        return False
    
    if not os.path.exists(instances_dir):
        print("\n⚠️  Répertoire d'instances non trouvé!")
        print("   Assurez-vous que le répertoire ./Instances existe avec des fichiers .dzn ou .msrcp")
        return False
    
    # Créer l'interface ML
    print("\n" + "="*50)
    print("INITIALISATION DU SYSTÈME ML")
    print("="*50)
    
    ml_system = MLIntegratedMSRCPSP(model_path)
    
    # Lister les instances disponibles
    instance_files = [f for f in os.listdir(instances_dir) 
                     if f.endswith(('.dzn', '.msrcp'))]
    
    if not instance_files:
        print("Aucun fichier d'instance trouvé!")
        return False
    
    print(f"Instances disponibles: {len(instance_files)}")
    
    # Test sur les 3 premières instances
    print("\n" + "="*50)
    print("TEST SUR QUELQUES INSTANCES")
    print("="*50)
    
    for i, filename in enumerate(instance_files[:3]):
        instance_path = os.path.join(instances_dir, filename)
        
        print(f"\n--- Instance {i+1}: {filename} ---")
        
        try:
            # Prédiction ML seulement
            recommendations = ml_system.predict_best_algorithms(instance_path, top_k=3)
            print(f"Algorithmes recommandés: {recommendations}")
            
            # Résolution complète si le solveur est disponible
            from binary_relevance_msrcpsp import MSRCPSPSolver
            if MSRCPSPSolver is not None:
                result = ml_system.solve_with_ml_guidance(instance_path)
                if result and 'best_makespan' in result:
                    print(f"Meilleur makespan: {result['best_makespan']}")
                    print(f"Meilleur algorithme: {result['best_algorithm']}")
                else:
                    print("Résolution échouée")
            else:
                print("Solveur non disponible - prédiction ML uniquement")
                
        except Exception as e:
            print(f"Erreur: {e}")
    
    print(f"\n{'='*50}")
    print("DÉMONSTRATION TERMINÉE")
    print(f"{'='*50}")
    print("Pour utiliser le système complet:")
    print("  python binary_relevance_msrcpsp.py")
    print("  Choisissez l'option 2 ou 4 pour utiliser le ML")
    
    return True


def interactive_demo():
    """Démonstration interactive"""
    print("=" * 70)
    print("DÉMONSTRATION INTERACTIVE - ML MS-RCPSP")
    print("=" * 70)
    
    # Vérifications
    if not quick_demo():
        return
    
    model_path = "./resultats/binary_relevance_model.pkl"
    instances_dir = "./Instances"
    
    ml_system = MLIntegratedMSRCPSP(model_path)
    instance_files = [f for f in os.listdir(instances_dir) 
                     if f.endswith(('.dzn', '.msrcp'))]
    
    while True:
        print(f"\n{'='*50}")
        print("OPTIONS DISPONIBLES")
        print(f"{'='*50}")
        print("1. Tester une instance spécifique")
        print("2. Tester plusieurs instances")
        print("3. Afficher les instances disponibles")
        print("4. Quitter")
        
        try:
            choice = input("\nChoisissez une option (1-4): ").strip()
            
            if choice == "1":
                print(f"\nInstances disponibles:")
                for i, f in enumerate(instance_files[:10], 1):
                    print(f"  {i:2d}. {f}")
                
                if len(instance_files) > 10:
                    print(f"  ... et {len(instance_files)-10} autres")
                
                try:
                    idx = int(input(f"\nChoisissez un numéro (1-{min(10, len(instance_files))}): ")) - 1
                    if 0 <= idx < len(instance_files):
                        instance_path = os.path.join(instances_dir, instance_files[idx])
                        test_single_instance(ml_system, instance_path)
                    else:
                        print("Numéro invalide!")
                except ValueError:
                    print("Veuillez entrer un numéro valide!")
            
            elif choice == "2":
                try:
                    n = int(input(f"Combien d'instances tester (max {len(instance_files)})? "))
                    n = min(n, len(instance_files))
                    
                    for i in range(n):
                        instance_path = os.path.join(instances_dir, instance_files[i])
                        print(f"\n--- Test {i+1}/{n}: {instance_files[i]} ---")
                        test_single_instance(ml_system, instance_path)
                        
                except ValueError:
                    print("Veuillez entrer un nombre valide!")
            
            elif choice == "3":
                print(f"\nInstances disponibles ({len(instance_files)} total):")
                for i, f in enumerate(instance_files, 1):
                    print(f"  {i:2d}. {f}")
            
            elif choice == "4":
                print("Au revoir!")
                break
            
            else:
                print("Option invalide!")
                
        except KeyboardInterrupt:
            print("\nInterruption utilisateur. Au revoir!")
            break
        except Exception as e:
            print(f"Erreur: {e}")


def test_single_instance(ml_system, instance_path):
    """Teste une instance spécifique"""
    filename = os.path.basename(instance_path)
    
    try:
        # Prédiction ML
        recommendations = ml_system.predict_best_algorithms(instance_path, top_k=5)
        print(f"Recommandations ML: {recommendations}")
        
        # Résolution si possible
        from binary_relevance_msrcpsp import MSRCPSPSolver
        if MSRCPSPSolver is not None:
            result = ml_system.solve_with_ml_guidance(instance_path)
            
            if result and 'all_results' in result:
                print(f"Résultats de résolution:")
                for algo, res in result['all_results'].items():
                    status = "✓" if res.get('success', False) else "✗"
                    makespan = res.get('makespan', 'inf')
                    print(f"  {status} {algo:8s}: {makespan}")
                
                if 'best_algorithm' in result:
                    print(f"🏆 Meilleur: {result['best_algorithm']} (makespan: {result['best_makespan']})")
            else:
                print("Résolution échouée")
        else:
            print("Solveur non disponible - prédiction ML uniquement")
            
    except Exception as e:
        print(f"Erreur lors du test de {filename}: {e}")


def performance_benchmark():
    """Benchmark de performance du système ML"""
    print("=" * 70)
    print("BENCHMARK DE PERFORMANCE ML")
    print("=" * 70)
    
    model_path = "./resultats/binary_relevance_model.pkl"
    instances_dir = "./Instances"
    
    if not os.path.exists(model_path) or not os.path.exists(instances_dir):
        print("Prérequis manquants pour le benchmark!")
        return
    
    ml_system = MLIntegratedMSRCPSP(model_path)
    instance_files = [f for f in os.listdir(instances_dir) 
                     if f.endswith(('.dzn', '.msrcp'))][:20]  # Max 20 instances
    
    results = {
        'total_instances': len(instance_files),
        'successful_predictions': 0,
        'successful_resolutions': 0,
        'algorithm_diversity': [],
        'makespan_improvements': []
    }
    
    print(f"Test sur {len(instance_files)} instances...")
    
    for i, filename in enumerate(instance_files, 1):
        instance_path = os.path.join(instances_dir, filename)
        print(f"\r{i}/{len(instance_files)} - {filename[:30]}...", end="")
        
        try:
            # Test de prédiction
            recommendations = ml_system.predict_best_algorithms(instance_path, top_k=3)
            if recommendations:
                results['successful_predictions'] += 1
                results['algorithm_diversity'].append(len(set(recommendations)))
            
            # Test de résolution si possible
            from binary_relevance_msrcpsp import MSRCPSPSolver
            if MSRCPSPSolver is not None:
                result = ml_system.solve_with_ml_guidance(instance_path)
                if result and result.get('best_makespan', float('inf')) != float('inf'):
                    results['successful_resolutions'] += 1
                    
                    perf = result.get('performance_improvement', {})
                    if 'improvement_percentage' in perf:
                        results['makespan_improvements'].append(perf['improvement_percentage'])
        
        except Exception:
            pass  # Ignorer les erreurs pour le benchmark
    
    print("\n\n" + "="*50)
    print("RÉSULTATS DU BENCHMARK")
    print("="*50)
    
    print(f"Instances testées: {results['total_instances']}")
    print(f"Prédictions réussies: {results['successful_predictions']}/{results['total_instances']} "
          f"({results['successful_predictions']/results['total_instances']*100:.1f}%)")
    
    if results['successful_resolutions'] > 0:
        print(f"Résolutions réussies: {results['successful_resolutions']}/{results['total_instances']} "
              f"({results['successful_resolutions']/results['total_instances']*100:.1f}%)")
    
    if results['algorithm_diversity']:
        import numpy as np
        avg_diversity = np.mean(results['algorithm_diversity'])
        print(f"Diversité moyenne des algorithmes: {avg_diversity:.1f}")
    
    if results['makespan_improvements']:
        import numpy as np
        avg_improvement = np.mean(results['makespan_improvements'])
        print(f"Amélioration moyenne: {avg_improvement:.1f}%")


def main():
    """Menu principal de démonstration"""
    print("=" * 70)
    print("DÉMONSTRATION ML MS-RCPSP")
    print("=" * 70)
    
    options = [
        ("1", "Démonstration rapide", quick_demo),
        ("2", "Démonstration interactive", interactive_demo),
        ("3", "Benchmark de performance", performance_benchmark),
        ("4", "Démonstration complète", demonstrate_ml_integration),
    ]
    
    print("\nOptions de démonstration:")
    for code, name, _ in options:
        print(f"  {code}. {name}")
    
    try:
        choice = input("\nChoisissez une option (1-4, ou Entrée pour option 1): ").strip()
        if not choice:
            choice = "1"
        
        for code, name, func in options:
            if choice == code:
                print(f"\n--- {name} ---")
                func()
                return
        
        print("Option invalide!")
        
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")


if __name__ == "__main__":
    main()
