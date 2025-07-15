#!/usr/bin/env python3
"""
🧪 TESTEUR MASSIF - TESTER TOUS LES PROJETS
==========================================

Ce script teste l'IA sur TOUS les projets disponibles
"""

import os
import time
import json
from binary_relevance_msrcpsp import MLIntegratedMSRCPSP

def tester_tous_les_projets():
    """Teste l'IA sur tous les projets disponibles"""
    
    print("🧪 TESTEUR MASSIF - TOUS LES PROJETS")
    print("=" * 60)
    
    # Vérifier le modèle
    model_path = "./resultats/binary_relevance_model.pkl"
    if not os.path.exists(model_path):
        print("❌ Modèle ML non trouvé !")
        print("💡 Exécutez './project.sh' pour créer le modèle")
        return
    
    # Créer l'instance ML
    try:
        ml_msrcpsp = MLIntegratedMSRCPSP(model_path)
        print("✅ Modèle ML chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        return
    
    # Lister tous les projets
    instances_dir = "./Instances"
    if not os.path.exists(instances_dir):
        print(f"❌ Dossier {instances_dir} non trouvé !")
        return
    
    all_instances = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    all_instances.sort()
    
    print(f"📁 Dossier source : {instances_dir}")
    print(f"📊 Nombre total de projets : {len(all_instances)}")
    
    # Demander combien tester
    print("\n🎯 COMBIEN DE PROJETS TESTER ?")
    print("1. 🚀 Test rapide (10 projets)")
    print("2. 📊 Test moyen (50 projets)")
    print("3. 🏗️ Test large (100 projets)")
    print("4. 🌍 TOUS LES PROJETS ! (peut prendre du temps)")
    print("5. 🎯 Nombre personnalisé")
    
    choix = input("\nVotre choix (1-5) : ").strip()
    
    if choix == "1":
        nb_projets = 10
    elif choix == "2":
        nb_projets = 50
    elif choix == "3":
        nb_projets = 100
    elif choix == "4":
        nb_projets = len(all_instances)
    elif choix == "5":
        try:
            nb_projets = int(input("Nombre de projets à tester : "))
        except:
            nb_projets = 10
    else:
        nb_projets = 10
    
    # Limiter au nombre disponible
    nb_projets = min(nb_projets, len(all_instances))
    test_instances = all_instances[:nb_projets]
    
    print(f"\n🎯 Test sur {nb_projets} projets")
    print("=" * 40)
    
    # Dossier de sortie
    output_dir = "./resultats_ml"
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables de suivi
    resultats_complets = []
    reussites = 0
    echecs = 0
    temps_total = 0
    ia_correcte = 0
    
    print("🔄 DÉMARRAGE DU TEST...")
    temps_debut = time.time()
    
    for i, filename in enumerate(test_instances):
        instance_path = os.path.join(instances_dir, filename)
        
        print(f"\n[{i+1:3d}/{nb_projets}] {filename}")
        
        try:
            temps_debut_instance = time.time()
            
            # Résoudre avec ML
            result = ml_msrcpsp.solve_with_ml_guidance(instance_path, output_dir)
            
            temps_fin_instance = time.time()
            temps_instance = temps_fin_instance - temps_debut_instance
            temps_total += temps_instance
            
            if result and 'best_makespan' in result:
                makespan = result['best_makespan']
                best_algo = result['best_algorithm']
                recommended = result['ml_recommended_algorithms']
                
                # Vérifier si l'IA avait raison
                ia_succes = best_algo in recommended
                if ia_succes:
                    ia_correcte += 1
                
                status_ia = "✅" if ia_succes else "❌"
                
                print(f"  {status_ia} Optimal: {best_algo} = {makespan} jours ({temps_instance:.1f}s)")
                print(f"     🤖 IA: {recommended}")
                
                # Sauver le résultat
                resultats_complets.append({
                    'instance': filename,
                    'best_algorithm': best_algo,
                    'best_makespan': makespan,
                    'ml_recommended': recommended,
                    'ia_correcte': ia_succes,
                    'temps': temps_instance
                })
                
                reussites += 1
            else:
                print(f"  ❌ Échec de résolution")
                echecs += 1
                
        except Exception as e:
            print(f"  ❌ Erreur: {str(e)[:50]}...")
            echecs += 1
        
        # Affichage du progrès toutes les 10 instances
        if (i + 1) % 10 == 0:
            temps_ecoule = time.time() - temps_debut
            vitesse = (i + 1) / temps_ecoule
            temps_restant = (nb_projets - (i + 1)) / vitesse if vitesse > 0 else 0
            
            print(f"\n📊 PROGRÈS: {i+1}/{nb_projets} ({(i+1)/nb_projets*100:.1f}%)")
            print(f"   ⏱️ Vitesse: {vitesse:.1f} projets/seconde")
            print(f"   ⏰ Temps restant estimé: {temps_restant/60:.1f} minutes")
    
    # Résultats finaux
    temps_total_reel = time.time() - temps_debut
    
    print("\n" + "="*60)
    print("🎊 RÉSULTATS FINAUX DU TEST MASSIF")
    print("="*60)
    
    print(f"📊 STATISTIQUES GÉNÉRALES:")
    print(f"   • Projets testés     : {nb_projets}")
    print(f"   • Réussites         : {reussites}")
    print(f"   • Échecs            : {echecs}")
    print(f"   • Taux de réussite  : {reussites/nb_projets*100:.1f}%")
    
    print(f"\n🤖 PERFORMANCE DE L'IA:")
    if reussites > 0:
        print(f"   • IA correcte       : {ia_correcte}/{reussites}")
        print(f"   • Taux de précision : {ia_correcte/reussites*100:.1f}%")
    
    print(f"\n⏱️ PERFORMANCE TEMPORELLE:")
    print(f"   • Temps total       : {temps_total_reel/60:.1f} minutes")
    print(f"   • Temps moyen/projet: {temps_total_reel/nb_projets:.2f} secondes")
    
    # Analyse des algorithmes
    if resultats_complets:
        print(f"\n🏆 ALGORITHMES LES PLUS PERFORMANTS:")
        algo_count = {}
        makespans = []
        
        for res in resultats_complets:
            algo = res['best_algorithm']
            algo_count[algo] = algo_count.get(algo, 0) + 1
            makespans.append(res['best_makespan'])
        
        for algo, count in sorted(algo_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {algo}: {count} fois ({count/len(resultats_complets)*100:.1f}%)")
        
        print(f"\n📊 MAKESPANS:")
        print(f"   • Minimum : {min(makespans):.0f} jours")
        print(f"   • Maximum : {max(makespans):.0f} jours")
        print(f"   • Moyenne : {sum(makespans)/len(makespans):.1f} jours")
    
    # Sauvegarder le rapport complet
    rapport_path = os.path.join(output_dir, "rapport_test_massif.json")
    rapport_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "nb_projets_testes": nb_projets,
        "reussites": reussites,
        "echecs": echecs,
        "ia_correcte": ia_correcte,
        "temps_total_minutes": temps_total_reel/60,
        "temps_moyen_seconde": temps_total_reel/nb_projets if nb_projets > 0 else 0,
        "resultats_detailles": resultats_complets
    }
    
    try:
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport_data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Rapport sauvé : {rapport_path}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde rapport : {e}")
    
    print(f"\n📁 Tous les résultats dans : {output_dir}")
    print(f"📄 Fichiers JSON créés : {len([f for f in os.listdir(output_dir) if f.endswith('.json')])}")
    
    print("\n🎯 COMMANDES POUR ANALYSER LES RÉSULTATS:")
    print("   python3 explication_algorithme_ml.py  # Voir tous les résultats")
    print("   python3 detail_resultat_ml.py         # Analyse détaillée")
    
    return resultats_complets

def test_rapide_echantillon():
    """Test rapide sur un échantillon représentatif"""
    
    print("🚀 TEST RAPIDE - ÉCHANTILLON REPRÉSENTATIF")
    print("=" * 60)
    
    # Sélectionner des projets variés
    instances_dir = "./Instances"
    all_instances = [f for f in os.listdir(instances_dir) if f.endswith('.msrcp')]
    
    # Prendre des projets à intervalles réguliers pour avoir de la variété
    step = max(1, len(all_instances) // 20)  # ~20 projets représentatifs
    echantillon = all_instances[::step][:20]
    
    print(f"📊 Sélection de {len(echantillon)} projets représentatifs")
    print(f"📁 Sur un total de {len(all_instances)} projets disponibles")
    
    # Lancer le test
    model_path = "./resultats/binary_relevance_model.pkl"
    if not os.path.exists(model_path):
        print("❌ Modèle non trouvé ! Lancez './project.sh'")
        return
    
    try:
        ml_msrcpsp = MLIntegratedMSRCPSP(model_path)
        output_dir = "./resultats_ml"
        
        reussites = 0
        ia_correcte = 0
        
        for i, filename in enumerate(echantillon):
            instance_path = os.path.join(instances_dir, filename)
            print(f"[{i+1:2d}/20] {filename[:20]}...", end=" ")
            
            try:
                result = ml_msrcpsp.solve_with_ml_guidance(instance_path, output_dir)
                if result and 'best_makespan' in result:
                    best_algo = result['best_algorithm']
                    recommended = result['ml_recommended_algorithms']
                    ia_succes = best_algo in recommended
                    
                    if ia_succes:
                        ia_correcte += 1
                    
                    status = "✅" if ia_succes else "❌"
                    print(f"{status} {best_algo}")
                    reussites += 1
                else:
                    print("❌ Échec")
            except:
                print("❌ Erreur")
        
        print(f"\n📊 RÉSULTAT RAPIDE:")
        print(f"   Réussites: {reussites}/20")
        print(f"   Précision IA: {ia_correcte}/{reussites} ({ia_correcte/reussites*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Menu principal"""
    
    print("🧪 TESTEUR DE PROJETS - MENU PRINCIPAL")
    print("=" * 50)
    print("1. 🚀 Test rapide (20 projets représentatifs)")
    print("2. 🏗️ Test personnalisé (choisir le nombre)")
    print("3. ❓ Aide")
    
    choix = input("\nVotre choix (1-3) : ").strip()
    
    if choix == "1":
        test_rapide_echantillon()
    elif choix == "2":
        tester_tous_les_projets()
    elif choix == "3":
        print("""
🎯 AIDE - COMMENT UTILISER CE TESTEUR

📋 OBJECTIF :
   Tester l'Intelligence Artificielle sur de nombreux projets
   pour mesurer sa performance réelle

🚀 TEST RAPIDE :
   • Sélectionne 20 projets variés automatiquement
   • Rapide (~2-3 minutes)
   • Donne une bonne idée de la performance

🏗️ TEST PERSONNALISÉ :
   • Vous choisissez combien de projets tester
   • Plus de projets = résultats plus précis
   • Peut prendre du temps pour de gros volumes

📊 RÉSULTATS :
   • Taux de réussite de l'IA
   • Algorithmes les plus performants
   • Temps de calcul moyen
   • Rapport détaillé en JSON

💡 CONSEILS :
   • Commencez par le test rapide
   • Si satisfait, lancez un test plus large
   • Les résultats sont sauvés dans resultats_ml/
""")
    else:
        test_rapide_echantillon()

if __name__ == "__main__":
    main()
