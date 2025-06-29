#!/usr/bin/env python3
"""
Script principal pour exécuter l'analyse complète MS-RCPSP
Usage: python run_analysis.py
"""

import sys
import os

# Ajouter le répertoire courant au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from makespan_calculator import MakespanCalculator
    from paste import parse_dzn_file, compute_temporal_metrics, MSRCPSPPriorityAlgorithms
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que tous les fichiers nécessaires sont présents:")
    print("  - makespan_calculator.py")
    print("  - paste.py (votre code des algorithmes)")
    sys.exit(1)


def check_directories():
    """Vérifie que les répertoires nécessaires existent"""
    required_dirs = ["./instances", "./resultats"]
    missing_dirs = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print("Répertoires manquants:")
        for directory in missing_dirs:
            print(f"  - {directory}")
        
        print("\nCréation des répertoires manquants...")
        for directory in missing_dirs:
            os.makedirs(directory, exist_ok=True)
            print(f"  ✓ {directory} créé")


def run_priority_algorithms_first():
    """Exécute d'abord les algorithmes de priorité si nécessaire"""
    print("Vérification des résultats des algorithmes de priorité...")
    
    # Vérifier si les résultats existent déjà
    results_exist = False
    algorithms = ['HRPW*', 'LST', 'LFT', 'MTS', 'TIMROS', 'HRU1', 'TIMRES', 'HRU2', 'STFD', 'EFT']
    
    for algorithm in algorithms:
        algo_dir = os.path.join("./resultats", algorithm)
        if os.path.exists(algo_dir) and os.listdir(algo_dir):
            results_exist = True
            break
    
    if not results_exist:
        print("Aucun résultat d'algorithme trouvé. Exécution des algorithmes de priorité...")
        
        # Importer et exécuter le code principal des algorithmes
        try:
            import glob
            
            instances_dir = "./instances"
            dzn_files = glob.glob(os.path.join(instances_dir, "*.dzn"))
            
            if not dzn_files:
                print(f"Aucune instance .dzn trouvée dans {instances_dir}")
                print("Veuillez placer vos fichiers d'instances dans le répertoire ./instances/")
                return False
            
            print(f"Traitement de {len(dzn_files)} instance(s)...")
            
            for dzn_file in dzn_files:
                instance_name = os.path.splitext(os.path.basename(dzn_file))[0]
                print(f"  Traitement: {instance_name}")
                
                try:
                    # Charger et traiter l'instance
                    instance_data = parse_dzn_file(dzn_file)
                    instance_data = compute_temporal_metrics(instance_data)
                    
                    # Créer l'objet algorithmes
                    algorithms_obj = MSRCPSPPriorityAlgorithms(instance_data)
                    
                    # Obtenir tous les ordres de priorité
                    all_orders = algorithms_obj.get_all_priority_orders()
                    
                    # Sauvegarder les résultats
                    for rule_name, activity_order in all_orders.items():
                        rule_dir = os.path.join("./resultats", rule_name)
                        os.makedirs(rule_dir, exist_ok=True)
                        
                        output_data = {
                            "instance": instance_name,
                            "rule": rule_name,
                            "n_activities": instance_data.get('nActs', 0),
                            "ordered_activities": activity_order,
                            "durations": instance_data.get('dur', [])
                        }
                        
                        output_file = os.path.join(rule_dir, f"{instance_name}.json")
                        import json
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                except Exception as e:
                    print(f"    Erreur: {e}")
                    continue
            
            print("Algorithmes de priorité exécutés avec succès!")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'exécution des algorithmes: {e}")
            return False
    else:
        print("Résultats des algorithmes de priorité trouvés ✓")
        return True


def main():
    """Fonction principale"""
    print("="*60)
    print("ANALYSE COMPLÈTE MS-RCPSP")
    print("Calcul des makespans et comparaison des algorithmes")
    print("="*60)
    
    # Vérifier les répertoires
    check_directories()
    
    # Exécuter les algorithmes de priorité si nécessaire
    if not run_priority_algorithms_first():
        print("Impossible de générer les résultats des algorithmes de priorité.")
        print("Vérifiez vos fichiers d'instances et réessayez.")
        return
    
    # Exécuter l'analyse des makespans
    print("\n" + "="*60)
    print("CALCUL DES MAKESPANS")
    print("="*60)
    
    try:
        calculator = MakespanCalculator()
        calculator.run_complete_analysis()
        
        print("\n" + "="*60)
        print("ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("="*60)
        print("\nFichiers de résultats générés dans ./resultats/")
        print("  📊 makespan_comparison.csv - Comparaison détaillée")
        print("  📈 summary_statistics.csv - Statistiques résumées")
        print("  📁 makespan_details/ - Résultats détaillés par instance")
        
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Astuce :")
        print("  - Vérifiez que vos fichiers JSON de résultats contiennent bien des dictionnaires (avec .get),")
        print("    et non des listes. Un résultat de type 'list' au lieu de 'dict' indique un problème dans la génération des fichiers JSON.")
        print("  - L'erreur 'KeyError: Avg_Makespan' signifie que la colonne 'Avg_Makespan' est absente du DataFrame.")
        print("    Vérifiez que les résultats intermédiaires sont bien calculés et que les noms de colonnes sont corrects dans makespan_calculator.py.")


if __name__ == "__main__":
    main()