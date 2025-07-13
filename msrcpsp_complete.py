#!/usr/bin/env python3
"""
MSRCPSP Solver - Version complète pour toutes les instances
"""

import os
import json
import csv
import sys
from msrcpsp_final import MSRCPSPParser, MSRCPSPScheduler


def run_full_analysis():
    """Analyse complète de toutes les instances"""
    print("🚀 MSRCPSP Solver - Analyse Complète")
    print("=" * 50)
    
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
    print(f"📁 {len(all_files)} instances trouvées")
    
    # Demander confirmation
    if len(all_files) > 50:
        response = input(f"⚠️  Traiter {len(all_files)} instances peut prendre du temps. Continuer? (o/N): ")
        if response.lower() != 'o':
            print("🛑 Analyse annulée")
            return
    
    # Créer répertoires de sortie
    os.makedirs("resultats", exist_ok=True)
    os.makedirs("resultats/full_analysis", exist_ok=True)
    
    all_results = {}
    comparison_data = []
    algorithms = ["EST", "LFT", "MSLF", "SPT"]
    
    print("\n🔄 Début du traitement...")
    
    for i, filename in enumerate(all_files):
        instance_path = os.path.join(instances_dir, filename)
        instance_name = filename.replace('.msrcp', '')
        
        # Afficher le progrès
        progress = (i + 1) / len(all_files) * 100
        print(f"\n📊 [{i+1:4d}/{len(all_files)}] {progress:5.1f}% - {instance_name}")
        
        try:
            # Parser l'instance
            instance = MSRCPSPParser.parse_file(instance_path)
            scheduler = MSRCPSPScheduler(instance)
            
            results = {}
            row = {'Instance': instance_name}
            
            # Tester chaque algorithme
            for alg in algorithms:
                try:
                    makespan, schedule = scheduler.schedule_with_priority(alg)
                    results[alg] = {
                        'makespan': makespan,
                        'schedule': schedule,
                        'activities_order': [s[0] for s in schedule]
                    }
                    row[alg] = makespan
                    print(f"    ✓ {alg}: {makespan}")
                except Exception as e:
                    results[alg] = {
                        'makespan': float('inf'),
                        'schedule': [],
                        'activities_order': [],
                        'error': str(e)
                    }
                    row[alg] = float('inf')
                    print(f"    ✗ {alg}: Erreur")
            
            all_results[instance_name] = results
            comparison_data.append(row)
            
            # Sauvegarder périodiquement
            if (i + 1) % 100 == 0 or i == len(all_files) - 1:
                save_results(all_results, comparison_data, algorithms)
                print(f"💾 Sauvegarde intermédiaire ({i+1} instances)")
        
        except Exception as e:
            print(f"    ❌ Erreur: {str(e)}")
            continue
    
    # Sauvegarder les résultats finaux
    save_results(all_results, comparison_data, algorithms)
    
    # Générer les statistiques
    generate_statistics(comparison_data, algorithms)
    
    print("\n" + "=" * 50)
    print("✅ Analyse complète terminée!")
    print("📁 Résultats disponibles dans le dossier 'resultats/'")


def save_results(all_results, comparison_data, algorithms):
    """Sauvegarde les résultats"""
    # Fichier de comparaison
    comparison_file = "resultats/full_comparison.csv"
    with open(comparison_file, 'w', newline='') as f:
        fieldnames = ['Instance'] + algorithms
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_data)
    
    # Résultats détaillés
    detail_file = "resultats/full_analysis/detailed_results.json"
    with open(detail_file, 'w') as f:
        json.dump(all_results, f, indent=2)


def generate_statistics(comparison_data, algorithms):
    """Génère les statistiques de performance"""
    print("\n📊 Génération des statistiques...")
    
    stats = []
    for alg in algorithms:
        makespans = [row[alg] for row in comparison_data if row[alg] != float('inf')]
        
        if makespans:
            avg_makespan = sum(makespans) / len(makespans)
            min_makespan = min(makespans)
            max_makespan = max(makespans)
            
            # Compter les victoires
            best_count = 0
            for row in comparison_data:
                valid_makespans = [row[a] for a in algorithms if row[a] != float('inf')]
                if valid_makespans and row[alg] == min(valid_makespans):
                    best_count += 1
            
            stats.append({
                'Algorithm': alg,
                'Average_Makespan': round(avg_makespan, 2),
                'Min_Makespan': min_makespan,
                'Max_Makespan': max_makespan,
                'Best_Count': best_count,
                'Total_Solved': len(makespans)
            })
        else:
            stats.append({
                'Algorithm': alg,
                'Average_Makespan': 'N/A',
                'Min_Makespan': 'N/A',
                'Max_Makespan': 'N/A',
                'Best_Count': 0,
                'Total_Solved': 0
            })
    
    # Sauvegarder les statistiques
    stats_file = "resultats/performance_statistics.csv"
    with open(stats_file, 'w', newline='') as f:
        fieldnames = ['Algorithm', 'Average_Makespan', 'Min_Makespan', 'Max_Makespan', 'Best_Count', 'Total_Solved']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stats)
    
    # Afficher le résumé
    print("\n" + "=" * 50)
    print("📈 RÉSUMÉ DES PERFORMANCES")
    print("=" * 50)
    
    for stat in sorted(stats, key=lambda x: x['Best_Count'], reverse=True):
        print(f"\n🔹 {stat['Algorithm']}:")
        print(f"    📊 Makespan moyen: {stat['Average_Makespan']}")
        print(f"    🏆 Victoires: {stat['Best_Count']}")
        print(f"    ✅ Instances résolues: {stat['Total_Solved']}")
    
    print(f"\n📄 Statistiques détaillées: {stats_file}")


def run_sample_analysis():
    """Analyse sur un échantillon d'instances"""
    print("🧪 MSRCPSP Solver - Analyse d'Échantillon")
    
    instances_dir = "Instances"
    if not os.path.exists(instances_dir):
        print(f"❌ Répertoire {instances_dir} non trouvé!")
        return
    
    all_files = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    if not all_files:
        print(f"❌ Aucun fichier .msrcp trouvé!")
        return
    
    all_files.sort()
    
    # Prendre un échantillon représentatif
    sample_size = min(20, len(all_files))
    step = len(all_files) // sample_size
    sample_files = [all_files[i] for i in range(0, len(all_files), step)][:sample_size]
    
    print(f"📊 Échantillon de {len(sample_files)} instances sur {len(all_files)}")
    
    # Traiter l'échantillon
    os.makedirs("resultats", exist_ok=True)
    
    all_results = {}
    comparison_data = []
    algorithms = ["EST", "LFT", "MSLF", "SPT"]
    
    for i, filename in enumerate(sample_files):
        instance_path = os.path.join(instances_dir, filename)
        instance_name = filename.replace('.msrcp', '')
        
        print(f"\n📊 [{i+1:2d}/{len(sample_files)}] {instance_name}")
        
        try:
            instance = MSRCPSPParser.parse_file(instance_path)
            scheduler = MSRCPSPScheduler(instance)
            
            results = {}
            row = {'Instance': instance_name}
            
            for alg in algorithms:
                try:
                    makespan, schedule = scheduler.schedule_with_priority(alg)
                    results[alg] = {
                        'makespan': makespan,
                        'schedule': schedule
                    }
                    row[alg] = makespan
                    print(f"    ✓ {alg}: {makespan}")
                except Exception:
                    row[alg] = float('inf')
                    print(f"    ✗ {alg}: Erreur")
            
            all_results[instance_name] = results
            comparison_data.append(row)
            
        except Exception as e:
            print(f"    ❌ Erreur: {str(e)}")
    
    # Sauvegarder les résultats
    comparison_file = "resultats/sample_comparison.csv"
    with open(comparison_file, 'w', newline='') as f:
        fieldnames = ['Instance'] + algorithms
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_data)
    
    print(f"\n📊 Résultats sauvegardés dans {comparison_file}")
    
    # Afficher résumé
    print("\n" + "=" * 40)
    print("📈 RÉSUMÉ DE L'ÉCHANTILLON")
    print("=" * 40)
    
    for row in comparison_data[:5]:  # Afficher les 5 premiers
        print(f"\n🔹 {row['Instance']}:")
        makespans = [(alg, row[alg]) for alg in algorithms if row[alg] != float('inf')]
        makespans.sort(key=lambda x: x[1])
        
        for i, (alg, makespan) in enumerate(makespans):
            symbol = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
            print(f"    {symbol} {alg}: {makespan}")


def main():
    """Menu principal"""
    print("🚀 MSRCPSP Solver - Sélection du Mode")
    print("=" * 40)
    print("1️⃣  Analyse complète (toutes les instances)")
    print("2️⃣  Analyse d'échantillon (20 instances)")
    print("3️⃣  Test rapide (3 instances spécifiques)")
    print("0️⃣  Quitter")
    
    try:
        choice = input("\nVotre choix (0-3): ").strip()
        
        if choice == "1":
            run_full_analysis()
        elif choice == "2":
            run_sample_analysis()
        elif choice == "3":
            # Importer et utiliser la fonction main du module principal
            from msrcpsp_final import main as test_main
            test_main()
        elif choice == "0":
            print("👋 Au revoir!")
        else:
            print("❌ Choix invalide")
    
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")


if __name__ == "__main__":
    main()
