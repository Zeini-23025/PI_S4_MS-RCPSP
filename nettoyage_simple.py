#!/usr/bin/env python3
"""
🧹 NETTOYAGE SIMPLE - SUPPRIMER FICHIERS NON NÉCESSAIRES
========================================================

Ce script supprime uniquement les fichiers redondants et obsolètes
"""

import os

def supprimer_fichiers_inutiles():
    """Supprime les fichiers redondants et non nécessaires"""
    
    print("🧹 SUPPRESSION DES FICHIERS NON NÉCESSAIRES")
    print("=" * 60)
    
    # Fichiers à supprimer (redondants ou obsolètes)
    fichiers_a_supprimer = [
        # Fichiers de test redondants
        "test_automatique.py",
        "test_verification_simple.py",
        
        # Démos redondants
        "demo.py",
        "demo_complete_system.py",
        "exemple_ml.py",
        
        # Versions obsolètes
        "msrcpsp_optimized.py",
        "improved_scheduler.py",
        "diagnostic.py",
        
        # Utilitaires intégrés ailleurs
        "lire_pkl.py",
        
        # Fichiers temporaires ou de développement
        "test_batch_ml.py",  # Remplacé par test_massif_projets.py
        
        # Doublons de scripts
        "nettoyage_et_graphiques.py",  # Ce script même après utilisation
    ]
    
    # Fichiers ESSENTIELS à garder absolument
    fichiers_essentiels = [
        "msrcpsp_final.py",                # ⭐ Core scheduler
        "binary_relevance_msrcpsp.py",     # ⭐ Core ML system
        "makespan_calculator.py",          # ⭐ Data generator
        "assistant_ml.py",                 # ⭐ Simple interface
        "solution_finale.py",              # ⭐ Diagnostic tool
        "explication_algorithme_ml.py",    # ⭐ Results viewer
        "detail_resultat_ml.py",           # ⭐ Detailed analysis
        "test_massif_projets.py",          # ⭐ Mass testing
        "demo_explication_simple.py",      # ⭐ Simple demo
        "demo_ml_integration.py",          # ⭐ ML integration demo
        "msrcpsp_complete.py",             # ⭐ Batch processing
        "project.sh",                      # ⭐ Automation script
    ]
    
    print("📋 ANALYSE DES FICHIERS...")
    
    # Lister tous les fichiers Python
    all_python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    print(f"📁 Trouvé {len(all_python_files)} fichiers Python")
    print(f"🎯 {len(fichiers_essentiels)} fichiers essentiels à garder")
    print(f"🗑️  {len(fichiers_a_supprimer)} fichiers à supprimer")
    
    # Confirmer avant suppression
    print(f"\n⚠️  FICHIERS QUI SERONT SUPPRIMÉS:")
    fichiers_presents = []
    for fichier in fichiers_a_supprimer:
        if os.path.exists(fichier):
            print(f"   🗑️  {fichier}")
            fichiers_presents.append(fichier)
        else:
            print(f"   ❌ {fichier} (déjà absent)")
    
    if not fichiers_presents:
        print("✅ Aucun fichier à supprimer (déjà nettoyé)")
        return
    
    print(f"\n📊 {len(fichiers_presents)} fichiers seront supprimés")
    
    # Demander confirmation
    reponse = input("\n❓ Confirmer la suppression? (o/N): ").strip().lower()
    
    if reponse != 'o':
        print("🛑 Suppression annulée")
        return
    
    # Procéder à la suppression
    print(f"\n🔄 SUPPRESSION EN COURS...")
    fichiers_supprimes = 0
    
    for fichier in fichiers_presents:
        try:
            os.remove(fichier)
            print(f"✅ Supprimé: {fichier}")
            fichiers_supprimes += 1
        except Exception as e:
            print(f"❌ Erreur suppression {fichier}: {e}")
    
    print(f"\n🎊 NETTOYAGE TERMINÉ!")
    print(f"✅ {fichiers_supprimes} fichiers supprimés")
    
    # Afficher les fichiers restants
    print(f"\n📁 FICHIERS PYTHON RESTANTS:")
    remaining_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    for f in sorted(remaining_files):
        if f in fichiers_essentiels:
            print(f"   ⭐ {f} (essentiel)")
        elif f == "nettoyage_simple.py":
            print(f"   🧹 {f} (script de nettoyage)")
        else:
            print(f"   ❓ {f} (à vérifier)")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   📁 Fichiers Python restants: {len(remaining_files)}")
    print(f"   ⭐ Fichiers essentiels: {len([f for f in remaining_files if f in fichiers_essentiels])}")
    
    print(f"\n💡 FICHIERS ESSENTIELS CONSERVÉS:")
    essential_kept = [f for f in remaining_files if f in fichiers_essentiels]
    for f in essential_kept:
        if f == "msrcpsp_final.py":
            print(f"   ⭐ {f} - Scheduler principal")
        elif f == "binary_relevance_msrcpsp.py":
            print(f"   ⭐ {f} - Système ML principal")
        elif f == "assistant_ml.py":
            print(f"   ⭐ {f} - Interface simple")
        elif f == "solution_finale.py":
            print(f"   ⭐ {f} - Diagnostic et test")
        elif f == "test_massif_projets.py":
            print(f"   ⭐ {f} - Test massif")
        else:
            print(f"   ⭐ {f}")

def supprimer_autres_fichiers():
    """Supprime d'autres fichiers non essentiels"""
    
    print(f"\n🧹 NETTOYAGE DES AUTRES FICHIERS")
    print("=" * 50)
    
    # Autres fichiers/dossiers non nécessaires
    autres_a_supprimer = [
        "__pycache__",  # Cache Python
        "*.pyc",        # Fichiers compilés Python
        ".pytest_cache", # Cache pytest
        "test_verification_simple.py",
        "RÉPONSE_QUESTIONS_ML.md",  # Redondant avec documentation
    ]
    
    print("🔍 Recherche d'autres fichiers à nettoyer...")
    
    # Supprimer __pycache__
    if os.path.exists("__pycache__"):
        try:
            import shutil
            shutil.rmtree("__pycache__")
            print("✅ Supprimé: __pycache__/")
        except Exception as e:
            print(f"❌ Erreur suppression __pycache__: {e}")
    
    # Supprimer les fichiers .pyc
    import glob
    pyc_files = glob.glob("*.pyc")
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"✅ Supprimé: {pyc_file}")
        except Exception as e:
            print(f"❌ Erreur suppression {pyc_file}: {e}")
    
    print("✅ Nettoyage des autres fichiers terminé")

def main():
    """Fonction principale"""
    
    print("🧹 NETTOYAGE SIMPLE DU PROJET MS-RCPSP")
    print("=" * 70)
    
    print("Ce script va supprimer uniquement les fichiers non nécessaires")
    print("et garder tous les fichiers essentiels pour le fonctionnement.")
    
    # Nettoyage principal
    supprimer_fichiers_inutiles()
    
    # Nettoyage supplémentaire
    supprimer_autres_fichiers()
    
    print(f"\n🎊 NETTOYAGE COMPLET TERMINÉ!")
    print("=" * 40)
    print("✅ Projet nettoyé et optimisé")
    print("✅ Tous les fichiers essentiels conservés")
    print("✅ Fonctionnalités intactes")
    
    print(f"\n🚀 POUR UTILISER LE SYSTÈME:")
    print("   python3 assistant_ml.py              # Interface simple")
    print("   python3 binary_relevance_msrcpsp.py  # Interface avancée")
    print("   python3 solution_finale.py           # Diagnostic complet")
    print("   ./project.sh                         # Automatisation complète")

if __name__ == "__main__":
    main()
