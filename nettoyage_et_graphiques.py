#!/usr/bin/env python3
"""
🧹 NETTOYAGE ET VISUALISATION
=============================

Ce script supprime les fichiers non nécessaires et ajoute des graphiques
"""

import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pathlib import Path

def supprimer_fichiers_inutiles():
    """Supprime les fichiers redondants et non nécessaires"""
    
    print("🧹 NETTOYAGE DES FICHIERS NON NÉCESSAIRES")
    print("=" * 60)
    
    # Fichiers à supprimer (redondants ou obsolètes)
    fichiers_a_supprimer = [
        "demo.py",  # Redondant avec demo_explication_simple.py
        "diagnostic.py",  # Remplacé par solution_finale.py
        "exemple_ml.py",  # Redondant avec demo_ml_integration.py
        "msrcpsp_optimized.py",  # Version obsolète
        "improved_scheduler.py",  # Intégré dans msrcpsp_final.py
        "test_automatique.py",  # Remplacé par test_massif_projets.py
        "demo_complete_system.py",  # Redondant
        "lire_pkl.py",  # Fonctionnalité intégrée ailleurs
    ]
    
    # Fichiers à garder (essentiels)
    fichiers_essentiels = [
        "msrcpsp_final.py",  # Core scheduler
        "binary_relevance_msrcpsp.py",  # Core ML
        "makespan_calculator.py",  # Data generator
        "msrcpsp_complete.py",  # Batch processing
        "assistant_ml.py",  # Simple interface
        "solution_finale.py",  # Diagnostic tool
        "explication_algorithme_ml.py",  # Results viewer
        "detail_resultat_ml.py",  # Detailed analysis
        "test_massif_projets.py",  # Mass testing
        "demo_explication_simple.py",  # Simple demo
        "demo_ml_integration.py",  # ML integration demo
        "project.sh",  # Automation script
    ]
    
    fichiers_supprimes = 0
    
    for fichier in fichiers_a_supprimer:
        if os.path.exists(fichier):
            try:
                os.remove(fichier)
                print(f"🗑️  Supprimé: {fichier}")
                fichiers_supprimes += 1
            except Exception as e:
                print(f"❌ Erreur suppression {fichier}: {e}")
        else:
            print(f"ℹ️  Déjà absent: {fichier}")
    
    print(f"\n✅ {fichiers_supprimes} fichiers supprimés")
    
    # Afficher les fichiers restants
    print(f"\n📁 FICHIERS PYTHON RESTANTS:")
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    for f in sorted(python_files):
        if f in fichiers_essentiels:
            print(f"   ✅ {f} (essentiel)")
        else:
            print(f"   ⚠️  {f} (à vérifier)")

def creer_graphiques_makespan():
    """Crée des graphiques pour les résultats de makespan"""
    
    print("\n📊 CRÉATION DES GRAPHIQUES MAKESPAN")
    print("=" * 50)
    
    # Chercher les données de makespan
    resultats_dir = "./resultats"
    makespan_details_dir = os.path.join(resultats_dir, "makespan_details")
    
    if not os.path.exists(makespan_details_dir):
        print("❌ Dossier makespan_details non trouvé")
        return
    
    # Créer dossier pour graphiques
    graphiques_dir = os.path.join(resultats_dir, "graphiques")
    os.makedirs(graphiques_dir, exist_ok=True)
    
    # Lire tous les fichiers JSON de makespan
    all_data = []
    json_files = [f for f in os.listdir(makespan_details_dir) if f.endswith('.json')]
    
    print(f"📄 Lecture de {len(json_files)} fichiers de données...")
    
    for json_file in json_files:
        try:
            with open(os.path.join(makespan_details_dir, json_file), 'r') as f:
                data = json.load(f)
                all_data.append(data)
        except Exception as e:
            print(f"❌ Erreur lecture {json_file}: {e}")
    
    if not all_data:
        print("❌ Aucune donnée trouvée")
        return
    
    # Convertir en DataFrame
    df_list = []
    for data in all_data:
        instance = data['instance']
        for algo, result in data['results'].items():
            df_list.append({
                'Instance': instance,
                'Algorithme': algo,
                'Makespan': result['makespan']
            })
    
    df = pd.DataFrame(df_list)
    
    # Style des graphiques
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Graphique en barres - Performance moyenne par algorithme
    plt.figure(figsize=(12, 8))
    avg_makespan = df.groupby('Algorithme')['Makespan'].mean().sort_values()
    
    plt.subplot(2, 2, 1)
    bars = plt.bar(avg_makespan.index, avg_makespan.values, 
                   color=sns.color_palette("viridis", len(avg_makespan)))
    plt.title('Makespan Moyen par Algorithme', fontsize=14, fontweight='bold')
    plt.xlabel('Algorithme')
    plt.ylabel('Makespan Moyen (jours)')
    plt.xticks(rotation=45)
    
    # Ajouter les valeurs sur les barres
    for bar, value in zip(bars, avg_makespan.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Boxplot - Distribution des makespans
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df, x='Algorithme', y='Makespan')
    plt.title('Distribution des Makespans', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    
    # 3. Heatmap - Comparaison par instance (échantillon)
    plt.subplot(2, 2, 3)
    # Prendre un échantillon d'instances pour la lisibilité
    sample_instances = df['Instance'].unique()[:15]
    df_sample = df[df['Instance'].isin(sample_instances)]
    pivot_data = df_sample.pivot(index='Instance', columns='Algorithme', values='Makespan')
    
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='RdYlGn_r', cbar_kws={'label': 'Makespan'})
    plt.title('Heatmap Makespans (Échantillon)', fontsize=14, fontweight='bold')
    plt.xlabel('Algorithme')
    plt.ylabel('Instance')
    
    # 4. Graphique de victoires
    plt.subplot(2, 2, 4)
    victories = []
    for instance in df['Instance'].unique():
        instance_data = df[df['Instance'] == instance]
        best_algo = instance_data.loc[instance_data['Makespan'].idxmin(), 'Algorithme']
        victories.append(best_algo)
    
    victory_counts = pd.Series(victories).value_counts()
    colors = sns.color_palette("Set2", len(victory_counts))
    wedges, texts, autotexts = plt.pie(victory_counts.values, labels=victory_counts.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Pourcentage de Victoires par Algorithme', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Sauvegarder
    graphique_path = os.path.join(graphiques_dir, "analyse_makespan.png")
    plt.savefig(graphique_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvé: {graphique_path}")
    
    plt.show()
    
    # Créer un graphique séparé pour les tendances
    plt.figure(figsize=(15, 6))
    
    # Graphique linéaire des performances
    for algo in df['Algorithme'].unique():
        algo_data = df[df['Algorithme'] == algo].sort_values('Instance')
        plt.plot(range(len(algo_data)), algo_data['Makespan'], 
                marker='o', label=algo, alpha=0.7, linewidth=2)
    
    plt.title('Évolution des Makespans par Instance', fontsize=16, fontweight='bold')
    plt.xlabel('Index d\'Instance')
    plt.ylabel('Makespan (jours)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Sauvegarder
    tendance_path = os.path.join(graphiques_dir, "tendances_makespan.png")
    plt.savefig(tendance_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvé: {tendance_path}")
    
    plt.show()

def creer_graphiques_ml():
    """Crée des graphiques pour les résultats ML"""
    
    print("\n🤖 CRÉATION DES GRAPHIQUES MACHINE LEARNING")
    print("=" * 60)
    
    # Chercher les résultats ML
    resultats_ml_dir = "./resultats_ml"
    
    if not os.path.exists(resultats_ml_dir):
        print("❌ Dossier resultats_ml non trouvé")
        return
    
    # Créer dossier pour graphiques
    graphiques_dir = os.path.join("./resultats", "graphiques")
    os.makedirs(graphiques_dir, exist_ok=True)
    
    # Lire tous les résultats ML
    ml_data = []
    json_files = [f for f in os.listdir(resultats_ml_dir) if f.endswith('.json')]
    
    print(f"📄 Lecture de {len(json_files)} résultats ML...")
    
    for json_file in json_files:
        try:
            with open(os.path.join(resultats_ml_dir, json_file), 'r') as f:
                data = json.load(f)
                ml_data.append(data)
        except Exception as e:
            print(f"❌ Erreur lecture {json_file}: {e}")
    
    if not ml_data:
        print("❌ Aucun résultat ML trouvé")
        return
    
    # Analyser les données ML
    ia_predictions = []
    optimal_results = []
    all_results = []
    
    for data in ml_data:
        instance = data.get('instance', 'Unknown')
        ml_recommended = data.get('ml_recommended_algorithms', [])
        best_algo = data.get('best_algorithm', 'Unknown')
        best_makespan = data.get('best_makespan', 0)
        all_res = data.get('all_results', {})
        
        # Vérifier si l'IA avait raison
        ia_correcte = best_algo in ml_recommended
        
        ia_predictions.append({
            'Instance': instance,
            'IA_Correcte': ia_correcte,
            'Meilleur_Algo': best_algo,
            'Makespan': best_makespan,
            'NB_Recommandes': len(ml_recommended)
        })
        
        # Analyser tous les résultats
        for algo, result in all_res.items():
            makespan = result.get('makespan', 0)
            all_results.append({
                'Instance': instance,
                'Algorithme': algo,
                'Makespan': makespan,
                'Est_Recommande': algo in ml_recommended,
                'Est_Optimal': algo == best_algo
            })
    
    df_predictions = pd.DataFrame(ia_predictions)
    df_all = pd.DataFrame(all_results)
    
    # Créer les graphiques ML
    plt.figure(figsize=(15, 10))
    
    # 1. Taux de succès de l'IA
    plt.subplot(2, 3, 1)
    success_rate = df_predictions['IA_Correcte'].mean() * 100
    labels = ['Succès IA', 'Échec IA']
    sizes = [success_rate, 100 - success_rate]
    colors = ['#28a745', '#dc3545']
    
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                      colors=colors, startangle=90)
    plt.title(f'Taux de Succès de l\'IA\n({success_rate:.1f}%)', 
              fontsize=14, fontweight='bold')
    
    # 2. Performance des algorithmes recommandés vs non recommandés
    plt.subplot(2, 3, 2)
    recommande_data = df_all[df_all['Est_Recommande']]['Makespan']
    non_recommande_data = df_all[~df_all['Est_Recommande']]['Makespan']
    
    plt.boxplot([recommande_data, non_recommande_data], 
                labels=['Recommandés\npar IA', 'Non\nRecommandés'])
    plt.title('Performance: Recommandés vs Non-Recommandés', 
              fontsize=14, fontweight='bold')
    plt.ylabel('Makespan (jours)')
    
    # 3. Fréquence des algorithmes recommandés
    plt.subplot(2, 3, 3)
    algo_recommendations = []
    for data in ml_data:
        algo_recommendations.extend(data.get('ml_recommended_algorithms', []))
    
    recommendation_counts = pd.Series(algo_recommendations).value_counts()
    bars = plt.bar(recommendation_counts.index, recommendation_counts.values,
                   color=sns.color_palette("Set3", len(recommendation_counts)))
    plt.title('Fréquence des Recommandations IA', fontsize=14, fontweight='bold')
    plt.xlabel('Algorithme')
    plt.ylabel('Nombre de Recommandations')
    plt.xticks(rotation=45)
    
    # Ajouter valeurs sur barres
    for bar, value in zip(bars, recommendation_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(value), ha='center', va='bottom', fontweight='bold')
    
    # 4. Heatmap de confusion IA
    plt.subplot(2, 3, 4)
    optimal_algos = df_predictions['Meilleur_Algo'].value_counts()
    confusion_matrix = np.zeros((len(optimal_algos), 2))
    
    for i, algo in enumerate(optimal_algos.index):
        successes = len(df_predictions[(df_predictions['Meilleur_Algo'] == algo) & 
                                     (df_predictions['IA_Correcte'] == True)])
        failures = len(df_predictions[(df_predictions['Meilleur_Algo'] == algo) & 
                                    (df_predictions['IA_Correcte'] == False)])
        confusion_matrix[i] = [successes, failures]
    
    sns.heatmap(confusion_matrix, annot=True, fmt='.0f', 
                xticklabels=['IA Succès', 'IA Échec'],
                yticklabels=optimal_algos.index,
                cmap='RdYlGn', cbar_kws={'label': 'Nombre de cas'})
    plt.title('Matrice de Performance IA', fontsize=14, fontweight='bold')
    
    # 5. Distribution des makespans par statut
    plt.subplot(2, 3, 5)
    optimal_makespans = df_all[df_all['Est_Optimal']]['Makespan']
    recommande_makespans = df_all[df_all['Est_Recommande'] & ~df_all['Est_Optimal']]['Makespan']
    autres_makespans = df_all[~df_all['Est_Recommande'] & ~df_all['Est_Optimal']]['Makespan']
    
    plt.hist([optimal_makespans, recommande_makespans, autres_makespans], 
             bins=15, alpha=0.7, 
             label=['Optimal', 'Recommandé (non-optimal)', 'Autres'],
             color=['gold', 'lightblue', 'lightcoral'])
    plt.title('Distribution des Makespans', fontsize=14, fontweight='bold')
    plt.xlabel('Makespan (jours)')
    plt.ylabel('Fréquence')
    plt.legend()
    
    # 6. Amélioration apportée par l'IA
    plt.subplot(2, 3, 6)
    ameliorations = []
    for data in ml_data:
        all_res = data.get('all_results', {})
        if len(all_res) > 1:
            makespans = [res.get('makespan', float('inf')) for res in all_res.values()]
            best_makespan = min(makespans)
            worst_makespan = max([ms for ms in makespans if ms != float('inf')])
            if worst_makespan != best_makespan:
                improvement = ((worst_makespan - best_makespan) / worst_makespan) * 100
                ameliorations.append(improvement)
    
    if ameliorations:
        plt.hist(ameliorations, bins=10, alpha=0.7, color='green', edgecolor='black')
        plt.title(f'Amélioration par l\'IA\n(Moyenne: {np.mean(ameliorations):.1f}%)', 
                  fontsize=14, fontweight='bold')
        plt.xlabel('Amélioration (%)')
        plt.ylabel('Nombre d\'Instances')
    
    plt.tight_layout()
    
    # Sauvegarder
    ml_graphique_path = os.path.join(graphiques_dir, "analyse_ml.png")
    plt.savefig(ml_graphique_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique ML sauvé: {ml_graphique_path}")
    
    plt.show()
    
    # Créer un rapport de performance IA
    print(f"\n📊 RAPPORT DE PERFORMANCE IA:")
    print(f"   🎯 Taux de succès: {success_rate:.1f}%")
    print(f"   📊 Instances testées: {len(df_predictions)}")
    if ameliorations:
        print(f"   📈 Amélioration moyenne: {np.mean(ameliorations):.1f}%")
    
    # Sauvegarder le rapport
    rapport_path = os.path.join(graphiques_dir, "rapport_performance_ia.json")
    rapport = {
        "taux_succes_ia": success_rate,
        "instances_testees": len(df_predictions),
        "amelioration_moyenne": np.mean(ameliorations) if ameliorations else 0,
        "algorithmes_les_plus_recommandes": recommendation_counts.to_dict(),
        "algorithmes_les_plus_optimaux": optimal_algos.to_dict()
    }
    
    with open(rapport_path, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Rapport sauvé: {rapport_path}")

def installer_dependances():
    """Installe les dépendances nécessaires pour les graphiques"""
    
    print("📦 INSTALLATION DES DÉPENDANCES")
    print("=" * 40)
    
    try:
        import matplotlib
        import seaborn
        import pandas
        import numpy
        print("✅ Toutes les dépendances sont déjà installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installation automatique...")
        
        import subprocess
        import sys
        
        packages = ['matplotlib', 'seaborn', 'pandas', 'numpy']
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} installé")
            except subprocess.CalledProcessError:
                print(f"❌ Échec installation {package}")
                return False
        
        return True

def main():
    """Fonction principale"""
    
    print("🎨 NETTOYAGE ET VISUALISATION MS-RCPSP")
    print("=" * 60)
    
    # Menu
    print("1. 🧹 Supprimer fichiers non nécessaires")
    print("2. 📊 Créer graphiques makespan")
    print("3. 🤖 Créer graphiques ML")
    print("4. 🎯 Tout faire (recommandé)")
    print("0. ❌ Quitter")
    
    choix = input("\nVotre choix (0-4): ").strip()
    
    if choix == "0":
        print("👋 Au revoir!")
        return
    
    # Installer les dépendances si nécessaire
    if choix in ["2", "3", "4"]:
        if not installer_dependances():
            print("❌ Impossible de créer les graphiques sans les dépendances")
            return
    
    if choix == "1":
        supprimer_fichiers_inutiles()
    elif choix == "2":
        creer_graphiques_makespan()
    elif choix == "3":
        creer_graphiques_ml()
    elif choix == "4":
        supprimer_fichiers_inutiles()
        creer_graphiques_makespan()
        creer_graphiques_ml()
        
        print(f"\n🎊 TERMINÉ !")
        print("✅ Fichiers nettoyés")
        print("✅ Graphiques créés")
        print("📁 Consultez le dossier resultats/graphiques/")
    else:
        print("❌ Choix invalide")

if __name__ == "__main__":
    main()
