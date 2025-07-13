#!/usr/bin/env python3
"""
MSRCPSP Solver - Version finale optimisée
Intègre toutes les améliorations pour éviter les deadlocks et augmenter la diversité
"""

import os
import json
import csv
import sys
import random
import time
from msrcpsp_final import MSRCPSPParser, MSRCPSPScheduler


def run_enhanced_analysis():
    """Analyse avec diversification des résultats"""
    print("🚀 MSRCPSP Solver - Analyse Complète Optimisée")
    print("=" * 55)
    
    # Vérifier le dossier Instances
    instances_dir = "Instances"
    if not os.path.exists(instances_dir):
        print(f"❌ Répertoire {instances_dir} non trouvé!")
        return
    
    # Lister toutes les instances
    all_files = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    if not all_files:
        print(f"❌ Aucun fichier .msrcp trouvé dans {instances_dir}!")
        return
    
    all_files.sort()
    
    # Prendre un échantillon plus large pour commencer
    sample_size = min(100, len(all_files))  # Augmenté de 20 à 100
    step = len(all_files) // sample_size
    sample_files = [all_files[i] for i in range(0, len(all_files), step)][:sample_size]
    
    print(f"📁 Échantillon de {len(sample_files)} instances sur {len(all_files)}")
    
    # Demander confirmation
    response = input(f"Traiter {len(sample_files)} instances? (o/N): ")
    if response.lower() != 'o':
        print("🛑 Analyse annulée")
        return
    
    # Créer répertoires de sortie
    os.makedirs("resultats", exist_ok=True)
    os.makedirs("resultats/enhanced_analysis", exist_ok=True)
    
    all_results = {}
    comparison_data = []
    algorithms = ["EST", "LFT", "MSLF", "SPT", "LPT", "FCFS", "LST"]
    
    # Statistiques pour le suivi
    diversity_stats = {
        'total_instances': 0,
        'high_diversity': 0,    # 5+ résultats uniques
        'medium_diversity': 0,  # 3-4 résultats uniques
        'low_diversity': 0,     # 1-2 résultats uniques
        'complete_success': 0,  # Toutes activités ordonnancées
        'partial_success': 0    # Certaines activités ordonnancées
    }
    
    print("\n🔄 Début du traitement...")
    start_time = time.time()
    
    for i, filename in enumerate(sample_files):
        instance_path = os.path.join(instances_dir, filename)
        instance_name = filename.replace('.msrcp', '')
        
        # Afficher le progrès
        progress = (i + 1) / len(sample_files) * 100
        print(f"\n📊 [{i+1:3d}/{len(sample_files)}] {progress:5.1f}% - {instance_name}")
        
        try:
            # Parser l'instance
            instance = MSRCPSPParser.parse_file(instance_path)
            scheduler = MSRCPSPScheduler(instance)
            
            results = {}
            row = {'Instance': instance_name}
            
            # Statistiques de l'instance
            activities_scheduled = []
            makespans = []
            
            # Tester chaque algorithme
            for alg in algorithms:
                try:
                    makespan, schedule = scheduler.schedule_with_priority(alg)
                    num_scheduled = len(schedule)
                    
                    results[alg] = {
                        'makespan': makespan,
                        'schedule': schedule,
                        'activities_scheduled': num_scheduled,
                        'completion_rate': num_scheduled / instance.num_activities
                    }
                    row[alg] = makespan
                    activities_scheduled.append(num_scheduled)
                    makespans.append(makespan)
                    
                    # Affichage avec statut
                    status = "✅" if num_scheduled == instance.num_activities else "⚠️"
                    print(f"    {status} {alg}: {makespan:3d} ({num_scheduled:2d}/{instance.num_activities})")
                    
                except Exception as e:
                    results[alg] = {
                        'makespan': float('inf'),
                        'schedule': [],
                        'activities_scheduled': 0,
                        'completion_rate': 0,
                        'error': str(e)
                    }
                    row[alg] = float('inf')
                    print(f"    ❌ {alg}: Erreur - {str(e)[:50]}")
            
            all_results[instance_name] = results
            comparison_data.append(row)
            
            # Analyser la diversité de cette instance
            valid_makespans = [m for m in makespans if m != float('inf')]
            unique_makespans = len(set(valid_makespans)) if valid_makespans else 0
            max_activities = max(activities_scheduled) if activities_scheduled else 0
            
            diversity_stats['total_instances'] += 1
            if max_activities == instance.num_activities:
                diversity_stats['complete_success'] += 1
            elif max_activities > 0:
                diversity_stats['partial_success'] += 1
                
            if unique_makespans >= 5:
                diversity_stats['high_diversity'] += 1
                print(f"    🌟 Diversité élevée: {unique_makespans} résultats uniques")
            elif unique_makespans >= 3:
                diversity_stats['medium_diversity'] += 1
                print(f"    🔸 Diversité moyenne: {unique_makespans} résultats uniques")
            else:
                diversity_stats['low_diversity'] += 1
                if unique_makespans <= 1:
                    print(f"    ⚠️ Faible diversité: {unique_makespans} résultat unique")
            
        except Exception as e:
            print(f"    ❌ Erreur instance: {str(e)}")
            continue
    
    elapsed_time = time.time() - start_time
    
    # Sauvegarder les résultats
    save_enhanced_results(all_results, comparison_data, algorithms)
    
    # Générer les statistiques finales
    generate_enhanced_statistics(comparison_data, algorithms, diversity_stats, elapsed_time)
    
    print("\n" + "=" * 55)
    print("✅ Analyse optimisée terminée!")
    print("📁 Résultats disponibles dans le dossier 'resultats/'")


def save_enhanced_results(all_results, comparison_data, algorithms):
    """Sauvegarde les résultats avec plus de détails"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Fichier de comparaison principal
    comparison_file = f"resultats/enhanced_comparison_{timestamp}.csv"
    with open(comparison_file, 'w', newline='') as f:
        fieldnames = ['Instance'] + algorithms
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_data)
    
    # Résultats détaillés
    detail_file = f"resultats/enhanced_analysis/detailed_results_{timestamp}.json"
    with open(detail_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"💾 Résultats sauvegardés:")
    print(f"    📊 Comparaison: {comparison_file}")
    print(f"    📄 Détails: {detail_file}")


def generate_enhanced_statistics(comparison_data, algorithms, diversity_stats, elapsed_time):
    """Génère des statistiques améliorées"""
    print("\n📊 Génération des statistiques avancées...")
    
    stats = []
    algorithm_performance = {}
    
    for alg in algorithms:
        makespans = [row[alg] for row in comparison_data if row[alg] != float('inf')]
        
        if makespans:
            avg_makespan = sum(makespans) / len(makespans)
            min_makespan = min(makespans)
            max_makespan = max(makespans)
            
            # Compter les victoires (meilleur résultat)
            best_count = 0
            tied_best_count = 0
            
            for row in comparison_data:
                valid_makespans = [row[a] for a in algorithms if row[a] != float('inf')]
                if valid_makespans:
                    best_makespan = min(valid_makespans)
                    if row[alg] == best_makespan:
                        algorithms_with_best = sum(1 for a in algorithms if row[a] == best_makespan)
                        if algorithms_with_best == 1:
                            best_count += 1
                        else:
                            tied_best_count += 1
            
            algorithm_performance[alg] = {
                'avg_makespan': avg_makespan,
                'wins': best_count,
                'tied_wins': tied_best_count,
                'solved_instances': len(makespans)
            }
            
            stats.append({
                'Algorithm': alg,
                'Average_Makespan': round(avg_makespan, 2),
                'Min_Makespan': min_makespan,
                'Max_Makespan': max_makespan,
                'Solo_Wins': best_count,
                'Tied_Wins': tied_best_count,
                'Total_Solved': len(makespans),
                'Success_Rate': round(len(makespans) / len(comparison_data) * 100, 1)
            })
        else:
            stats.append({
                'Algorithm': alg,
                'Average_Makespan': 'N/A',
                'Min_Makespan': 'N/A',
                'Max_Makespan': 'N/A',
                'Solo_Wins': 0,
                'Tied_Wins': 0,
                'Total_Solved': 0,
                'Success_Rate': 0
            })
    
    # Sauvegarder les statistiques
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    stats_file = f"resultats/enhanced_statistics_{timestamp}.csv"
    with open(stats_file, 'w', newline='') as f:
        fieldnames = ['Algorithm', 'Average_Makespan', 'Min_Makespan', 'Max_Makespan', 
                     'Solo_Wins', 'Tied_Wins', 'Total_Solved', 'Success_Rate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stats)
    
    # Afficher le résumé détaillé
    print("\n" + "=" * 65)
    print("📈 RÉSUMÉ DES PERFORMANCES AVANCÉES")
    print("=" * 65)
    
    # Classement par victoires
    stats_sorted = sorted(stats, key=lambda x: (x['Solo_Wins'], x['Tied_Wins']), reverse=True)
    
    for i, stat in enumerate(stats_sorted):
        rank_icon = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1:2d}."
        print(f"\n{rank_icon} {stat['Algorithm']}:")
        print(f"    📊 Makespan moyen: {stat['Average_Makespan']}")
        print(f"    🏆 Victoires solo: {stat['Solo_Wins']}")
        print(f"    🤝 Victoires ex-æquo: {stat['Tied_Wins']}")
        print(f"    ✅ Taux de succès: {stat['Success_Rate']}%")
    
    # Statistiques de diversité
    print(f"\n" + "=" * 65)
    print("🎨 ANALYSE DE LA DIVERSITÉ")
    print("=" * 65)
    total = diversity_stats['total_instances']
    print(f"📊 Instances traitées: {total}")
    print(f"🌟 Haute diversité (5+ résultats): {diversity_stats['high_diversity']} ({diversity_stats['high_diversity']/total*100:.1f}%)")
    print(f"🔸 Diversité moyenne (3-4 résultats): {diversity_stats['medium_diversity']} ({diversity_stats['medium_diversity']/total*100:.1f}%)")
    print(f"⚠️  Faible diversité (1-2 résultats): {diversity_stats['low_diversity']} ({diversity_stats['low_diversity']/total*100:.1f}%)")
    print(f"\n✅ Résolution complète: {diversity_stats['complete_success']} ({diversity_stats['complete_success']/total*100:.1f}%)")
    print(f"⚠️  Résolution partielle: {diversity_stats['partial_success']} ({diversity_stats['partial_success']/total*100:.1f}%)")
    
    print(f"\n⏱️  Temps d'exécution: {elapsed_time:.1f} secondes")
    print(f"📄 Statistiques détaillées: {stats_file}")


def main():
    """Menu principal amélioré"""
    print("🚀 MSRCPSP Solver - Version Finale Optimisée")
    print("=" * 50)
    print("1️⃣  Analyse optimisée (échantillon représentatif)")
    print("2️⃣  Analyse complète (toutes les instances)")
    print("3️⃣  Test rapide (diagnostic)")
    print("0️⃣  Quitter")
    
    try:
        choice = input("\nVotre choix (0-3): ").strip()
        
        if choice == "1":
            run_enhanced_analysis()
        elif choice == "2":
            # Importer depuis le module complet
            from msrcpsp_complete import run_full_analysis
            run_full_analysis()
        elif choice == "3":
            # Diagnostic
            os.system("python diagnostic.py")
        elif choice == "0":
            print("👋 Au revoir!")
        else:
            print("❌ Choix invalide")
    
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")


if __name__ == "__main__":
    main()
