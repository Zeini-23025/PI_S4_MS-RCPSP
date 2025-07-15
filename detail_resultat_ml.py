#!/usr/bin/env python3
"""
🔍 VISUALISATEUR DÉTAILLÉ DES RÉSULTATS ML
==========================================

Ce script permet de voir en détail un résultat ML spécifique
"""

import os
import json
from datetime import datetime

def lire_resultat_ml_detaille(filename=None):
    """Lit et affiche en détail un résultat ML"""
    
    print("🔍 VISUALISATEUR DÉTAILLÉ DES RÉSULTATS ML")
    print("=" * 60)
    
    resultats_dir = "./resultats_ml"
    
    if not os.path.exists(resultats_dir):
        print(f"❌ Dossier {resultats_dir} non trouvé !")
        return
    
    # Lister tous les fichiers
    json_files = [f for f in os.listdir(resultats_dir) if f.endswith('.json')]
    
    if not json_files:
        print("❌ Aucun résultat ML trouvé !")
        return
    
    # Si pas de fichier spécifié, prendre le premier
    if not filename:
        filename = json_files[0]
        print(f"📄 Fichier choisi automatiquement : {filename}")
    
    filepath = os.path.join(resultats_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier {filename} non trouvé !")
        print(f"📋 Fichiers disponibles : {json_files}")
        return
    
    # Lire le fichier
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Fichier chargé : {filename}")
        print()
        
        # Informations générales
        print("📋 INFORMATIONS GÉNÉRALES")
        print("-" * 30)
        print(f"🎯 Projet analysé    : {data.get('instance', 'N/A')}")
        print(f"📅 Date de création  : {data.get('timestamp', 'N/A')}")
        print(f"⏱️  Temps de calcul   : {data.get('computation_time', 'N/A')} secondes")
        print()
        
        # Recommandations de l'IA
        print("🤖 RECOMMANDATIONS DE L'INTELLIGENCE ARTIFICIELLE")
        print("-" * 50)
        ml_algos = data.get('ml_recommended_algorithms', [])
        print(f"📊 Nombre d'algorithmes recommandés : {len(ml_algos)}")
        
        for i, algo in enumerate(ml_algos):
            print(f"   {i+1}. {algo}")
        
        print()
        
        # Résultat optimal trouvé
        print("🏆 MEILLEUR RÉSULTAT TROUVÉ")
        print("-" * 30)
        best_algo = data.get('best_algorithm', 'N/A')
        best_makespan = data.get('best_makespan', 'N/A')
        
        print(f"🥇 Algorithme optimal  : {best_algo}")
        print(f"⏰ Makespan optimal    : {best_makespan} jours")
        
        # Vérifier si l'IA avait raison
        if best_algo in ml_algos:
            rank = ml_algos.index(best_algo) + 1
            print(f"✅ IA avait raison ! (recommandé en position {rank})")
        else:
            print(f"❌ IA s'est trompée (n'avait pas recommandé {best_algo})")
        
        print()
        
        # Tous les résultats détaillés
        print("📊 TOUS LES RÉSULTATS DÉTAILLÉS")
        print("-" * 40)
        
        all_results = data.get('all_results', {})
        
        if all_results:
            # Trier par makespan
            results_sorted = sorted(all_results.items(), 
                                  key=lambda x: x[1].get('makespan', float('inf')))
            
            print(f"📈 Comparaison des {len(results_sorted)} algorithmes testés :")
            print()
            
            for i, (algo, result) in enumerate(results_sorted):
                makespan = result.get('makespan', 'N/A')
                time_taken = result.get('computation_time', 'N/A')
                
                # Icône selon le rang
                if i == 0:
                    icon = "🥇"
                elif i == 1:
                    icon = "🥈"
                elif i == 2:
                    icon = "🥉"
                else:
                    icon = f"{i+1:2d}."
                
                # Indiquer si recommandé par l'IA
                ml_mark = "🤖" if algo in ml_algos else "  "
                
                print(f"   {icon} {ml_mark} {algo:4s} : {makespan:>6} jours ({time_taken} sec)")
            
            # Calcul des écarts
            print()
            print("📈 ANALYSE DES ÉCARTS")
            print("-" * 25)
            
            best_makespan_val = float(best_makespan) if best_makespan != 'N/A' else None
            
            if best_makespan_val:
                for algo, result in all_results.items():
                    makespan = result.get('makespan', None)
                    if makespan and makespan != best_makespan_val:
                        ecart = makespan - best_makespan_val
                        ecart_pct = (ecart / best_makespan_val) * 100
                        print(f"   {algo:4s} : +{ecart:>4.0f} jours (+{ecart_pct:>4.1f}%)")
        
        # Performance de l'IA sur ce projet
        print()
        print("🎯 PERFORMANCE DE L'IA SUR CE PROJET")
        print("-" * 40)
        
        if best_algo in ml_algos:
            print("✅ SUCCÈS ! L'IA a recommandé l'algorithme optimal")
            rank = ml_algos.index(best_algo) + 1
            print(f"   Position dans les recommandations : {rank}/{len(ml_algos)}")
        else:
            print("❌ ÉCHEC ! L'IA n'a pas recommandé l'optimal")
            if all_results and best_algo in all_results:
                # Voir si l'IA était proche
                ml_makespans = []
                for algo in ml_algos:
                    if algo in all_results:
                        ml_makespans.append(all_results[algo].get('makespan', float('inf')))
                
                if ml_makespans:
                    best_ml = min(ml_makespans)
                    if best_ml != float('inf') and best_makespan_val:
                        ecart = best_ml - best_makespan_val
                        ecart_pct = (ecart / best_makespan_val) * 100
                        print(f"   Meilleur parmi recommandés : {best_ml} jours")
                        print(f"   Écart avec optimal : +{ecart:.0f} jours (+{ecart_pct:.1f}%)")
        
        # Conseils
        print()
        print("💡 CONSEILS POUR CE PROJET")
        print("-" * 30)
        
        if len(ml_algos) >= 5:
            print("🎯 L'IA est très confiante (recommande 5+ algorithmes)")
            print("   → Probablement un projet avec plusieurs bonnes solutions")
        elif len(ml_algos) <= 2:
            print("🎯 L'IA est très sélective (recommande ≤2 algorithmes)")
            print("   → Probablement un projet avec contraintes spécifiques")
        
        if best_algo in ['EST', 'LFT']:
            print("📋 L'optimal est un algorithme de priorité temporelle")
            print("   → Projet où l'ordre chronologique est critique")
        elif best_algo in ['SPT', 'LPT']:
            print("📋 L'optimal est un algorithme de priorité par durée")
            print("   → Projet où la gestion des tâches courtes/longues compte")
        elif best_algo in ['LST', 'MSLF']:
            print("📋 L'optimal est un algorithme de priorité par slack/skills")
            print("   → Projet où les ressources et compétences sont critiques")
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")

def comparer_plusieurs_resultats():
    """Compare plusieurs résultats ML"""
    
    print("\n🔄 COMPARAISON DE PLUSIEURS RÉSULTATS")
    print("=" * 50)
    
    resultats_dir = "./resultats_ml"
    json_files = [f for f in os.listdir(resultats_dir) if f.endswith('.json')]
    
    if len(json_files) < 2:
        print("❌ Pas assez de résultats pour comparaison")
        return
    
    # Lire tous les résultats
    all_data = []
    for filename in json_files:
        filepath = os.path.join(resultats_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['filename'] = filename
                all_data.append(data)
        except:
            continue
    
    if not all_data:
        return
    
    print(f"📊 Comparaison de {len(all_data)} projets")
    print()
    
    # Statistiques de réussite IA
    succes_ia = 0
    total_projets = len(all_data)
    
    print("🎯 RÉSUMÉ PAR PROJET")
    print("-" * 25)
    
    for data in all_data:
        instance = data.get('instance', 'N/A')
        best_algo = data.get('best_algorithm', 'N/A')
        ml_algos = data.get('ml_recommended_algorithms', [])
        best_makespan = data.get('best_makespan', 'N/A')
        
        ia_succes = best_algo in ml_algos
        if ia_succes:
            succes_ia += 1
        
        status = "✅" if ia_succes else "❌"
        print(f"   {status} {instance[:15]:15s} : {best_algo:4s} = {best_makespan:>6} jours")
    
    print()
    print("📈 STATISTIQUES GLOBALES")
    print("-" * 30)
    print(f"🎯 Taux de réussite IA : {succes_ia}/{total_projets} ({succes_ia/total_projets*100:.1f}%)")
    
    # Algorithmes les plus performants
    algo_wins = {}
    makespans = []
    
    for data in all_data:
        best_algo = data.get('best_algorithm')
        if best_algo:
            algo_wins[best_algo] = algo_wins.get(best_algo, 0) + 1
        
        makespan = data.get('best_makespan')
        if makespan:
            makespans.append(makespan)
    
    print("\n🏆 Algorithmes les plus souvent optimaux :")
    for algo, wins in sorted(algo_wins.items(), key=lambda x: x[1], reverse=True):
        print(f"   {algo} : {wins} fois ({wins/total_projets*100:.1f}%)")
    
    if makespans:
        print(f"\n📊 Makespans globaux :")
        print(f"   Min : {min(makespans):.0f} jours")
        print(f"   Max : {max(makespans):.0f} jours")
        print(f"   Moy : {sum(makespans)/len(makespans):.1f} jours")

def main():
    """Fonction principale"""
    
    # Lire un résultat en détail
    lire_resultat_ml_detaille()
    
    # Comparer plusieurs résultats
    comparer_plusieurs_resultats()
    
    print("\n🎊 ANALYSE TERMINÉE !")
    print("\n💡 POUR VOIR D'AUTRES FICHIERS :")
    print("   python3 detail_resultat_ml.py")

if __name__ == "__main__":
    main()
