#!/usr/bin/env python3
"""
🚀 LANCEUR COMPLET DU PROJET MS-RCPSP
=====================================

Ce script exécute automatiquement tout le projet :
- Génération des données de makespan
- Entraînement du modèle ML
- Tests et analyses
- Génération des graphiques
- Rapport final
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_banner():
    """Affiche la bannière du projet"""
    print("🚀" * 30)
    print("🎯 LANCEUR COMPLET MS-RCPSP PROJECT")
    print("🚀" * 30)
    print(f"📅 Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def print_step(step_num, title, description=""):
    """Affiche l'étape en cours"""
    print(f"\n{'='*60}")
    print(f"📋 ÉTAPE {step_num}: {title}")
    if description:
        print(f"   {description}")
    print(f"{'='*60}")

def run_command(command, description, show_output=True):
    """Exécute une commande et affiche le résultat"""
    print(f"⚙️  {description}")
    print(f"💻 Commande: {command}")
    print("-" * 40)
    
    start_time = time.time()
    
    try:
        if show_output:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=False, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Succès en {duration:.1f}s")
        return True, result
        
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"❌ Erreur après {duration:.1f}s")
        print(f"Code d'erreur: {e.returncode}")
        if hasattr(e, 'stdout') and e.stdout:
            print(f"Sortie: {e.stdout}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Erreur: {e.stderr}")
        
        return False, e

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print_step(0, "VÉRIFICATION DES DÉPENDANCES")
    
    required_packages = ['numpy', 'scikit-learn', 'matplotlib', 'pandas', 'seaborn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} manquant")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installation des packages manquants...")
        for package in missing_packages:
            success, _ = run_command(f"pip install {package}", 
                                   f"Installation de {package}", show_output=False)
            if not success:
                print(f"❌ Impossible d'installer {package}")
                return False
    
    print("✅ Toutes les dépendances sont disponibles")
    return True

def generate_makespan_data():
    """Génère les données de makespan"""
    print_step(1, "GÉNÉRATION DES DONNÉES MAKESPAN", 
               "Calcul des makespans pour l'entraînement ML")
    
    success, _ = run_command("python3 makespan_calculator.py", 
                           "Génération des données makespan")
    return success

def train_ml_model():
    """Entraîne le modèle ML"""
    print_step(2, "ENTRAÎNEMENT DU MODÈLE ML", 
               "Création du classificateur Binary Relevance")
    
    success, _ = run_command("python3 binary_relevance_msrcpsp.py", 
                           "Entraînement du modèle ML")
    return success

def run_mass_tests():
    """Exécute les tests massifs"""
    print_step(3, "TESTS MASSIFS", 
               "Tests sur plusieurs instances pour valider le système")
    
    success, _ = run_command("python3 solution_finale.py", 
                           "Exécution des tests massifs")
    return success

def create_visualizations():
    """Crée les visualisations et graphiques"""
    print_step(4, "CRÉATION DES GRAPHIQUES", 
               "Génération des visualisations pour l'analyse")
    
    # Créer les graphiques automatiquement (option 4 = tout faire)
    success, _ = run_command("echo '4' | python3 nettoyage_et_graphiques.py", 
                           "Création des graphiques et nettoyage")
    return success

def generate_detailed_analysis():
    """Génère l'analyse détaillée"""
    print_step(5, "ANALYSE DÉTAILLÉE", 
               "Génération du rapport d'analyse détaillé")
    
    # Analyser un résultat spécifique avec graphiques (option 1)
    success, _ = run_command("echo '1' | python3 detail_resultat_ml.py", 
                           "Analyse détaillée avec graphiques")
    return success

def show_project_status():
    """Affiche le statut final du projet"""
    print_step(6, "RAPPORT FINAL", 
               "Vérification de tous les résultats générés")
    
    # Vérifier les dossiers et fichiers créés
    directories_to_check = [
        "./resultats",
        "./resultats_ml", 
        "./resultats/graphiques",
        "./resultats/makespan_details"
    ]
    
    files_to_check = [
        "./resultats/binary_relevance_model.pkl",
        "./resultats/graphiques/analyse_makespan.png",
        "./resultats/graphiques/analyse_ml.png",
        "./resultats/graphiques/rapport_performance_ia.json"
    ]
    
    print("📁 VÉRIFICATION DES DOSSIERS:")
    all_dirs_ok = True
    for directory in directories_to_check:
        if os.path.exists(directory):
            count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
            print(f"   ✅ {directory} ({count} fichiers)")
        else:
            print(f"   ❌ {directory} manquant")
            all_dirs_ok = False
    
    print("\n📄 VÉRIFICATION DES FICHIERS CLÉS:")
    all_files_ok = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} manquant")
            all_files_ok = False
    
    # Compter les résultats ML
    ml_count = 0
    if os.path.exists("./resultats_ml"):
        ml_count = len([f for f in os.listdir("./resultats_ml") if f.endswith('.json')])
    
    print(f"\n📊 RÉSUMÉ FINAL:")
    print(f"   🤖 Résultats ML générés: {ml_count}")
    print(f"   📁 Dossiers: {'✅' if all_dirs_ok else '❌'}")
    print(f"   📄 Fichiers: {'✅' if all_files_ok else '❌'}")
    
    if all_dirs_ok and all_files_ok and ml_count > 0:
        print(f"\n🎊 PROJET COMPLÈTEMENT OPÉRATIONNEL ! 🎊")
        return True
    else:
        print(f"\n⚠️  Projet partiellement opérationnel")
        return False

def show_usage_instructions():
    """Affiche les instructions d'utilisation"""
    print("\n" + "="*60)
    print("💡 COMMENT UTILISER LE PROJET:")
    print("="*60)
    print("1️⃣  Pour l'assistant ML simple:")
    print("   python3 assistant_ml.py")
    print()
    print("2️⃣  Pour une démonstration complète:")
    print("   python3 demo_ml_integration.py")
    print()
    print("3️⃣  Pour l'analyse détaillée:")
    print("   python3 detail_resultat_ml.py")
    print()
    print("4️⃣  Pour voir les algorithmes ML:")
    print("   python3 explication_algorithme_ml.py")
    print()
    print("5️⃣  Pour des tests massifs:")
    print("   python3 solution_finale.py")
    print()
    print("📁 RÉSULTATS DANS:")
    print("   • ./resultats/graphiques/ (images)")
    print("   • ./resultats_ml/ (résultats JSON)")
    print("   • ./resultats/ (modèles et données)")

def main():
    """Fonction principale"""
    print_banner()
    
    start_time = time.time()
    steps_completed = 0
    total_steps = 6
    
    try:
        # Étape 0: Vérifier les dépendances
        if not check_dependencies():
            print("❌ Impossible de continuer sans les dépendances")
            sys.exit(1)
        
        # Étape 1: Générer les données makespan
        if generate_makespan_data():
            steps_completed += 1
            print("✅ Données makespan générées")
        else:
            print("⚠️  Problème avec la génération des données makespan")
        
        # Étape 2: Entraîner le modèle ML
        if train_ml_model():
            steps_completed += 1
            print("✅ Modèle ML entraîné")
        else:
            print("⚠️  Problème avec l'entraînement ML")
        
        # Étape 3: Tests massifs
        if run_mass_tests():
            steps_completed += 1
            print("✅ Tests massifs réalisés")
        else:
            print("⚠️  Problème avec les tests massifs")
        
        # Étape 4: Créer les visualisations
        if create_visualizations():
            steps_completed += 1
            print("✅ Graphiques créés")
        else:
            print("⚠️  Problème avec la création des graphiques")
        
        # Étape 5: Analyse détaillée
        if generate_detailed_analysis():
            steps_completed += 1
            print("✅ Analyse détaillée générée")
        else:
            print("⚠️  Problème avec l'analyse détaillée")
        
        # Étape 6: Rapport final
        if show_project_status():
            steps_completed += 1
            print("✅ Projet complètement opérationnel")
        else:
            print("⚠️  Projet partiellement fonctionnel")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt demandé par l'utilisateur")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
    
    finally:
        # Résumé final
        end_time = time.time()
        total_duration = end_time - start_time
        
        print(f"\n{'='*60}")
        print(f"🏁 EXÉCUTION TERMINÉE")
        print(f"{'='*60}")
        print(f"⏱️  Durée totale: {total_duration:.1f} secondes")
        print(f"✅ Étapes réussies: {steps_completed}/{total_steps}")
        print(f"📊 Taux de succès: {(steps_completed/total_steps)*100:.1f}%")
        
        if steps_completed == total_steps:
            print(f"\n🎉 FÉLICITATIONS ! PROJET 100% OPÉRATIONNEL ! 🎉")
            show_usage_instructions()
        else:
            print(f"\n⚠️  Projet partiellement fonctionnel ({steps_completed}/{total_steps} étapes)")
            print(f"💡 Vous pouvez relancer le script pour corriger les problèmes")

if __name__ == "__main__":
    main()
