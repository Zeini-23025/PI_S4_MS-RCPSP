#!/usr/bin/env python3
"""
Script de diagnostic pour analyser pourquoi les algorithmes donnent les mêmes résultats
"""

import os
from msrcpsp_final import MSRCPSPParser, MSRCPSPScheduler


def diagnose_instance_issue(instance_path: str):
    """Diagnostic détaillé d'une instance"""
    print(f"\n{'='*60}")
    print(f"DIAGNOSTIC: {os.path.basename(instance_path)}")
    print(f"{'='*60}")
    
    try:
        # Parser l'instance
        instance = MSRCPSPParser.parse_file(instance_path)
        scheduler = MSRCPSPScheduler(instance)
        
        # Statistiques de base
        print(f"📊 Activités: {instance.num_activities}")
        print(f"📊 Ressources: {instance.num_resources}")
        print(f"📊 Compétences: {instance.num_skills}")
        print(f"📊 Deadline: {instance.level_deadline}")
        
        # Analyser les activités
        total_duration = sum(a.duration for a in instance.activities)
        zero_duration = sum(1 for a in instance.activities if a.duration == 0)
        print(f"📊 Durée totale: {total_duration}")
        print(f"📊 Activités durée 0: {zero_duration}")
        
        # Analyser les contraintes de précédence
        total_prec = sum(len(a.predecessors) for a in instance.activities)
        print(f"📊 Contraintes de précédence: {total_prec}")
        
        # Analyser les exigences de ressources
        activities_with_req = 0
        total_requirements = 0
        for activity in instance.activities:
            req_sum = sum(activity.skill_requirements)
            if req_sum > 0:
                activities_with_req += 1
                total_requirements += req_sum
        
        print(f"📊 Activités avec exigences: {activities_with_req}/{instance.num_activities}")
        print(f"📊 Total exigences: {total_requirements}")
        
        # Tester l'ordonnancement avec différents algorithmes
        algorithms = ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"]
        results = {}
        
        print(f"\n🔍 Test des algorithmes:")
        for alg in algorithms:
            try:
                makespan, schedule = scheduler.schedule_with_priority(alg)
                results[alg] = makespan
                activities_scheduled = len(schedule)
                print(f"  {alg:4s}: makespan={makespan:3d}, activités={activities_scheduled:3d}/{instance.num_activities}")
            except Exception as e:
                results[alg] = float('inf')
                print(f"  {alg:4s}: ERREUR - {str(e)}")
        
        # Analyser les résultats
        valid_results = [v for v in results.values() if v != float('inf')]
        if valid_results:
            unique_results = set(valid_results)
            print(f"\n📈 Résultats uniques: {len(unique_results)}")
            print(f"📈 Meilleur: {min(valid_results)}")
            print(f"📈 Pire: {max(valid_results)}")
            
            if len(unique_results) == 1:
                print("⚠️  TOUS LES ALGORITHMES DONNENT LE MÊME RÉSULTAT!")
                print("   Causes possibles:")
                print("   - Instance trop contrainte (peu de liberté d'ordonnancement)")
                print("   - Problème dans l'algorithme de scheduling")
                print("   - Activités dummy dominent le problème")
        
        # Examiner une activité en détail
        if instance.activities:
            print(f"\n🔍 Exemple d'activité (ID 0):")
            act = instance.activities[0]
            print(f"  Durée: {act.duration}")
            print(f"  Prédécesseurs: {act.predecessors}")
            print(f"  Successeurs: {act.successors}")
            print(f"  Exigences: {act.skill_requirements}")
            print(f"  Earliest start: {act.earliest_start}")
            print(f"  Latest start: {act.latest_start}")
            print(f"  Slack: {act.slack}")
        
        # Examiner les ressources
        if instance.resources:
            print(f"\n🔍 Exemple de ressource (ID 0):")
            res = instance.resources[0]
            print(f"  Compétences: {res.skills}")
            print(f"  Niveaux: {res.skill_levels}")
        
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {str(e)}")


def main():
    """Programme principal de diagnostic"""
    print("🔬 DIAGNOSTIC DES INSTANCES MSRCPSP")
    print("=" * 60)
    
    instances_dir = "Instances"
    if not os.path.exists(instances_dir):
        print(f"❌ Répertoire {instances_dir} non trouvé!")
        return
    
    # Prendre quelques instances problématiques
    test_files = [
        "MSLIB_Set1_1000.msrcp",  # Tous donnent 4
        "MSLIB_Set1_1001.msrcp",  # Tous donnent 0
        "MSLIB_Set1_1003.msrcp",  # Tous donnent 21
        "MSLIB_Set1_101.msrcp",   # Résultats différents
        "MSLIB_Set1_1.msrcp"      # Résultats variés
    ]
    
    for filename in test_files:
        filepath = os.path.join(instances_dir, filename)
        if os.path.exists(filepath):
            diagnose_instance_issue(filepath)
        else:
            print(f"⚠️  Fichier {filename} non trouvé")
    
    print(f"\n{'='*60}")
    print("🎯 RECOMMANDATIONS:")
    print("1. Vérifier la logique de scheduling dans msrcpsp_final.py")
    print("2. Augmenter la diversité des règles de priorité")
    print("3. Implémenter des heuristiques plus sophistiquées")
    print("4. Ajouter de la randomisation pour briser les égalités")
    print("=" * 60)


if __name__ == "__main__":
    main()
