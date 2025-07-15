#!/usr/bin/env python3
"""
Générateur de données de makespan pour l'entraînement ML
Version simplifiée et robuste
"""

import os
import json
import time
from msrcpsp_final import MSRCPSPParser, MSRCPSPScheduler

def calculate_makespans_for_instances(instances_dir="./Instances", 
                                    results_dir="./resultats", 
                                    max_instances=20):
    """Calcule les makespans pour un ensemble d'instances"""
    
    # Créer les dossiers nécessaires
    os.makedirs(results_dir, exist_ok=True)
    makespan_details_dir = os.path.join(results_dir, "makespan_details")
    os.makedirs(makespan_details_dir, exist_ok=True)
    
    # Algorithmes à tester
    algorithms = ['EST', 'LFT', 'MSLF', 'SPT', 'LPT', 'FCFS', 'LST']
    
    print(f"🚀 Génération des données de makespan")
    print(f"Répertoire instances: {instances_dir}")
    print(f"Répertoire résultats: {results_dir}")
    print(f"Algorithmes: {algorithms}")
    print(f"Maximum instances: {max_instances}")
    
    # Trouver les fichiers d'instances
    instance_files = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    instance_files = instance_files[:max_instances]  # Limiter pour les tests
    
    print(f"Fichiers trouvés: {len(instance_files)}")
    
    all_results = {}
    successful_instances = 0
    
    for i, filename in enumerate(instance_files):
        instance_name = filename.replace('.msrcp', '')
        filepath = os.path.join(instances_dir, filename)
        
        print(f"\n[{i+1}/{len(instance_files)}] Traitement de {instance_name}")
        
        try:
            # Parser l'instance
            instance = MSRCPSPParser.parse_file(filepath)
            scheduler = MSRCPSPScheduler(instance)
            
            instance_results = {
                'instance': instance_name,
                'instance_info': {
                    'num_activities': instance.num_activities,
                    'num_resources': instance.num_resources,
                    'num_skills': instance.num_skills
                },
                'results': {}
            }
            
            # Tester chaque algorithme
            for algo in algorithms:
                print(f"  Test {algo}...", end=" ")
                try:
                    start_time = time.time()
                    makespan, schedule = scheduler.schedule_with_priority(algo)
                    duration = time.time() - start_time
                    
                    instance_results['results'][algo] = {
                        'makespan': float(makespan) if makespan != float('inf') else None,
                        'duration': duration,
                        'success': makespan != float('inf')
                    }
                    
                    if makespan != float('inf'):
                        print(f"✅ {makespan}")
                    else:
                        print(f"❌ Infini")
                        
                except Exception as e:
                    print(f"❌ Erreur: {e}")
                    instance_results['results'][algo] = {
                        'makespan': None,
                        'duration': 0,
                        'success': False,
                        'error': str(e)
                    }
            
            # Sauvegarder les résultats de cette instance
            output_file = os.path.join(makespan_details_dir, f"{instance_name}_makespans.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(instance_results, f, indent=2, ensure_ascii=False)
            
            all_results[instance_name] = instance_results
            successful_instances += 1
            
        except Exception as e:
            print(f"❌ Erreur générale avec {instance_name}: {e}")
    
    # Générer un résumé global
    summary = {
        'total_instances': len(instance_files),
        'successful_instances': successful_instances,
        'success_rate': (successful_instances / len(instance_files) * 100) if instance_files else 0,
        'algorithms': algorithms,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Sauvegarder le résumé
    summary_file = os.path.join(results_dir, "makespan_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Terminé!")
    print(f"Instances traitées avec succès: {successful_instances}/{len(instance_files)}")
    print(f"Taux de réussite: {summary['success_rate']:.1f}%")
    print(f"Résultats sauvegardés dans: {results_dir}")
    
    return all_results, summary

if __name__ == "__main__":
    calculate_makespans_for_instances()
